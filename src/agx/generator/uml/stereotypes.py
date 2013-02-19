import logging
from agx.core import (
    handler,
    token,
)
from node.ext.uml.core import (
    Stereotype,
    TaggedValue,
)
from configure import registerStereotypeScope


registerStereotypeScope('stereotype', 'xmi2uml')
from agx.transform.xmi2uml.flavours import XMI2_1

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
    try:
        targetuuid = tok.uuids[st_target.uuid]
    except KeyError:
        # XXX: Heuristics: if a stereotype has accidentially been assigned to
        # the toplevel element, it doesnt work and should be ignored.
        if st_target.name.endswith('}Model'):
            logging.warn('Error getting the stereotype on the top-level '
                         'model (propably you have assigned a stereotype '
                         'there, which should not be), ignoring it '
                         '[agx.generator.uml.stereotypes, stereotype()]')
            return
        else:
            raise

    target = target.anchor.node(targetuuid)
    stereotype = Stereotype()
    stereotype.profile = target.root[source.ns_name]
    name = '%s:%s' % (source.ns_name,
                      source.__name__[source.__name__.rfind('}') + 1:])
    target[name] = stereotype
    for key in source.attributes.keys():
        if key.startswith('base_') or XMI2_1.is_profile(key):
            continue
        taggedvalue = TaggedValue()
        taggedvalue.value = source.attributes[key]
        stereotype[key] = taggedvalue

    multivals = {}

    # collect the multivalued stereotype props
    for child in source.values():
        key = child.element.tag
        if not multivals.has_key(key):
            multivals[key] = []
        multivals[key].append(child.element.text.strip())

    for k, v in multivals.items():
        tgv = TaggedValue()
        tgv.value = v
        stereotype[k] = tgv
