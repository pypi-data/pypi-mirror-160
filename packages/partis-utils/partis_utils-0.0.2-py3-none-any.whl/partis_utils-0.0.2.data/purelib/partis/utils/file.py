import os
from glob import glob
import hashlib
import pathlib

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def head( path, n, bufsize = 1024, encoding = 'utf-8' ):
  """Reads the first n lines from a file

  Parameters
  ----------
  path : str
  n : int
    Max number of lines to read from the beginning of the file
  bufsize : int
    Number of bytes to buffer at a time.

  Returns
  -------
  lines : List[str]
    Up to ``n`` lines from the beginning of the file
  """

  bufsize = int(bufsize)
  bufsize = max(1, bufsize)

  n = int(n)
  n = max( 0, n )

  buf = bytes()
  nlines = 0

  head = 0

  with open( path, 'rb' ) as fp:
    # total number of bytes in the file
    tot = fp.seek( 0, os.SEEK_END )

    # start at beginning
    head = 0

    while nlines < n and head < tot:
      # NOTE: the number of newline characters is one less than number of 'lines'
      nread = min( tot - head, bufsize )

      fp.seek( head, os.SEEK_SET )

      _buf = fp.read( nread )

      head += nread

      nlines += _buf.count(b'\n')

      buf = _buf + buf

  if nlines > 0 and head < tot:
    # remove everything after last newline to ensure only complete lines are kept
    i = buf.rindex(b'\n')
    buf = buf[:i]

  res = buf.decode(encoding, errors = 'replace')
  lines = res.split('\n')[:n]

  return lines

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def tail( path, n, bufsize = 1024, encoding = 'utf-8' ):
  """Reads the last n lines from a file

  Parameters
  ----------
  path : str
  n : int
    Max number of lines to read from the end of the file
  bufsize : int
    Number of bytes to buffer at a time.

  Returns
  -------
  lines : List[str]
    Up to ``n`` lines from the end of the file
  """

  bufsize = int(bufsize)
  bufsize = max(1, bufsize)

  n = int(n)
  n = max( 0, n )

  buf = bytes()
  nlines = 0

  head = 0

  with open( path, 'rb' ) as fp:
    # total number of bytes in the file
    tot = fp.seek( 0, os.SEEK_END )

    head = tot

    while nlines < n and head > 0:
      # NOTE: the number of newline characters is one less than number of 'lines'
      nread = min( head, bufsize )
      head -= nread

      fp.seek( head, os.SEEK_SET )

      _buf = fp.read( nread )

      nlines += _buf.count(b'\n')

      buf = _buf + buf

  if nlines > 0 and head > 0:
    # remove everything before first newline to ensure only complete lines are kept
    i = buf.index(b'\n')
    buf = buf[(i+1):]

  res = buf.decode(encoding, errors = 'replace')
  lines = res.split('\n')[-n:]

  return lines

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def checksum(
  path,
  algorithm = "sha1",
  bufsize = 2**24 ):
  """
  Parameters
  ----------
  path : str
  algorithm : str
    Hash algorithm to use. ('sha1', 'md5'). See hashlib.algorithms_available
  bufsize : int
    Number of bytes to buffer at a time.

  Returns
  -------
  hash : str
    Hexadecimal formatted hash of file `size` bytes.
  """

  if algorithm not in hashlib.algorithms_available:
    raise ValueError(f"Checksum algorithm must be one of {hashlib.algorithms_available}: {algorithm}")

  if not os.path.exists( path ):
    raise ValueError(f"File must exist: {path}")

  hasher = getattr( hashlib, algorithm )()

  with open( path, 'rb' ) as fp:
    bytes = fp.read( bufsize )

    while len(bytes) > 0:
      hasher.update( bytes )
      bytes = fp.read( bufsize )

  checksum = hasher.hexdigest()

  return checksum

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def copytree( src, dst, exclude = None ):
  """Recursivly copies a directory tree

  This differs from the shutil.copytree in that this can be used to copy into
  a sub-directory of the directory being copied. The destination directory, and
  anything already copied into it, will be ignored as the remainder of the source
  directory is copied into it.
  """

  if exclude is None:
    exclude = list()

  if not isinstance( exclude, list ):
    exclude = [ exclude, ]

  src = os.path.abspath( src )
  dst = os.path.abspath( dst )

  exclude.append( dst )

  topfiles = os.listdir( src )

  if os.path.exists( dst ):
    os.rmtree( dst )

  os.makedirs( dst )

  for file in topfiles:

    _src = os.path.join( src, file )

    if _src in exclude:
      continue

    _dst = os.path.join( dst, file )

    if os.path.isdir( _src ):
      copytree(
        src = _src,
        dst = _dst,
        exclude = exclude )

    else:
      shutil.copy2( _src, _dst )
