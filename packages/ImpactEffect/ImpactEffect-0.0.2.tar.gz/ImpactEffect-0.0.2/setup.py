try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='impactEffects',
      #   use_scm_version=True,
      version="0.0.1",
      setup_requires=['setuptools_scm'],
      description="Environment for MPM assessment 3.",
      long_description="Environment for MPM assessement 3.",
      url="https://github.com/acse-dx121/impact-effects.git",
      author="Imperial College London",
      author_email='rhodri.nelson@imperial.ac.uk',
      packages=['impactEffects'])

with open("README.md", "r") as fh:
    long_description = fh.read()
