from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='collective.timedevents',
      version=version,
      description="Easy to use clock mechanism for software developers who need time based Zope events",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone zope events clock time',
      author='Mikko Ohtamaa',
      author_email='mikko.ohtamaa@twinapex.com',
      url='http://www.twinapex.com',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
