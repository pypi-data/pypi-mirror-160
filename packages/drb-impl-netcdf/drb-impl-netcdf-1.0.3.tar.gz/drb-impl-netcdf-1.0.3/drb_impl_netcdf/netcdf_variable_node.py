from typing import Any, List, Dict, Optional, Tuple

import numpy
import xarray
from drb import DrbNode
from drb.exceptions import DrbNotImplementationException, DrbException
import netCDF4 as netCDF

from drb.path import ParsedPath
from drb_impl_netcdf.netcdf_common import DrbNetcdfAbstractNode, \
    DrbNetcdfSimpleValueNode


class DrbNetcdfVariableNode(DrbNetcdfAbstractNode):
    """
    This node is used to retrieve the variable of a netcdf.
    A netCDF `Variable` is used to read and write netCDF data.

    Parameters:
        parent (DrbNode): The parent of the node.
        variable (netCDF.Variable): the variable of the netcdf.
    """

    def __init__(self, parent: DrbNode, variable: netCDF.Variable):
        super().__init__()

        self._attributes: Dict[Tuple[str, str], Any] = None
        self._name = variable.name
        self._parent: DrbNode = parent
        self._children: List[DrbNode] = None
        self._path = None
        self._variable = variable
        # value scalar indicate a variable with only one value
        # in this case value return this value
        # and all method to retrieve array are not activated
        # this type of variable can be for example a time...
        self._is_scalar = len(self._variable.shape) == 0
        self.supported_impl = [netCDF.Variable]

        if not self._is_scalar:
            self.supported_impl.append(numpy.ndarray)
            if variable.mask:
                self.supported_impl.append(numpy.ma.masked_array)
                self.supported_impl.append(numpy.ma.core.MaskedArray)

    @property
    def parent(self) -> Optional[DrbNode]:
        return self._parent

    @property
    def path(self) -> ParsedPath:
        if self._path is None:
            self._path = self.parent.path / self.name
        return self._path

    @property
    def name(self) -> str:
        return self._name

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        if self._attributes is None:
            self._attributes = {}
            for attribute_name in self._variable.ncattrs():
                self._attributes[(attribute_name, None)] = getattr(
                    self._variable, attribute_name)
        return self._attributes

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        key = (name, namespace_uri)
        if key in self.attributes.keys():
            return self.attributes[key]
        raise DrbException(f'Attribute not found name: {name}, '
                           f'namespace: {namespace_uri}')

    @property
    def value(self) -> Any:
        if self._is_scalar:
            return self._variable.getValue()
        return None

    @property
    def children(self) -> List[DrbNode]:

        if self._children is None:
            self._children = []
            if not self._is_scalar:
                self._children.append(DrbNetcdfSimpleValueNode(
                    self, 'dimensions', self._variable.dimensions))
                self._children.append(DrbNetcdfSimpleValueNode(
                    self, 'shape', self._variable.shape))
            self._children.append(DrbNetcdfSimpleValueNode(
                self, 'size', self._variable.size))
        return self._children

    def has_impl(self, impl: type) -> bool:
        if impl in self.supported_impl:
            return True
        if impl == xarray.DataArray and self.parent.parent and \
                self.parent.parent.has_impl(xarray.Dataset):
            return True

    def get_impl(self, impl: type, **kwargs) -> Any:
        if self.has_impl(impl):
            if impl == netCDF.Variable:
                return self._variable
            elif impl == xarray.DataArray and self.parent.parent \
                    and self.parent.parent.has_impl(xarray.Dataset):
                xarray_dataset = self.parent.parent.get_impl(xarray.Dataset)
                return xarray_dataset[self.name]
            elif not self._is_scalar:
                if impl == numpy.ndarray and self._variable.mask:
                    # if we ask numpy array and not masked array
                    # and array is masked we temporary unset
                    # auto mask to return value unmasked
                    self._variable.set_auto_mask(False)
                    array_to_return = self._variable[:]
                    # restore mask as previous
                    self._variable.set_auto_mask(True)
                else:
                    array_to_return = self._variable[:]
                return array_to_return
        raise DrbNotImplementationException(f'no {impl} '
                                            f'implementation found')
