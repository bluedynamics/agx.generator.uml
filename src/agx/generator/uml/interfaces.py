from zope.interface import Attribute
from node.interfaces import INode
from agx.core.interfaces import IScope


class IXMLScope(IScope):
    """XML specific scope interface.

    Uses tag names for scope identification instead of interfaces.
    """

    tags = Attribute(u"List of tags this scope applies.")
