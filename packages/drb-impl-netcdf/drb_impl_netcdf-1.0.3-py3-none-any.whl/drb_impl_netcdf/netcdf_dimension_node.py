from typing import Any, Dict, Tuple
from drb import DrbNode
from drb.exceptions import DrbNotImplementationException, DrbException
import netCDF4 as netCDF

from drb_impl_netcdf import DrbNetcdfAttributeNames
from drb_impl_netcdf.netcdf_common import DrbNetcdfSimpleNode


class DrbNetcdfDimensionNode(DrbNetcdfSimpleNode):
    """
    This node is used to retrieve the dimension of a netcdf.
    A netCDF `Dimension` is used to describe the coordinates of a `Variable`.
    The value of the file is his dimension only if it is not UNLIMITED.

    Parameters:
        parent (DrbNode): The parent of the node.
        dimension (netCDF.Dimension): the dimension of the netcdf.
    """
    supported_impl = {
        netCDF.Dimension,
    }

    def __init__(self, parent: DrbNode, dimension: netCDF.Dimension):
        super().__init__(parent, dimension.name)
        self._dimension = dimension

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        """
        The attributes of this node only contain UNLIMITED a boolean,
        True if the netcdf has no limit otherwise False.
        """
        if self._attributes is None:
            self._attributes = {
                (DrbNetcdfAttributeNames.UNLIMITED.value, None):
                    self._dimension.isunlimited()}

        return self._attributes

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        key = (name, namespace_uri)
        if key in self.attributes.keys():
            return self.attributes[key]
        raise DrbException(f'Attribute not found name: {name}, '
                           f'namespace: {namespace_uri}')

    @property
    def value(self) -> Any:
        """
        Retrieve the current size of Dimension.

        Returns:
            netCDF.Dimension: the dimension.
        """
        if self._value is None:
            if self._dimension.isunlimited():
                self._value = -1
            else:
                self._value = self._dimension.size
        return self._value

    def has_impl(self, impl: type) -> bool:
        if impl in self.supported_impl:
            return True

    def get_impl(self, impl: type, **kwargs) -> Any:
        if self.has_impl(impl):
            return self._dimension
        raise DrbNotImplementationException(f'no {impl} '
                                            f'implementation found')
