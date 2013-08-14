from agx.core import (
    handler,
    token,
)
from node.ext.uml.core import (
    Package,
    Datatype,
)
from node.ext.uml.classes import (
    Class,
    Interface,
    Association,
    AssociationClass,
)
from agx.transform.xmi2uml.flavours import XMI2_1
from configure import registerXMIScope
from util import (
    isprofilemember,
    assignxmiprops,
)


tags = [XMI2_1.PACKAGED_ELEMENT]
registerXMIScope('package', 'xmi2uml', tags, 'uml:Package')


@handler('package', 'xmi2uml', 'hierarchygenerator', 'package')
def package(self, source, target):
    """Create packages.
    """
    package = Package()
    assignxmiprops(package,source)
    target.anchor[source.attributes['name']] = package
    target.finalize(source, package)


tags = [XMI2_1.PACKAGED_ELEMENT]
registerXMIScope('class', 'xmi2uml', tags, 'uml:Class')


@handler('class', 'xmi2uml', 'hierarchygenerator', 'class')
def class_(self, source, target):
    """Create classes.
    """
    class_ = Class()
#    import pdb;pdb.set_trace()
    assignxmiprops(class_,source)
    target.anchor[source.attributes['name']] = class_
    target.finalize(source, class_)

tags = [XMI2_1.PACKAGED_ELEMENT]
registerXMIScope('interface', 'xmi2uml', tags, 'uml:Interface')


@handler('interface', 'xmi2uml', 'hierarchygenerator', 'interface')
def interface(self, source, target):
    """Create interfaces.
    """
    interface = Interface()
    assignxmiprops(interface,source)
    target.anchor[source.attributes['name']] = interface
    target.finalize(source, interface)


tags = [XMI2_1.IMPORTED_ELEMENT]
registerXMIScope('importedprimitivetype', 'xmi2uml', tags, 'uml:PrimitiveType')


@handler('importedprimitivetype', 'xmi2uml', 'hierarchygenerator', 'importedprimitivetype')
def importedprimitivetype(self, source, target):
    """Create datatypes out of imported primitivetypes.
    """
    datatype = Datatype()
    name = source.attributes['href']
    name = name[name.rfind('#') + 1:]
    tok = token('primitivetypemapping', True, types={})
    tok.types[name] = datatype.uuid
    target.anchor[name] = datatype
    target.finalize(source, datatype)


tags = [XMI2_1.PACKAGED_ELEMENT]
registerXMIScope('primitivetype', 'xmi2uml', tags, 'uml:PrimitiveType')


@handler('primitivetype', 'xmi2uml', 'hierarchygenerator', 'primitivetype')
def primitivetype(self, source, target):
    """Create datatypes out of primitivetypes.
    """
    datatype = Datatype()
    name = source.attributes['name']
    tok = token('primitivetypemapping', True, types={})
    tok.types[name] = datatype.uuid
    target.anchor[name] = datatype
    target.finalize(source, datatype)


tags = [XMI2_1.PACKAGED_ELEMENT]
registerXMIScope('datatype', 'xmi2uml', tags, 'uml:DataType')


@handler('datatype', 'xmi2uml', 'hierarchygenerator', 'datatype')
def datatype(self, source, target):
    """Create datatypes.
    """
    # XXX: discuss, if datatypes of profile are ignored, they are not available
    #      in UML representation.
    if isprofilemember(source):
        return
    datatype = Datatype()
    target.anchor[source.attributes['name']] = datatype
    target.finalize(source, datatype)


tags = [XMI2_1.PACKAGED_ELEMENT]
registerXMIScope('association', 'xmi2uml', tags, 'uml:Association')


@handler('association', 'xmi2uml', 'hierarchygenerator', 'association')
def association(self, source, target):
    """Create associations.
    """
    if isprofilemember(source):
        return
    association = Association()
    assignxmiprops(association,source)
    target.anchor[str(association.uuid)] = association
    target.finalize(source, association)

tags = [XMI2_1.PACKAGED_ELEMENT]
registerXMIScope('associationclass', 'xmi2uml', tags, 'uml:AssociationClass')


@handler('associationclass', 'xmi2uml', 'hierarchygenerator', 'associationclass')
def associationclass(self, source, target):
    """Create association classes.
    """
    if isprofilemember(source):
        return
    association = AssociationClass()
#    association = Class()
    assignxmiprops(association,source)
    import pdb;pdb.set_trace()
    target.anchor[str(association.uuid)] = association
    target.anchor[source.attributes['name']] = association
    target.finalize(source, association)

    
