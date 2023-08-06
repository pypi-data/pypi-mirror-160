import abc
import enum
from abc import ABC
from typing import Optional, List, Any, Dict, Tuple


from drb import DrbNode, AbstractNode
from drb.exceptions import DrbNotImplementationException, DrbException
from drb.path import ParsedPath

NAMESPACE_NETCDF_NODE = None


class DrbNetcdfAttributeNames(enum.Enum):
    UNLIMITED = 'unlimited'
    """
    A boolean indicating whether the netcdf file has a fixed size or not.
    """


class DrbNetcdfAbstractNode(AbstractNode, abc.ABC):
    """
    This node will be inherited by other netcdf node.
    """
    _path = None

    @property
    def namespace_uri(self) -> Optional[str]:
        """
        Not use in this implementation.

        Return:
            None
        """
        return NAMESPACE_NETCDF_NODE

    def close(self) -> None:
        """
        Not use in this implementation.
        Do nothing.
        """
        pass

    @property
    def path(self) -> ParsedPath:
        """
        Returns the path of the node.

        Returns:
            ParsedPath: The path of the node.
        """
        if self._path is None:
            self._path = self.parent.path / self.name
        return self._path


class DrbNetcdfSimpleNode(DrbNetcdfAbstractNode, ABC):
    """
    This node will be inherited by DrbNetcdfSimpleValueNode
    and DrbNetcdfDimensionNode.

    It is used to represent the key to a node with value.

    Parameters:
        parent (DrbNode): The parent of the node.
        name (str): the name of the node.
    """

    def __init__(self, parent: DrbNode, name):
        super().__init__()
        self._parent: DrbNode = parent
        self._attributes = None
        self._name = name
        self._value = None

    @property
    def parent(self) -> Optional[DrbNode]:
        """
        Return the parent of this node if he has one otherwise None.

        Returns:
            DrbNode: The parent of this node or None.
        """
        return self._parent

    @property
    def name(self) -> str:
        """
        Return the name of the node.
        This name doesn't contain the path of the node.

        Returns:
            str: the file name
        """
        return self._name

    @property
    def children(self) -> List[DrbNode]:
        """
        This node as no children.

        Returns:
            List: An empty List
        """
        return []


class DrbNetcdfSimpleValueNode(DrbNetcdfSimpleNode):
    """
    This node is used to get a simple value.

    Parameters:
        parent (DrbNode): The parent of the node.
        name (str): the name of the node.
        value (any): the value.
    """
    def __init__(self, parent: DrbNode, name: str, value: any):
        super().__init__(parent, name)
        self._value = value

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        """
        This node as no attributes.

        Returns:
            Dict: An empty Dict
        """
        return {}

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        raise DrbException(f'Attribute not found name: {name}, '
                           f'namespace: {namespace_uri}')

    @property
    def value(self) -> Any:
        """
        Get the value of the node.

        Returns:
            Any: the value.
        """
        return self._value

    def has_impl(self, impl: type) -> bool:
        return False

    def get_impl(self, impl: type, **kwargs) -> Any:
        raise DrbNotImplementationException(f'no {impl} '
                                            f'implementation found')
