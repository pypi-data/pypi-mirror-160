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

EGG_INFO_NAME = 'partis-utils.egg-info'

PKG_INFO = b'Metadata-Version: 2.1\nName: partis-utils\nVersion: 0.0.3\nRequires-Python: >=3.6.2\nMaintainer-email: "Nanohmics Inc." <software.support@nanohmics.com>\nSummary: Collection of text and functional utilities\nLicense-File: LICENSE.txt\nClassifier: Programming Language :: Python\nClassifier: Topic :: Utilities\nClassifier: Programming Language :: Python :: 3\nClassifier: Intended Audience :: Developers\nClassifier: Operating System :: Microsoft :: Windows\nClassifier: License :: OSI Approved :: BSD License\nClassifier: Operating System :: POSIX :: Linux\nClassifier: Development Status :: 4 - Beta\nProvides-Extra: doc\nProvides-Extra: lint\nProvides-Extra: asy\nProvides-Extra: theme\nProvides-Extra: sphinx\nRequires-Dist: psutil>=5.9.0\nRequires-Dist: importlib_metadata; python_version < "3.8"\nRequires-Dist: wheel\nRequires-Dist: partis-pyproj==0.0.3\nRequires-Dist: partis-utils[sphinx]==0.0.3; extra == "doc"\nRequires-Dist: pyflakes==2.4.0; extra == "lint"\nRequires-Dist: typed-ast==1.5.4; extra == "lint" and python_version < "3.8"\nRequires-Dist: trio==0.19.0; extra == "asy" and python_version < "3.7"\nRequires-Dist: trio==0.20.0; extra == "asy" and python_version >= "3.7"\nRequires-Dist: pygments==2.9.0; extra == "theme"\nRequires-Dist: sphinx-paramlinks==0.5.2; extra == "sphinx"\nRequires-Dist: furo>=2022.1.2; extra == "sphinx"\nRequires-Dist: sphinxcontrib-bibtex>=2.4.1; extra == "sphinx"\nRequires-Dist: partis-pyproj==0.0.3; extra == "sphinx"\nRequires-Dist: sphinxcontrib-svg2pdfconverter[CairoSVG]==1.2.0; extra == "sphinx"\nRequires-Dist: sphinx-inline-tabs; extra == "sphinx"\nRequires-Dist: sphinx>=4.4.0; extra == "sphinx"\nRequires-Dist: sphinx-copybutton>=0.4.0; extra == "sphinx"\nRequires-Dist: pygments==2.9.0; extra == "sphinx"\nDescription-Content-Type: text/x-rst\n\nThe ``partis.utils`` package contains a collection of text and functional utilities.\n\nhttps://nanohmics.bitbucket.io/doc/partis/utils'

REQUIRES = b'psutil>=5.9.0\nimportlib_metadata; python_version < "3.8"\nwheel\npartis-pyproj==0.0.3\npartis-utils[sphinx]==0.0.3; extra == "doc"\npyflakes==2.4.0; extra == "lint"\ntyped-ast==1.5.4; extra == "lint" and python_version < "3.8"\ntrio==0.19.0; extra == "asy" and python_version < "3.7"\ntrio==0.20.0; extra == "asy" and python_version >= "3.7"\npygments==2.9.0; extra == "theme"\nsphinx-paramlinks==0.5.2; extra == "sphinx"\nfuro>=2022.1.2; extra == "sphinx"\nsphinxcontrib-bibtex>=2.4.1; extra == "sphinx"\npartis-pyproj==0.0.3; extra == "sphinx"\nsphinxcontrib-svg2pdfconverter[CairoSVG]==1.2.0; extra == "sphinx"\nsphinx-inline-tabs; extra == "sphinx"\nsphinx>=4.4.0; extra == "sphinx"\nsphinx-copybutton>=0.4.0; extra == "sphinx"\npygments==2.9.0; extra == "sphinx"'

SOURCES = b'partis_utils-0.0.3/src/utils/__init__.py\npartis_utils-0.0.3/src/utils/lint.py\npartis_utils-0.0.3/src/utils/valid.py\npartis_utils-0.0.3/src/utils/mem.py\npartis_utils-0.0.3/src/utils/module.py\npartis_utils-0.0.3/src/utils/file.py\npartis_utils-0.0.3/src/utils/hint.py\npartis_utils-0.0.3/src/utils/mutex_file.py\npartis_utils-0.0.3/src/utils/log.py\npartis_utils-0.0.3/src/utils/sphinx/__init__.py\npartis_utils-0.0.3/src/utils/sphinx/basic_main.py\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/README.md\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/package.json\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/tex-svg.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/adaptors/liteDOM.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/tex-mml-chtml.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/core.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/loader.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex-base.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/bbox.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/mhchem.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/setoptions.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/gensymb.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/upgreek.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/action.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/noundefined.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/colortbl.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/centernot.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/mathtools.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/extpfeil.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/color.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/braket.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/require.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/boldsymbol.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/autoload.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/tagformat.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/all-packages.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/colorv2.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/textmacros.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/noerrors.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/physics.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/configmacros.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/amscd.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/newcommand.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/ams.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/textcomp.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/html.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/verb.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/unicode.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/enclose.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/cancel.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex/extensions/bussproofs.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex-full.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/mml.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/mml/extensions/mml3.sef.json\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/mml/extensions/mml3.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/mml/entities.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/tex.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/input/asciimath.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/tex-chtml-full.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/startup.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/node-main.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/mml-chtml.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/tex-svg-full.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/a11y/semantic-enrich.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/a11y/assistive-mml.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/a11y/complexity.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/a11y/explorer.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/latest.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/sre/sre-node.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/sre/sre_browser.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/sre/mathmaps/en.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/sre/mathmaps/es.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/sre/mathmaps/it.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/sre/mathmaps/de.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/sre/mathmaps/fr.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/sre/mathmaps/hi.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/sre/mathmaps/nemeth.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/tex-chtml.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/output/svg.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/output/svg/fonts/tex.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/output/chtml.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/output/chtml/fonts/woff-v2/MathJax_Zero.woff\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/output/chtml/fonts/woff-v2/MathJax_Typewriter-Regular.woff\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/output/chtml/fonts/woff-v2/MathJax_SansSerif-Bold.woff\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/output/chtml/fonts/woff-v2/MathJax_Size1-Regular.woff\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/output/chtml/fonts/woff-v2/MathJax_AMS-Regular.woff\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/output/chtml/fonts/woff-v2/MathJax_Math-Italic.woff\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/output/chtml/fonts/woff-v2/MathJax_Vector-Bold.woff\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/output/chtml/fonts/woff-v2/MathJax_Main-Bold.woff\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/output/chtml/fonts/woff-v2/MathJax_Size2-Regular.woff\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/output/chtml/fonts/woff-v2/MathJax_Vector-Regular.woff\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/output/chtml/fonts/woff-v2/MathJax_Main-Italic.woff\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/output/chtml/fonts/woff-v2/MathJax_Math-BoldItalic.woff\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/output/chtml/fonts/woff-v2/MathJax_Math-Regular.woff\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/output/chtml/fonts/woff-v2/MathJax_SansSerif-Regular.woff\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/output/chtml/fonts/woff-v2/MathJax_Calligraphic-Regular.woff\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/output/chtml/fonts/woff-v2/MathJax_Calligraphic-Bold.woff\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/output/chtml/fonts/woff-v2/MathJax_SansSerif-Italic.woff\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/output/chtml/fonts/woff-v2/MathJax_Script-Regular.woff\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/output/chtml/fonts/woff-v2/MathJax_Fraktur-Regular.woff\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/output/chtml/fonts/woff-v2/MathJax_Main-Regular.woff\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/output/chtml/fonts/woff-v2/MathJax_Size3-Regular.woff\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/output/chtml/fonts/woff-v2/MathJax_Fraktur-Bold.woff\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/output/chtml/fonts/woff-v2/MathJax_Size4-Regular.woff\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/output/chtml/fonts/tex.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/mml-svg.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/tex-mml-svg.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/ui/safe.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/ui/lazy.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/es5/ui/menu.js\npartis_utils-0.0.3/src/utils/sphinx/_static/mathjax-3.2.0/LICENSE\npartis_utils-0.0.3/src/utils/sphinx/_static/tables.css\npartis_utils-0.0.3/src/utils/sphinx/_static/app_icon.svg\npartis_utils-0.0.3/src/utils/sphinx/ext.py\npartis_utils-0.0.3/src/utils/sphinx/basic_conf.py\npartis_utils-0.0.3/src/utils/fmt_doc.py\npartis_utils-0.0.3/src/utils/plugin.py\npartis_utils-0.0.3/src/utils/fmt.py\npartis_utils-0.0.3/src/utils/data.py\npartis_utils-0.0.3/src/utils/time.py\npartis_utils-0.0.3/src/utils/async_trio/__init__.py\npartis_utils-0.0.3/src/utils/async_trio/async_trio.py\npartis_utils-0.0.3/src/utils/venv.py\npartis_utils-0.0.3/src/utils/theme/pygments_light.py\npartis_utils-0.0.3/src/utils/theme/pygments_dark.py\npartis_utils-0.0.3/src/utils/special.py\npartis_utils-0.0.3/src/utils/inspect.py\npartis_utils-0.0.3/doc/conf.py\npartis_utils-0.0.3/doc/__init__.py\npartis_utils-0.0.3/doc/index.rst\npartis_utils-0.0.3/doc/src/partis.utils.valid.rst\npartis_utils-0.0.3/doc/src/partis.utils.log.rst\npartis_utils-0.0.3/doc/src/partis.utils.module.rst\npartis_utils-0.0.3/doc/src/partis.utils.fmt.rst\npartis_utils-0.0.3/doc/src/partis.utils.mem.rst\npartis_utils-0.0.3/doc/src/partis.utils.hint.rst\npartis_utils-0.0.3/doc/src/partis.utils.inspect.rst\npartis_utils-0.0.3/doc/src/partis.utils.mutex_file.rst\npartis_utils-0.0.3/doc/src/partis.utils.special.rst\npartis_utils-0.0.3/doc/src/partis.utils.plugin.rst\npartis_utils-0.0.3/doc/src/partis.utils.data.rst\npartis_utils-0.0.3/doc/src/partis.utils.venv.rst\npartis_utils-0.0.3/doc/__main__.py\npartis_utils-0.0.3/test/100_utils/__init__.py\npartis_utils-0.0.3/test/100_utils/test_fmt.py\npartis_utils-0.0.3/pyproject.toml\npartis_utils-0.0.3/LICENSE.txt\npartis_utils-0.0.3/README.rst'

TOP_LEVEL = b''

ENTRY_POINTS = b''

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

if __name__ == "__main__":
  exit( main() )
