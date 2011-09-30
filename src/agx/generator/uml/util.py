# Copyright BlueDynamics Alliance - http://bluedynamics.com
# GNU General Public License Version 2

from agx.core import token

def isprofilemember(node):
    while True:
        if node is None:
            return False
        tag = '{http://www.eclipse.org/uml2/3.0.0/UML}Profile'
        if node.__name__.endswith(tag):
            return True
        node = node.__parent__
    return False

def assignxmiprops(node,source):
    if source.attributes.has_key('name'):
        # XXX: failed on association, have a look.
        node.xminame=source.attributes['name']
    node.xmiid=source.attributes['{http://schema.omg.org/spec/XMI/2.1}id']
