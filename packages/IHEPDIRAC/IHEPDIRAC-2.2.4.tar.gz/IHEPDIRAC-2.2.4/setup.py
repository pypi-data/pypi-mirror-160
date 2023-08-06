from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from dirac_webapp_packaging import extjs_cmdclass
from setuptools import setup
# This is required to allow editable pip installs while using the declarative configuration (setup.cfg)
setup(cmdclass=extjs_cmdclass)
