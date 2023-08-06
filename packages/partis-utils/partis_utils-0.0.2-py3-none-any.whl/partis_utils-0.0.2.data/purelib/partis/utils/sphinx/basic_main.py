# -*- coding: utf-8 -*-
"""CLI for running sphinx-build

.. code-block:: bash

  python -m doc -b html latexpdf

"""

import sys
import os
import os.path as osp
import re
import subprocess
import argparse
from argparse import RawTextHelpFormatter

from partis.pyproj import (
  norm_dist_name,
  join_dist_filename,
  dist_targz )

from partis.utils import caller_module

try:
  from importlib.metadata import metadata

except ImportError:
  from importlib_metadata import metadata


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def basic_main(
  package,
  conf_dir,
  src_dir,
  root_dir ):
  """Convenience implementation of the ``__main__`` to build documentation and
  distribution file.


  Parameters
  ----------
  package : str
    Name of installed package to build documentation
  conf_dir : str
    Directory where conf.py is located
  src_dir : str
    Directory where 'index' document is located
  root_dir : str
    Directory for root project

  Returns
  -------
  int
    returncode

  Example
  -------

  .. code-block:: python

  from partis.utils.sphinx import basic_main

  if __name__ == "__main__":

    conf_dir = osp.abspath( osp.dirname(__file__) )
    root_dir = osp.abspath( osp.join( conf_dir, os.pardir ) )

    basic_main(
      package = 'partis',
      conf_dir = conf_dir,
      src_dir = root_dir,
      root_dir = root_dir )

  """

  meta = metadata( package )

  project = meta['Name']
  project_normed = norm_dist_name( project )

  version = meta['Version']

  dist_name = join_dist_filename( [project_normed, version] )
  doc_dist_name = dist_name + '-doc'
  doc_dist_file = doc_dist_name + '.tar.gz'

  parser = argparse.ArgumentParser(
    description = __doc__,
    formatter_class = RawTextHelpFormatter )

  parser.add_argument( "-b", "--builder",
    type = str,
    nargs = '+',
    default = [ 'html' ],
    help = "builder to use passed to sphinx-build `-b` option. "
      "May give multiple builders to run in series." )

  parser.add_argument( "-o", "--outdir",
    type = str,
    default = None,
    help = "Output directory" )

  parser.add_argument( "--no-dist",
    action = 'store_true',
    help = f"Do not create a documentation distribution: {doc_dist_file}" )

  args = parser.parse_args()


  outdir = args.outdir

  if not outdir:
    outdir = osp.join( root_dir, 'dist' )

  build_dir = osp.join( root_dir, 'build' )

  if not osp.exists( outdir ):
    os.makedirs( outdir )

  if not osp.exists( build_dir ):
    os.makedirs( build_dir )

  doctrees = osp.join( build_dir, '.doctrees' )


  #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  builds = list()

  for builder in args.builder:
    builder_dir = osp.join( build_dir, builder )
    builds.append( (builder, builder_dir) )

    subprocess.check_call([
      'python3',
      '-m',
      'sphinx.cmd.build',
      '-M',
      builder,
      src_dir,
      build_dir,
      '-c',
      conf_dir ])

  #+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
  if not args.no_dist:

    print(f'Packaging documentation: {doc_dist_file}')

    with dist_targz(
      outname = doc_dist_file,
      outdir = outdir ) as dist:

      for builder, builder_dir in builds:
        if builder == 'latexpdf':
          # only copy in the generated pdf
          pdf_name = dist_name + '.pdf'

          dist.copyfile(
            src = osp.join( build_dir, 'latex', pdf_name ),
            dst = '/'.join([ doc_dist_name, pdf_name ]) )

        else:
          dist.copytree(
            src = builder_dir,
            dst = osp.join( doc_dist_name, builder ) )

  return 0
