"""Usage of `setup.py` is deprecated, and is supplied only for legacy installation.
"""
import sys
import os
import os.path as osp
import importlib
import logging
import argparse
import subprocess
import tempfile
from argparse import RawTextHelpFormatter
logger = logging.getLogger(__name__)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def egg_info( args ):

  logger.warning(
    "running legacy 'setup.py egg_info'" )

  dir = osp.join( args.egg_base, EGG_INFO_NAME )

  if not osp.exists( dir ):
    os.mkdir( dir )

  with open( osp.join( dir, 'PKG-INFO' ), 'wb' ) as fp:
    fp.write( PKG_INFO )

  with open( osp.join( dir, 'setup_requires.txt' ), 'wb' ) as fp:
    fp.write( b'' )

  with open( osp.join( dir, 'requires.txt' ), 'wb' ) as fp:
    fp.write( REQUIRES )

  with open( osp.join( dir, 'SOURCES.txt' ), 'wb' ) as fp:
    fp.write( SOURCES )

  with open( osp.join( dir, 'top_level.txt' ), 'wb' ) as fp:
    fp.write( TOP_LEVEL )

  with open( osp.join( dir, 'entry_points.txt' ), 'wb' ) as fp:
    fp.write( ENTRY_POINTS )

  with open( osp.join( dir, 'dependency_links.txt' ), 'wb' ) as fp:
    fp.write( b'' )

  with open( osp.join( dir, 'not-zip-safe' ), 'wb' ) as fp:
    fp.write( b'' )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def bdist_wheel( args ):

  logger.warning(
    "running legacy 'setup.py bdist_wheel'" )

  sys.path = backend_path + sys.path

  backend = importlib.import_module( build_backend )

  backend.build_wheel(
    wheel_directory = args.dist_dir or args.bdist_dir or '.' )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def install( args ):

  logger.warning(
    "running legacy 'setup.py install'" )

  reqs = [ f"{r}" for r in build_requires ]

  subprocess.check_call([
    sys.executable,
    '-m',
    'pip',
    'install',
    *reqs ] )

  sys.path = backend_path + sys.path

  backend = importlib.import_module( build_backend )

  with tempfile.TemporaryDirectory() as tmpdir:
    wheel_name = backend.build_wheel(
      wheel_directory = tmpdir )

    subprocess.check_call([
      sys.executable,
      '-m',
      'pip',
      'install',
      osp.join(tmpdir, wheel_name) ])

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def dummy( args ):
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def main():

  logging.basicConfig(
    level = logging.INFO,
    format = "{name}:{levelname}: {message}",
    style = "{" )


  logger.warning(
    "'setup.py' is deprecated, limited support for legacy installs. Upgrade pip." )

  parser = argparse.ArgumentParser(
    description = __doc__,
    formatter_class = RawTextHelpFormatter )

  subparsers = parser.add_subparsers()

  #.............................................................................
  egg_info_parser = subparsers.add_parser( 'egg_info' )

  egg_info_parser.set_defaults( func = egg_info )

  egg_info_parser.add_argument( "-e", "--egg-base",
    type = str,
    default = '.' )

  #.............................................................................
  bdist_wheel_parser = subparsers.add_parser( 'bdist_wheel' )

  bdist_wheel_parser.set_defaults( func = bdist_wheel )

  bdist_wheel_parser.add_argument( "-b", "--bdist-dir",
    type = str,
    default = '' )

  bdist_wheel_parser.add_argument( "-d", "--dist-dir",
    type = str,
    default = '' )

  bdist_wheel_parser.add_argument( "--python-tag",
    type = str,
    default = None )

  bdist_wheel_parser.add_argument( "--plat-name",
    type = str,
    default = None )

  bdist_wheel_parser.add_argument( "--py-limited-api",
    type = str,
    default = None )

  bdist_wheel_parser.add_argument( "--build-number",
    type = str,
    default = None )

  #.............................................................................
  install_parser = subparsers.add_parser( 'install' )

  install_parser.set_defaults( func = install )

  install_parser.add_argument( "--record",
    type = str,
    default = None )

  install_parser.add_argument( "--install-headers",
    type = str,
    default = None )

  install_parser.add_argument( "--compile",
    action='store_true' )

  install_parser.add_argument( "--single-version-externally-managed",
    action='store_true' )

  #.............................................................................
  clean_parser = subparsers.add_parser( 'clean' )

  clean_parser.set_defaults( func = dummy )

  clean_parser.add_argument( "-a", "--all",
    action='store_true' )

  args = parser.parse_args( )

  args.func( args )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# NOTE: these are templated literal values substituded by the backend when
# building the source distribution

build_backend = 'partis.pyproj.backend'
backend_path = []
build_requires = ['wheel', 'partis-pyproj==0.0.3']

EGG_INFO_NAME = 'partis.egg-info'

PKG_INFO = b'Metadata-Version: 2.1\nName: partis\nVersion: 0.0.3\nRequires-Python: >=3.6.2\nMaintainer-email: "Nanohmics Inc." <software.support@nanohmics.com>\nSummary: Top-level namespace package for partis packages\nLicense-File: LICENSE.txt\nProvides-Extra: test\nProvides-Extra: cov\nProvides-Extra: lint\nRequires-Dist: wheel\nRequires-Dist: partis-view==0.0.3\nRequires-Dist: partis-utils[sphinx]==0.0.3\nRequires-Dist: partis-nwl==0.0.3\nRequires-Dist: partis-schema==0.0.3\nRequires-Dist: partis-pyproj==0.0.3\nRequires-Dist: numpy; extra == "test"\nRequires-Dist: pytest>=6.2.5; extra == "test"\nRequires-Dist: meson>=0.61.3; extra == "test"\nRequires-Dist: pytest-cov>=3.0.0; extra == "test"\nRequires-Dist: ninja>=1.10.2.3; extra == "test"\nRequires-Dist: pip>=18.1; extra == "test"\nRequires-Dist: coverage[toml]>=6.2; extra == "test"\nRequires-Dist: nox>=2021.10.1; extra == "test"\nRequires-Dist: Cython>=0.29.18; extra == "test"\nRequires-Dist: pytest_mock>=3.6.1; extra == "test"\nRequires-Dist: tomli>=1.2.3; extra == "test"\nRequires-Dist: PyVirtualDisplay>=2.2; extra == "test"\nRequires-Dist: build>=0.7.0; extra == "test"\nRequires-Dist: coverage[toml]>=6.2; extra == "cov"\nRequires-Dist: pyflakes==2.4.0; extra == "lint"\nDescription-Content-Type: text/x-rst\n\nReadme for partis\n=================\n\n\nUtilities for defining and validating schemas for YAML/JSON compatible data, and\nfor configuring and running programs/workflows using the domain specific\nNano Workflow Language (NWL).\n\n\nInstallation\n------------\n\nCompatible with Python >= 3.6, pip >= 18.1.\n\nFor full install of core API, docs, runtime utilities, and GUI application:\n\n.. code-block:: bash\n\n  python3 make_dists.py\n  pip3 install --find-links ./dist partis\n\nTo install only a particular set of sub-component(s), such as the nwl command-line runner:\n\n.. code-block:: bash\n\n  pip3 install --find-links ./dist partis-pyproj\n  pip3 install --find-links ./dist partis-utils\n  pip3 install --find-links ./dist partis-schema\n  pip3 install --find-links ./dist partis-nwl\n\nNote that unless distributions have already been generated and made available to\npip, these must be done in the above order.\n\nBuilding the Documentation\n--------------------------\n\nThe ``doc`` folder is made as a runnable python module to conveniently\nbuild documentation.\nBy default, html documentation will be generated in a ``build`` directory.\n\n.. code-block:: bash\n\n  pip3 install --find-links ./dist \'.[doc]\'\n  python -m doc\n\n.. note::\n\n  Any changes to source-code will not be reflected until the package is rebuilt.\n\nRunning the Tests\n-----------------\n\nThe ``test`` folder is made as a runnable python module to conveniently\nrun automated test suite.\n\nTo test the GUI, Xvfb must also be installed on the system to create\na virtual display in order to run the Qt application without displaying windows.\nIf Xvfb is not found those tests will be skipped.\n\nTo test multiple versions of python, they must all be discoverable within the\n``PATH`` environment variable.\nThe tests configured for versions of python that cannot be found will be skipped.\nFor example, if the python installations are being managed with the Environment\nModules convention:\n\n.. code:: bash\n\n  module load python/3.6.2\n  module load python/3.7.0\n  module load python/3.8.0\n  module load python/3.9.0\n\nIt is highly recommended to install package and dependencies within a virtual\nenvironment to isolate the effects of any changes it may cause.\n\n.. code:: bash\n\n  pip install --find-links ./dist \'.[test]\'\n  python -m test\n\nDevelopment\n===========\n\npre-commit\n----------\n\nBefore committing any changes to this repo, please install pre-commit and hooks.\n\n.. code-block:: bash\n\n  pip install pre-commit\n  pre-commit install\n  pre-commit run --all-files\n\nA convenience script ``runme.py`` is placed in the root directory to perform this action,\nand needs to be run only once.\n\n.. note::\n\n  The ``pre-commit`` program is installed as a Python package.\n  If a virtual environment is used during development, ensure that ``pre-commit``\n  is installed in the environment active at the time of any commit.'

REQUIRES = b'wheel\npartis-view==0.0.3\npartis-utils[sphinx]==0.0.3\npartis-nwl==0.0.3\npartis-schema==0.0.3\npartis-pyproj==0.0.3\nnumpy; extra == "test"\npytest>=6.2.5; extra == "test"\nmeson>=0.61.3; extra == "test"\npytest-cov>=3.0.0; extra == "test"\nninja>=1.10.2.3; extra == "test"\npip>=18.1; extra == "test"\ncoverage[toml]>=6.2; extra == "test"\nnox>=2021.10.1; extra == "test"\nCython>=0.29.18; extra == "test"\npytest_mock>=3.6.1; extra == "test"\ntomli>=1.2.3; extra == "test"\nPyVirtualDisplay>=2.2; extra == "test"\nbuild>=0.7.0; extra == "test"\ncoverage[toml]>=6.2; extra == "cov"\npyflakes==2.4.0; extra == "lint"'

SOURCES = b'partis-0.0.3/test/__init__.py\npartis-0.0.3/test/__main__.py\npartis-0.0.3/test/sitecustom/partis-sitecustom.pth\npartis-0.0.3/test/sitecustom/pyproject.toml\npartis-0.0.3/test/noxfile.py\npartis-0.0.3/test/.flake8\npartis-0.0.3/pyproject.toml\npartis-0.0.3/README.rst\npartis-0.0.3/LICENSE.txt'

TOP_LEVEL = b''

ENTRY_POINTS = b''

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

if __name__ == "__main__":
  exit( main() )
