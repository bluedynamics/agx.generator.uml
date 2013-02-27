from agx.core import token

from agx.transform.xmi2uml.flavours import get_active_flavour

def isprofilemember(node):
    while True:
        if node is None:
            return False
        
        if get_active_flavour().is_profile(node.__name__):
            return True
            
        node = node.__parent__
    return False


def assignxmiprops(node,source):
    if source.attributes.has_key('name'):
        # XXX: failed on association, have a look.
        node.xminame = source.attributes['name']
        
    node.xmiid = source.attributes['{%s}id' % source.namespaces['xmi']]
