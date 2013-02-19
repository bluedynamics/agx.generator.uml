from agx.core import token

from agx.transform.xmi2uml.flavours import XMI2_1

def isprofilemember(node):
    while True:
        if node is None:
            return False
        
        if XMI2_1.is_profile(node.__name__):
            return True
            
        node = node.__parent__
    return False


def assignxmiprops(node,source):
    if source.attributes.has_key('name'):
        # XXX: failed on association, have a look.
        node.xminame = source.attributes['name']
    node.xmiid = source.attributes['{http://schema.omg.org/spec/XMI/2.1}id']
