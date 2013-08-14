from agx.core import (
    handler,
    token,
)
from agx.core.util import write_source_to_target_mapping
from node.ext.xmi.interfaces import IXMINode
from node.ext.uml.core import Profile
from agx.transform.xmi2uml.flavours import get_active_flavour
from configure import (
    registerXMLScope,
    registerXMIScope,
)


tags = get_active_flavour().profiles()
#XXX: should be implemented, so that regexps are supported
registerXMLScope('profile', 'xmi2uml', tags)


@handler('profile', 'xmi2uml', 'profilegenerator', 'profile')
def profile(self, source, target):
    """Create profile.
    """
    profile = Profile()
    target.anchor.root[source.attributes['name']] = profile
    write_source_to_target_mapping(source, profile)


tags = [get_active_flavour().PACKAGED_ELEMENT]
registerXMIScope('stereotypedef', 'xmi2uml', tags, 'uml:Stereotype')


@handler('stereotypetokenizer', 'xmi2uml', 'profilegenerator', 'stereotypedef')
def stereotypetokenizer(self, source, target):
    """Collect stereotype definitions from UML profile.
    """
    next = source
    while True:
        next = next.__parent__
        if IXMINode.providedBy(next) or next is None:
            break
        profilexml = next
    profile = profilexml.values()[0].attributes['name']
    
    defs = {
        'id': source.attributes['{%s}id' % source.namespaces['xmi']],
        'name': source.attributes['name'],
        'profile': profile,
    }
    tok = token('stereotypedefinitions', True, defs={})
    tok.defs[source.attributes['name']] = defs
