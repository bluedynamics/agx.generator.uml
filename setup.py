import os
from setuptools import (
    setup,
    find_packages,
)


version = '1.0'
shortdesc ="AGX Generator for UML Nodes"
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()


setup(name='agx.generator.uml',
      version=version,
      description=shortdesc,
      long_description=longdesc,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Operating System :: OS Independent',
          'Programming Language :: Python', 
      ],
      keywords='AGX, Code Generator, UML',
      author='BlueDynamics Alliance',
      author_email='dev@bluedynamics.com',
      url=u'https://svn.plone.org/svn/archetypes/AGX',
      license='GNU General Public Licence',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['agx', 'agx.generator'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'agx.transform.xmi2uml',
      ],
      extras_require = dict(
          test=[
            'interlude',
            'agx.transform.xmi2uml',
          ]
      ),
      entry_points="""
      # -*- Entry points: -*-
      [agx.generator]
      register = agx.generator.uml:register
      """)
