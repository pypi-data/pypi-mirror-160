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
build_requires = ['partis-pyproj==0.0.3', 'wheel']

EGG_INFO_NAME = 'partis-schema.egg-info'

PKG_INFO = b'Metadata-Version: 2.1\nName: partis-schema\nVersion: 0.0.3\nRequires-Python: >=3.6.2\nMaintainer-email: "Nanohmics Inc." <software.support@nanohmics.com>\nSummary: Base classes for defining JSON-compatible schemas\nLicense-File: LICENSE.txt\nClassifier: Topic :: Software Development :: Libraries\nClassifier: Programming Language :: Python :: 3\nClassifier: Operating System :: Microsoft :: Windows\nClassifier: Operating System :: POSIX :: Linux\nClassifier: License :: OSI Approved :: BSD License\nClassifier: Intended Audience :: Developers\nClassifier: Programming Language :: Python\nClassifier: Development Status :: 4 - Beta\nProvides-Extra: doc\nRequires-Dist: cheetah3<4.0.0,>=3.2.4\nRequires-Dist: tomli>=1.2.3\nRequires-Dist: wheel\nRequires-Dist: pygments==2.9.0\nRequires-Dist: partis-utils[lint]==0.0.3\nRequires-Dist: partis-pyproj==0.0.3\nRequires-Dist: ruamel.yaml==0.16.5\nRequires-Dist: overrides<4.0.0,>=3.1.0\nRequires-Dist: partis-utils[sphinx]==0.0.3; extra == "doc"\nDescription-Content-Type: text/x-rst\n\nThe ``partis.schema`` package contains base classes for defining JSON-compatible schemas.\n\nhttps://nanohmics.bitbucket.io/doc/partis/schema'

REQUIRES = b'cheetah3<4.0.0,>=3.2.4\ntomli>=1.2.3\nwheel\npygments==2.9.0\npartis-utils[lint]==0.0.3\npartis-pyproj==0.0.3\nruamel.yaml==0.16.5\noverrides<4.0.0,>=3.1.0\npartis-utils[sphinx]==0.0.3; extra == "doc"'

SOURCES = b'partis_schema-0.0.3/src/schema/prim/seq_prim.py\npartis_schema-0.0.3/src/schema/prim/__init__.py\npartis_schema-0.0.3/src/schema/prim/pass_prim.py\npartis_schema-0.0.3/src/schema/prim/map_prim.py\npartis_schema-0.0.3/src/schema/prim/base.py\npartis_schema-0.0.3/src/schema/prim/bool_prim.py\npartis_schema-0.0.3/src/schema/prim/any_prim.py\npartis_schema-0.0.3/src/schema/prim/int_prim.py\npartis_schema-0.0.3/src/schema/prim/str_prim.py\npartis_schema-0.0.3/src/schema/prim/union_prim.py\npartis_schema-0.0.3/src/schema/prim/float_prim.py\npartis_schema-0.0.3/src/schema/__init__.py\npartis_schema-0.0.3/src/schema/declared.py\npartis_schema-0.0.3/src/schema/eval/__init__.py\npartis_schema-0.0.3/src/schema/eval/eval.py\npartis_schema-0.0.3/src/schema/eval/eval_cheetah.py\npartis_schema-0.0.3/src/schema/eval/eval_py.py\npartis_schema-0.0.3/src/schema/eval/eval_pjc.py\npartis_schema-0.0.3/src/schema/serialize/__init__.py\npartis_schema-0.0.3/src/schema/serialize/config.py\npartis_schema-0.0.3/src/schema/serialize/yaml.py\npartis_schema-0.0.3/src/schema/serialize/json.py\npartis_schema-0.0.3/src/schema/serialize/utils.py\npartis_schema-0.0.3/src/schema/module.py\npartis_schema-0.0.3/src/schema/hint.py\npartis_schema-0.0.3/src/schema/plugin.py\npartis_schema-0.0.3/src/schema/valued/struct_valued.py\npartis_schema-0.0.3/src/schema/valued/__init__.py\npartis_schema-0.0.3/src/schema/valued/str_valued.py\npartis_schema-0.0.3/src/schema/valued/int_valued.py\npartis_schema-0.0.3/src/schema/valued/map_valued.py\npartis_schema-0.0.3/src/schema/valued/valued.py\npartis_schema-0.0.3/src/schema/valued/float_valued.py\npartis_schema-0.0.3/src/schema/valued/bool_valued.py\npartis_schema-0.0.3/src/schema/valued/seq_valued.py\npartis_schema-0.0.3/src/schema_meta/__init__.py\npartis_schema-0.0.3/src/schema_meta/struct.py\npartis_schema-0.0.3/src/schema_meta/eval.py\npartis_schema-0.0.3/src/schema_meta/base.py\npartis_schema-0.0.3/src/schema_meta/property.py\npartis_schema-0.0.3/src/schema_meta/schema.py\npartis_schema-0.0.3/src/schema_meta/valued.py\npartis_schema-0.0.3/src/schema_meta/prim.py\npartis_schema-0.0.3/doc/conf.py\npartis_schema-0.0.3/doc/__init__.py\npartis_schema-0.0.3/doc/index.rst\npartis_schema-0.0.3/doc/src/partis.schema.prim.union_prim.rst\npartis_schema-0.0.3/doc/src/partis.schema_meta.schema.rst\npartis_schema-0.0.3/doc/src/partis.schema_meta.struct.rst\npartis_schema-0.0.3/doc/src/partis.schema.prim.float_prim.rst\npartis_schema-0.0.3/doc/src/partis.schema_meta.rst\npartis_schema-0.0.3/doc/src/partis.schema_meta.prim.rst\npartis_schema-0.0.3/doc/src/partis.schema.prim.map_prim.rst\npartis_schema-0.0.3/doc/src/partis.schema.eval.rst\npartis_schema-0.0.3/doc/src/partis.schema.valued.rst\npartis_schema-0.0.3/doc/src/partis.schema_meta.property.rst\npartis_schema-0.0.3/doc/src/partis.schema.prim.str_prim.rst\npartis_schema-0.0.3/doc/src/partis.schema.prim.seq_prim.rst\npartis_schema-0.0.3/doc/src/partis.schema.plugin.rst\npartis_schema-0.0.3/doc/src/partis.schema.module.rst\npartis_schema-0.0.3/doc/src/partis.schema.prim.bool_prim.rst\npartis_schema-0.0.3/doc/src/partis.schema.serialize.rst\npartis_schema-0.0.3/doc/src/partis.schema.prim.base.rst\npartis_schema-0.0.3/doc/src/partis.schema.rst\npartis_schema-0.0.3/doc/src/partis.schema_meta.eval.rst\npartis_schema-0.0.3/doc/src/partis.schema_meta.base.rst\npartis_schema-0.0.3/doc/src/partis.schema.declared.rst\npartis_schema-0.0.3/doc/src/partis.schema.prim.rst\npartis_schema-0.0.3/doc/src/partis.schema_meta.valued.rst\npartis_schema-0.0.3/doc/src/partis.schema.prim.int_prim.rst\npartis_schema-0.0.3/doc/src/partis.schema.prim.pass_prim.rst\npartis_schema-0.0.3/doc/__main__.py\npartis_schema-0.0.3/test/300_schema/test_prim_str.py\npartis_schema-0.0.3/test/300_schema/test_prim_float.py\npartis_schema-0.0.3/test/300_schema/__init__.py\npartis_schema-0.0.3/test/300_schema/test_prim_map.py\npartis_schema-0.0.3/test/300_schema/test_valued.py\npartis_schema-0.0.3/test/300_schema/test_struct.py\npartis_schema-0.0.3/test/300_schema/test_prim_union.py\npartis_schema-0.0.3/test/300_schema/test_prim_bool.py\npartis_schema-0.0.3/test/300_schema/test_prim.py\npartis_schema-0.0.3/test/300_schema/test_declared.py\npartis_schema-0.0.3/test/300_schema/test_hint.py\npartis_schema-0.0.3/test/300_schema/test_prim_int.py\npartis_schema-0.0.3/test/300_schema/test_eval_pjc.py\npartis_schema-0.0.3/test/300_schema/test_prim_seq.py\npartis_schema-0.0.3/test/200_schema_meta/test_203_struct.py\npartis_schema-0.0.3/test/200_schema_meta/__init__.py\npartis_schema-0.0.3/test/200_schema_meta/test_201_base.py\npartis_schema-0.0.3/test/200_schema_meta/test_202_declared.py\npartis_schema-0.0.3/pyproject.toml\npartis_schema-0.0.3/LICENSE.txt\npartis_schema-0.0.3/README.rst'

TOP_LEVEL = b''

ENTRY_POINTS = b''

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

if __name__ == "__main__":
  exit( main() )
