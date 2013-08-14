from agx.core import (
    handler,
    token,
)
from node.ext.uml.core import INFINITE
from node.ext.uml.classes import (
    Property,
    Operation,
    Parameter,
    AssociationEnd,
    Dependency,
    Generalization,
    InterfaceRealization,
)
from agx.transform.xmi2uml.flavours import XMI2_1
from configure import (
    registerXMLScope,
    registerXMIScope,
)
from util import (
    isprofilemember,
    assignxmiprops,
)


@handler('anchorpackage', 'xmi2uml',
         'datatypedependentgenerator',
         'package', order=10)
@handler('anchorclass', 'xmi2uml',
         'datatypedependentgenerator',
         'class', order=10)
@handler('anchorinterface', 'xmi2uml',
         'datatypedependentgenerator',
         'interface', order=10)
def anchor(self, source, target):
    """Dummy handler for target preperation.
    """
    target.finalize(source, target.anchor[source.attributes['name']])


tags = [XMI2_1.OWNED_ATTRIBUTE]
registerXMLScope('property', 'xmi2uml', tags)


@handler('property', 'xmi2uml', 'datatypedependentgenerator',
         'property', order=20)
def property(self, source, target):
    """Create property.
    """
    if isprofilemember(source):
        return
    if source.attributes.get('association', None) is not None:
        return
    if 'type' in source.attributes.keys():
        typedef = source.refindex[source.attributes['type']]
        tok = token('sourcetotargetuuidmapping', False)
        type = target.anchor.node(tok.uuids[typedef.uuid])
    else:
        try:
            name = source['type'].attributes['href']
        except KeyError:
            raise ValueError,'Property "%s" in class "%s" has no datatype!' % \
                (source.element.get('name'),source.parent.element.get('name'))
        name = name[name.rfind('#') + 1:]
        tok = token('primitivetypemapping', False)
        type = target.anchor.node(tok.types[name])
    property = Property()
    assignxmiprops(property,source)

    property.type = type
    target.anchor[source.attributes['name']] = property
    target.finalize(source, property)


tags = [XMI2_1.OWNED_OPERATION]
registerXMLScope('operation', 'xmi2uml', tags)


@handler('operation', 'xmi2uml', 'datatypedependentgenerator',
         'operation', order=20)
def operation(self, source, target):
    """Create operation.
    """
    operation = Operation()
    import pdb;pdb.set_trace()
    assignxmiprops(operation,source)
    target.anchor[source.attributes['name']] = operation
    target.finalize(source, operation)


tags = [XMI2_1.OWNED_PARAMETER]
registerXMLScope('parameter', 'xmi2uml', tags)


@handler('parameter', 'xmi2uml', 'datatypedependentgenerator',
         'parameter', order=20)
def parameter(self, source, target):
    """Create parameter.
    """
    parameter = Parameter()
    dt_source = source.refindex[source.attributes['type']]
    tok = token('sourcetotargetuuidmapping', False)
    datatypeuuid = tok.uuids[dt_source.uuid]
    datatype = target.anchor.node(datatypeuuid)
    parameter.type = datatype
    parameter.direction = source.attributes['direction']
    # XXX: check name handling, incoming parameters missing.
    target.anchor[str(source.uuid)] = parameter
    target.finalize(source, parameter)


tags = [XMI2_1.OWNED_END]
registerXMLScope('ownedend', 'xmi2uml', tags)


@handler('ownedend', 'xmi2uml', 'datatypedependentgenerator',
         'ownedend', order=20)
def ownedend(self, source, target):
    """Create owned end.
    """
    if isprofilemember(source):
        return
    oe_source = source.refindex[source.attributes['association']]
    tok = token('sourcetotargetuuidmapping', False)
    associationuuid = tok.uuids[oe_source.uuid]
    association = target.anchor.node(associationuuid)
    associationend = AssociationEnd()
    assignxmiprops(associationend,source)
    associationend.association = association
    # XXX: we the private uuid listing pointing to member ends. could
    #      be simlified, read node.ext.uml.classes for details
    association._memberEnds.append(associationend.uuid)
    cla_source = source.refindex[source.attributes['type']]
    classuuid = tok.uuids[cla_source.uuid]
    associationend.type = target.anchor.node(classuuid)
    uppervalue = source['upperValue'].attributes['value']
    if uppervalue == '*':
        uppervalue = INFINITE
    else:
        uppervalue = int(uppervalue)
    associationend.uppervalue = uppervalue
    lowervalue = source['lowerValue'].attributes.get('value', '*')
    if lowervalue == '*':
        lowervalue = INFINITE
    else:
        lowervalue = int(lowervalue)
    associationend.lowervalue = lowervalue
    association[source.attributes['name']] = associationend
    target.finalize(source, associationend)


tags = [XMI2_1.OWNED_ATTRIBUTE]
registerXMLScope('memberend', 'xmi2uml', tags)


@handler('memberend', 'xmi2uml', 'datatypedependentgenerator',
         'memberend', order=20)
def memberend(self, source, target):
    """Create member end.
    """
    if isprofilemember(source):
        return
    if source.attributes.get('association', None) is None:
        return
    
    me_source = source.refindex[source.attributes['association']]
    tok = token('sourcetotargetuuidmapping', False)
    associationuuid = tok.uuids[me_source.uuid]
    association = target.anchor.node(associationuuid)
    assignxmiprops(memberend,source)
    associationend = AssociationEnd()
    associationend.association = association
    # XXX: we the private uuid listing pointing to member ends. could
    #      be simlified, read node.ext.uml.classes for details
    association._memberEnds.append(associationend.uuid)
    cla_source = source.refindex[source.attributes['type']]
    classuuid = tok.uuids[cla_source.uuid]
    associationend.type = target.anchor.node(classuuid)
    associationend.aggregationkind=associationend.aggregationkind or \
        source.element.attrib.get('aggregation')

    uppervalue = source['upperValue'].attributes['value']
    if uppervalue == '*':
        uppervalue = INFINITE
    else:
        uppervalue = int(uppervalue)
    associationend.uppervalue = uppervalue
    lowervalue = source['lowerValue'].attributes.get('value', '*')
    if lowervalue == '*':
        lowervalue = INFINITE
    else:
        lowervalue = int(lowervalue)
    associationend.lowervalue = lowervalue
    target.anchor[source.attributes['name']] = associationend
    target.finalize(source, associationend)


tags = [XMI2_1.PACKAGED_ELEMENT]
registerXMIScope('dependency', 'xmi2uml', tags, 'uml:Dependency')


@handler('dependency', 'xmi2uml', 'datatypedependentgenerator',
         'dependency', order=20)
def dependency(self, source, target):
    if isprofilemember(source):
        return
    tok = token('sourcetotargetuuidmapping', False)
    supplier_source = source.refindex[source.attributes['supplier']]
    supplieruuid = tok.uuids[supplier_source.uuid]
    supplier = target.anchor.node(supplieruuid)
    client_source = source.refindex[source.attributes['client']]
    clientuuid = tok.uuids[client_source.uuid]
    client = target.anchor.node(clientuuid)
    dependency = Dependency()
    assignxmiprops(dependency,source)
    dependency.client = client
    dependency.supplier = supplier
    target.anchor[str(dependency.uuid)] = dependency
    target.finalize(source, dependency)


tags = [XMI2_1.GENERALIZATION]
registerXMLScope('generalization', 'xmi2uml', tags)


@handler('generalization', 'xmi2uml', 'datatypedependentgenerator',
         'generalization', order=20)
def generalization(self, source, target):
    """Create generalization.
    """
    if isprofilemember(source):
        return
    tok = token('sourcetotargetuuidmapping', False)
    containeruuid = tok.uuids[source.__parent__.uuid]
    container = target.anchor.node(containeruuid)
    general_source = source.refindex[source.attributes['general']]
    generaluuid = tok.uuids[general_source.uuid]
    general = target.anchor.node(generaluuid)
    generalization = Generalization()
    generalization.general = general
    container[str(generalization.uuid)] = generalization
    target.finalize(source, generalization)


tags = [XMI2_1.INTERFACE_REALIZATION]
registerXMLScope('interfacerealization', 'xmi2uml', tags)


@handler('interfacerealization', 'xmi2uml', 'datatypedependentgenerator',
         'interfacerealization', order=20)
def interfacerealization(self, source, target):
    """Create interface realization.
    """
    if isprofilemember(source):
        return
    tok = token('sourcetotargetuuidmapping', False)
    containeruuid = tok.uuids[source.__parent__.uuid]
    container = target.anchor.node(containeruuid)
    contract_source = source.refindex[source.attributes['contract']]
    contractuuid = tok.uuids[contract_source.uuid]
    contract = target.anchor.node(contractuuid)
    interfacerealization = InterfaceRealization()
    interfacerealization.contract = contract
    container[str(interfacerealization.uuid)] = interfacerealization
    target.finalize(source, interfacerealization)
