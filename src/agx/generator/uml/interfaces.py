# Copyright BlueDynamics Alliance - http://bluedynamics.com
# GNU General Public License Version 2

from zope.interface import Attribute
from zodict.interfaces import INode
from agx.core.interfaces import IScope

class IXMLScope(IScope):
    """XML specific scope interface.
    
    Uses tag names for scope identification instead of interfaces.
    """
    
    tags = Attribute(u"List of tags this scope applies.")