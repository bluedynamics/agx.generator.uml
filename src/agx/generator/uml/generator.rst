Test transform related generators
=================================

::
    >>> import os
    >>> modelpath = os.path.sep.join([datadir, 'examplegg.uml'])
    >>> profilepath = os.path.sep.join([datadir, 'pyegg.profile.uml'])

    >>> from zope.component import getUtility
    >>> from agx.core.interfaces import ITransform
    >>> from agx.core import Processor
    >>> transform = getUtility(ITransform, name="xmi2uml")
    >>> processor = Processor('xmi2uml')
    >>> xmi = transform.source([modelpath, profilepath])
    >>> uml = processor(transform.source([modelpath, profilepath]),
    ...                 transform.target('Model'))
    >>> uml
    <Model object 'Model' at ...>

    >>> from agx.core import token
    >>> tok = token('stereotypedefinitions', False)
    >>> tok.defs
    {'pyegg': {'profile': 'pyegg', 'id': '...', 'name': 'pyegg'}, 
    'DecoratedClass': {'profile': 'pyegg', 'id': '...', 'name': 'DecoratedClass'}}

    >>> uml.printtree()
    <class 'node.ext.uml.core.Model'>: Model
      <class 'node.ext.uml.core.Profile'>: pyegg
      <class 'node.ext.uml.core.Datatype'>: Boolean
      <class 'node.ext.uml.core.Datatype'>: String
      <class 'node.ext.uml.core.Datatype'>: UnlimitedNatural
      <class 'node.ext.uml.core.Datatype'>: Integer
      <class 'node.ext.uml.core.Package'>: example.agx.egg
        <class 'node.ext.uml.core.Package'>: mypackage
          <class 'node.ext.uml.classes.Class'>: MyClass
            <class 'node.ext.uml.classes.Property'>: myattribute1
            <class 'node.ext.uml.classes.Operation'>: operation
            <class 'node.ext.uml.classes.Operation'>: operation1
              <class 'node.ext.uml.classes.Parameter'>: ...
          <class 'node.ext.uml.core.Datatype'>: DataTypeInPkg
          <class 'node.ext.uml.core.Package'>: browser
            <class 'node.ext.uml.classes.Class'>: YourClass
              <class 'node.ext.uml.classes.Property'>: yourattr
              <class 'node.ext.uml.core.Stereotype'>: DecoratedClass
                <class 'node.ext.uml.core.TaggedValue'>: decorator
        <class 'node.ext.uml.core.Stereotype'>: pyegg
      <class 'node.ext.uml.core.Datatype'>: MyFancyDatatype
      <class 'node.ext.uml.core.Package'>: myassociations
        <class 'node.ext.uml.classes.Class'>: Klass1
        <class 'node.ext.uml.classes.Class'>: Klass2
        <class 'node.ext.uml.classes.Class'>: Klass1_1
          <class 'node.ext.uml.classes.Generalization'>: ...
          <class 'node.ext.uml.classes.AssociationEnd'>: dst
        <class 'node.ext.uml.classes.Class'>: Klass4
          <class 'node.ext.uml.classes.InterfaceRealization'>: ...
        <class 'node.ext.uml.classes.Interface'>: Interface
        <class 'node.ext.uml.classes.Association'>: ...
          <class 'node.ext.uml.classes.AssociationEnd'>: src
        <class 'node.ext.uml.classes.Association'>: ...
          <class 'node.ext.uml.classes.AssociationEnd'>: src
          <class 'node.ext.uml.classes.AssociationEnd'>: dst
        <class 'node.ext.uml.classes.Association'>: ...
          <class 'node.ext.uml.classes.AssociationEnd'>: src
          <class 'node.ext.uml.classes.AssociationEnd'>: dst
        <class 'node.ext.uml.classes.Association'>: ...
          <class 'node.ext.uml.classes.AssociationEnd'>: src
          <class 'node.ext.uml.classes.AssociationEnd'>: dst
        <class 'node.ext.uml.classes.Dependency'>: ...
