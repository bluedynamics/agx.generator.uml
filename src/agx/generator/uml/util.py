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