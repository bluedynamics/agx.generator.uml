# Copyright BlueDynamics Alliance - http://bluedynamics.com
# GNU General Public License Version 2

from agx.core import handler
from agx.core import token
from agx.io.uml.core import (
    Package,
    Datatype,
)
from agx.io.uml.classes import (
    Class,
    Interface,
    Association,
)
from agx.transform.xmi2uml.flavours import XMI2_1
from configure import registerXMIScope
from util import isprofilemember

tags = [XMI2_1.PACKAGED_ELEMENT]
registerXMIScope('package', 'xmi2uml', tags, 'uml:Package')

@handler('package', 'xmi2uml', 'hierarchygenerator', 'package')
def package(self, source, target):
    """Create packages.
    """
    package = Package()
    target.anchor[source.attributes['name']] = package
    target.finalize(source, package)

tags = [XMI2_1.PACKAGED_ELEMENT]
registerXMIScope('class', 'xmi2uml', tags, 'uml:Class')

@handler('class', 'xmi2uml', 'hierarchygenerator', 'class')
def class_(self, source, target):
    """Create classes.
    """
    class_ = Class()
    target.anchor[source.attributes['name']] = class_
    target.finalize(source, class_)

tags = [XMI2_1.PACKAGED_ELEMENT]
registerXMIScope('interface', 'xmi2uml', tags, 'uml:Interface')

@handler('interface', 'xmi2uml', 'hierarchygenerator', 'interface')
def interface(self, source, target):
    """Create interfaces.
    """
    interface = Interface()
    target.anchor[source.attributes['name']] = interface
    target.finalize(source, interface)

tags = [XMI2_1.IMPORTED_ELEMENT]
registerXMIScope('primitivetype', 'xmi2uml', tags, 'uml:PrimitiveType')

@handler('primitivetype', 'xmi2uml', 'hierarchygenerator', 'primitivetype')
def primitivetype(self, source, target):
    """Create datatypes out of primitivetypes.
    """
    datatype = Datatype()
    name = source.attributes['href']
    name = name[name.rfind('#') + 1:]
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
    target.anchor[str(association.uuid)] = association
    target.finalize(source, association)