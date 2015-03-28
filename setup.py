try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='newrelic_ops',
      version='1.0',
      description='newrelic manipulation tool',
      long_description=open('README').read(),
      keywords='newrelic install saltstack automatic',
      url='https://github.com/Abukamel/newrelic_ops',
      author='Ahmed Kamel',
      author_email='k.tricky@gmail.com',
      license='MIT',
      packages=['newrelic_ops'],
      install_requires=['click', 'salt', 'begins', 'argparse', 'funcsigs'],
      dependency_links=['https://pypi.python.org/pypi/salt'],
      scripts=['bin/new_relic.py', 'bin/new_relic_begin.py'],
      include_package_data=True,
      zip_safe=False)
