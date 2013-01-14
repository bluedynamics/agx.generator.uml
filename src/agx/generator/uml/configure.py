from zope.component import provideUtility
from agx.core.interfaces import IScope
from agx.core.metaconfigure import _chkregistered
from scope import (
    XMLScope,
    XMIScope,
    StereotypeScope,
)


def registerXMLScope(name, transform, tags, class_=XMLScope):
    name = '%s.%s' % (transform, name)
    _chkregistered(IScope, name=name)
    scope = XMLScope(name, tags)
    provideUtility(scope, provides=IScope, name=name)


def registerXMIScope(name, transform, tags, type, class_=XMIScope):
    name = '%s.%s' % (transform, name)
    _chkregistered(IScope, name=name)
    scope = class_(name, tags, type)
    provideUtility(scope, provides=IScope, name=name)


def registerStereotypeScope(name, transform, class_=StereotypeScope):
    name = '%s.%s' % (transform, name)
    _chkregistered(IScope, name=name)
    scope = class_()
    provideUtility(scope, provides=IScope, name=name)
