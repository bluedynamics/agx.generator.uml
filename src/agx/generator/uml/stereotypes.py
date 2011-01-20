# Copyright BlueDynamics Alliance - http://bluedynamics.com
# GNU General Public License Version 2

from agx.core import handler
from agx.core import token
from agx.io.uml.core import Stereotype
from agx.io.uml.core import TaggedValue
from configure import registerStereotypeScope

registerStereotypeScope('stereotype', 'xmi2uml')

@handler('stereotype', 'xmi2uml', 'stereotypegenerator', 'stereotype')
def stereotype(self, source, target):
    """Create stereotypes.
    """
    attrname = None
    for key in source.attributes.keys():
        if key.startswith('base_'):
            attrname = key
    if not attrname:
        return
    st_target = source.refindex[source.attributes[attrname]]
    tok = token('sourcetotargetuuidmapping', False)
    targetuuid = tok.uuids[st_target.uuid]
    target = target.anchor.node(targetuuid)
    stereotype = Stereotype()
    stereotype.profile = target.root[source.ns_name]
    name = '%s:%s' % (source.ns_name,
                      source.__name__[source.__name__.rfind('}') + 1:])
    target[name] = stereotype
    for key in source.attributes.keys():
        if key.startswith('base_') \
          or key == '{http://schema.omg.org/spec/XMI/2.1}id':
            continue
        taggedvalue = TaggedValue()
        taggedvalue.value = source.attributes[key]
        stereotype[key] = taggedvalue