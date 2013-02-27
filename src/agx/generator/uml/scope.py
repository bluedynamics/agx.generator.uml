import types
from zope.interface import implementer
from zope.component.interfaces import ComponentLookupError
from agx.core import (
    token,
    Scope,
)
from node.ext.xml.interfaces import IXMLNode
from interfaces import IXMLScope
from agx.transform.xmi2uml.flavours import get_active_flavour


@implementer(IXMLScope)
class XMLScope(Scope):
    """XML scope implementation.
    """

    def __init__(self, name, tags):
        if not type(tags) == types.ListType:
            tags = [tags]
        self.name = name
        self.interfaces = None # just provide due original interface, not used
        self.tags = tags

    def __call__(self, node):
        for tag in self.tags:
            if node.__name__[node.__name__.find(':') + 1:] == tag:
                return True
        return False


class XMIScope(XMLScope):
    """XMI scope implementation.

    Derives from XMLScope and takes an additional type to check against the
    type.
    """

    def __init__(self, name, tags, type):
        XMLScope.__init__(self, name, tags)
        self.type = type

    def __call__(self, node):
        tagmatches = False
        for tag in self.tags:
            if node.__name__[node.__name__.find(':') + 1:] == tag:
                tagmatches = True
                break
        if tagmatches:
            #XXX:move to XMI Flavor
            
            for ns in get_active_flavour().XMI_NS_ALT:
                name = '{%s}type' % ns
                if node.attributes.get(name) == self.type:
                    return True
        return False


class StereotypeScope(Scope):
    """Stereotype scope implementation.
    """

    def __init__(self):
        pass

    def __call__(self, node):
        if not IXMLNode.providedBy(node):
            return
        nsmapping = self._nsmapping(node)
        if not nsmapping:
            return
        tok = self._token
        if not tok:
            return False
        for stdef in tok.defs.values():
            if node.__name__.find(nsmapping.get(stdef['profile'], '')) != -1:
                return True
        return False

    @property
    def _token(self):
        try:
            return token('stereotypedefinitions', False)
        except ComponentLookupError, e:
            return None

    @property
    def _tokennamespaces(self):
        tok = self._token
        if not tok:
            return None
        return [stdef['profile'] for stdef in tok.defs.values()]

    def _nsmapping(self, node):
        ret = dict()
        tokns = self._tokennamespaces
        if not tokns:
            return None
        for ns in tokns:
            for key, value in node.namespaces.items():
                if ns == value or ns == key: # ??
                    ret[ns] = key
        return ret
