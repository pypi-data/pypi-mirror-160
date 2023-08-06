# -*- coding: UTF-8 -*-

import sys
import os
import gc
import inspect
import weakref
from inspect import getframeinfo, stack
import logging
import pprint
import traceback
import linecache
from copy import copy, deepcopy

from collections import OrderedDict as odict
from collections.abc import (
  Mapping,
  Sequence,
  Set,
  Iterable )

log = logging.getLogger(__name__)

from .valid import (
  valid_list,
  ensure_iterable,
  ensure_callable )

from .fmt import (
  fmt_src_line,
  split_lines,
  indent_lines,
  fmt_limit,
  fmt_obj )

from .special import NoType

try:
  from ruamel.yaml.comments import CommentedBase, CommentedMap, CommentedSeq

except ImportError:

  CommentedBase = NoType
  CommentedMap = NoType
  CommentedSeq = NoType


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
HINT_LEVELS = [
  ( 'notset',
    logging.NOTSET,
    """Any information""" ),
  ( 'trace',
    ( logging.NOTSET + logging.DEBUG ) // 2,
    """Internal program state information, such as values of variables.""" ),
  ( 'debug',
    logging.DEBUG,
    """Debugging information, typically of interest only when diagnosing problems.""" ),
  ( 'detail',
    ( logging.DEBUG + logging.INFO ) // 2,
    """Detailed information about the progress of an operation that a user may
    find informative, such as the intermediate results of a larger operation.""" ),
  ( 'info',
    logging.INFO,
    """Information about an operation being performed.""" ),
  ( 'warning',
    logging.WARNING,
    """Information of a result that is suspected to be invalid,
    but the expected progress of an operation was not interrupted.""" ),
  ( 'error',
    logging.ERROR,
    """Information of a result preventing the expected progress of an operation.""" ),
  ( 'critical',
    logging.CRITICAL,
    """An error occured that may prevent the program from continuing.""" ) ]

# sort by numeric levels to ensure proper order
HINT_LEVELS = sorted(
  HINT_LEVELS,
  key = lambda obj: obj[1] )

# cleanup description strings
HINT_LEVELS = [
  (str(k).upper().strip(), int(n), inspect.cleandoc(v) )
  for (k,n,v) in HINT_LEVELS ]

# mapping of level names to descriptions
HINT_LEVELS_NAME = [ k for (k,n,v) in HINT_LEVELS ]
HINT_LEVELS_DESC = odict( [ (k,v) for (k,n,v) in HINT_LEVELS ] )
HINT_LEVELS_TO_NUM = odict( [ (k,n) for (k,n,v) in HINT_LEVELS ] )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def hint_level_name( num ):
  """Returns the closest textual representation of a numeric level

  Parameters
  ----------
  num : int
    Level number in the range [0,50]

  Returns
  -------
  name : str
    One of the textual level names :data:`HINT_LEVELS <partis.utils.hint.HINT_LEVELS>`
    that has the highest numeric level that is <= ``num``.

  """

  try:
    # ensure level can be cast to an integer
    num = int(num)
  except Exception as e:
    raise ValueError(f"Level must be a number: {num}") from e

  # search starting with highest numeric level
  for (k,n,v) in HINT_LEVELS[::-1]:
    # find highest level name that is less-than or equal to given level number
    if n <= num:
      return k



#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def hint_level_num( name ):
  """Returns the closest textual representation of a numeric level

  Parameters
  ----------
  name : str | int
    One of the textual level names :data:`HINT_LEVELS <partis.utils.hint.HINT_LEVELS>`.

  Returns
  -------
  num : int
    Level number in the range [0,50]

  """

  if isinstance( name, int ):
    # convenience use to simply ensure a level number
    return name

  if not isinstance( name, str ):
    raise ValueError(f"Level name must be a string: {name}")

  # standardize name case
  name = name.upper().strip()

  if name not in HINT_LEVELS_NAME:
    raise ValueError(f"Level must be one of {HINT_LEVELS_NAME}: {name}")

  return HINT_LEVELS_TO_NUM[name]


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ModelHint:
  """Hint for diagnosing/resolving a given application model error

  Parameters
  ----------
  msg : str
    A message for the hint.
    The call will not happen until the message is required.
  loc : None | str
    Information on the location to which the hint corresponds.
  level : None | str | int
    Level of the model hint.
    Must be a value in :data:`HINT_LEVELS <partis.utils.hint.HINT_LEVELS>`.
    If given as an integer number, the level number of the hint will also have this value, but
    the name will be set from highest numeric level that is <= the given number.
    default: 'info'.
  hints : None | str | list< :py:class:` ModelHint <partis.utils.ModelHint` >
    Additional hints supporting this hint.
  width : None | int
    Maximum length of automatically formatted strings
  height : None | int
    Maximum height of automatically formatted strings
  with_stack : bool
    Include stack-trace of exceptions
  """
  #-----------------------------------------------------------------------------
  def __init__( self,
    msg = None,
    loc = None,
    level = None,
    hints = None,
    width = None,
    height = None,
    mark = None,
    with_stack = True ):

    # will determine this from level argument
    level_num = None

    if msg is None:
      msg = ""
    else:
      msg = str(msg)

      msg = inspect.cleandoc(msg)

    if loc is None:
      loc = ""
    else:
      loc = str(loc)

    hints = ensure_iterable( hints )

    hints = [
      self.cast(
        hint,
        width = width,
        height = height,
        mark = mark,
        with_stack = with_stack )
      for hint in hints
      if hint is not None ]

    if level is None:
      if hints:
        level_num = max( h.level_num for h in hints )
        level = hint_level_name( level_num )

      else:
        level = 'INFO'
        level_num = HINT_LEVELS_TO_NUM['INFO']

    else:
      # standardize level name/number
      if isinstance( level, str ):
        # convert to number, standardize name
        level = level.upper().strip()
        level_num = hint_level_num( level )


      else:
        # convert to name
        _level = hint_level_name( level )
        # NOTE: this does not alter the level number even if it is not one of the
        # pre-defined ones, allowing fine-grained numbers.
        # However, the name is still the nearest one less than given number
        # to be user-friendly
        # NOTE: casting after call to level_name, which will raise exception if
        # it couldn't be cast
        level_num = int(level)
        level = _level


    if mark is not None:
      mark = str(mark)

    self._msg = msg
    self._loc = loc
    self._level = level
    self._level_num = level_num
    self._hints = hints
    self._mark = mark

  #-----------------------------------------------------------------------------
  @property
  def msg( self ):
    return self._msg

  #-----------------------------------------------------------------------------
  @property
  def loc( self ):
    return self._loc

  #-----------------------------------------------------------------------------
  @property
  def level( self ):
    return self._level

  #-----------------------------------------------------------------------------
  @property
  def level_num( self ):
    return self._level_num

  #-----------------------------------------------------------------------------
  @property
  def hints( self ):
    return self._hints

  #-----------------------------------------------------------------------------
  def __str__( self ):
    try:
      return self.fmt()
    except:
      # this is a last restort, should only happend during a serious error
      return f"{type(self)} id({id(self)})"

  #-----------------------------------------------------------------------------
  def __repr__( self ):
    return str(self)

  #-----------------------------------------------------------------------------
  @staticmethod
  def filter( hint, level ):
    """Filter hint and all sub-hints to the given level or higher

    Parameters
    ----------
    level : str | int

    Returns
    -------
    hints : List[ hint ]
      List of hints filtered to the given level. If the root hint is above the `level`,
      it will be the only hint in the list. If it below `level`, but contains sub-hints
      >= `level` then the list will contain a collapse of all hints from the first
      recursive depth they occured. If all are < `level`, then an empy list is returned.
    """

    if isinstance( level, str ):
      level_num = hint_level_num( level )
    else:
      level_num = int( level )


    fltr_hints = list()

    for h in hint.hints:
      fltr_hints.extend( ModelHint.filter( hint = h, level = level_num ) )

    if hint_level_num(hint.level) >= level_num:

      return [ type(hint)(
        msg = hint.msg,
        loc = hint.loc,
        level = hint.level,
        hints = fltr_hints ), ]

    return fltr_hints

  #-----------------------------------------------------------------------------
  def fmt( self,
    level = 0,
    depth = 0,
    initdepth = None,
    maxdepth = None,
    mark = None,
    indent = 2,
    with_loc = True ):
    """Format hint to a string
    """

    if maxdepth is not None and maxdepth <= depth:
      return f"[max depth reached: {maxdepth}]"

    if mark is not None:
      _mark = mark

    elif self._mark is not None:
      _mark = self._mark

    else:
      _mark = "+ "

    if initdepth is None:
      initdepth = depth

    if isinstance( level, str ):
      level_num = hint_level_num( level )
    else:
      level_num = int( level )

    lines = list()
    next_depth = depth

    if self.level_num >= level_num and ( self.msg or ( with_loc and self.loc ) ):
      next_depth += indent

      if self.msg:
        lines.extend( split_lines(self.msg) )

      if with_loc and self.loc:
        lines.append( self.loc )

      lines = indent_lines(
        n = depth,
        lines = lines,
        mark = _mark )

    for hint in self.hints:
      line = hint.fmt(
        level = level_num,
        depth = next_depth,
        initdepth = initdepth,
        maxdepth = maxdepth,
        mark = mark,
        with_loc = with_loc )

      if isinstance( line, str ):
        if line:
          lines.append( line )
      else:
        lines.extend( line )


    if depth == initdepth:
      return "\n".join( lines )
    else:
      return lines

  #-----------------------------------------------------------------------------
  @classmethod
  def cast( cls,
    obj,
    width = None,
    height = None,
    mark = None,
    with_stack = True,
    level = None ):
    """Converts an object into an application model hint

    Parameters
    ----------
    obj : object
      Object to convert into a hint
    width : None | int
      Maximum length of automatically formatted strings
    height : None | int
      Maximum height of automatically formatted strings
    mark : None | str
    with_stack : bool
      Include stack-trace of exceptions
    level : None | str | int
      If given, the level to cast top-level hint.

    Returns
    -------
    ModelHint
    """

    level_num = None

    if level is not None:
      if isinstance( level, str ):
        level_num = hint_level_num( level )
      else:
        level_num = int( level )

    if isinstance( obj, ModelError ) or isinstance( obj, ModelHint ):
      if mark is None:
        mark = obj._mark

      if level_num is None:
        level_num = obj.level_num

    try:
      if isinstance( obj, BaseException ):

        if isinstance( obj, ModelError ):
          hint = cls(
            obj.msg,
            loc = obj.loc,
            level = level_num,
            mark = mark,
            # combine builtin hints and exception hints
            hints = obj.hints )

        else:
          # this is a regular exception
          _args = ", ".join([ str(arg) for arg in obj.args ])

          hint = cls(
            f"{obj.__class__.__name__}: { _args }",
            level = level_num if level_num is not None else 'error',
            mark = mark )

        if with_stack and obj.__traceback__ is not None:
          # extract traceback information, if available
          stack_width = width or 100
          stack_height = height or 1

          prev_hint = hint

          for frame, lineno in list( traceback.walk_tb( obj.__traceback__ ) )[::-1]:

            code = frame.f_code

            local_hints = list()

            if code.co_name != '<module>' and isinstance( frame.f_locals, dict ):
              # add local variable values, if not module level code

              for k, v in frame.f_locals.items():
                if v is not obj:

                  v = fmt_obj(
                    v,
                    width = stack_width,
                    height = stack_height )

                  local_hints.append( StackHint(
                    f"{k} = {v}",
                    level = 'trace',
                    mark = mark ) )

            sub_hints = list()

            if len(local_hints) > 0:
              sub_hints.append( StackHint(
                "Local variables",
                level = 'trace',
                hints = local_hints,
                mark = mark ) )

            sub_hints.append( StackHint(
              f"{os.path.basename(code.co_filename)}:{lineno} `{linecache.getline( code.co_filename, lineno ).strip()}`",
              level = 'trace',
              hints = prev_hint,
              mark = mark ) )

            prev_hint = StackHint(
              f"In function: `{code.co_name}`",
              loc = f"File \"{code.co_filename}\", line {lineno}",
              level = 'trace',
              mark = mark,
              hints = sub_hints )

          hint = prev_hint

        return hint

      if isinstance( obj, ModelHint ):
        # already a hint, but make a copy ensuring type and level are set

        return cls(
          obj.msg,
          loc = obj.loc,
          level = level_num,
          mark = mark,
          # combine builtin hints and exception hints
          hints = obj.hints )

      if isinstance( obj, Mapping ):

        return cls(
          msg = type(obj).__name__,
          level = level_num,
          hints = [ MappingHint(
            msg = f"{k}:",
            level = level_num,
            hints = [v],
            mark = mark,
            width = width,
            height = height )
            for k,v in obj.items() ] )

      if isinstance( obj, Sequence ) and not isinstance( obj, str ):

        return cls(
          msg = type(obj).__name__,
          level = level_num,
          hints = [ SequenceHint(
            msg = f"{i}:",
            level = level_num,
            hints = [v],
            mark = mark,
            width = width,
            height = height )
            for i,v in enumerate(obj) ] )

    except:
      log.exception(f"Failed to cast object to hint: {obj}", exc_info = True )

    # not a castable object type

    v = fmt_obj(
      obj,
      width = width,
      height = height )

    hint = cls(
      msg = v,
      level = level_num,
      mark = mark )

    return hint

  #-----------------------------------------------------------------------------
  def __getstate__(self):
    """Return state values to be pickled."""
    return {
      'msg' : self._msg,
      'loc' : self._loc,
      'level' : self._level,
      'hints' : [ h.__getstate__() for h in self._hints ] }

  #-----------------------------------------------------------------------------
  def __setstate__(self, state):
    """Restore state from the unpickled state values."""
    self.__init__( **state )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class MappingHint( ModelHint ):
  """Hints related to mappings
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SequenceHint( ModelHint ):
  """Hints related to sequences
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class StackHint( ModelHint ):
  """Hints related to exception stack-trace
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ModelError( ModelHint, Exception ):
  """General Model Error

  Parameters
  ----------
  msg : str
    A message for the hint.
    The call will not happen until the message is required.
  loc : None | str
    Information on the location to which the hint corresponds.
  level : None | str
    Level of the model hint.
    Must be a value in :py:data:`HINT_LEVELS <partis.utils.HINT_LEVELS>`.
    default: 'info'.
  hints : None | str | list< :py:class:` ModelHint <partis.utils.ModelHint` >
    Additional hints supporting this hint.
  """
  #-----------------------------------------------------------------------------
  def __init__( self,
    msg,
    loc = None,
    level = None,
    *args, **kwargs ):

    if level is None:
      level = 'error'

    ModelHint.__init__( self,
      msg = msg,
      loc = loc,
      level = level,
      *args, **kwargs )

    Exception.__init__( self, self.msg )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class ExternalModelError( ModelError ):
  """Error that indicates some error factor that, if changed, may not cause
  the same error to happen again.

  Parameters
  ----------
  msg : str | callable
    A message for the hint.
    If callable, the extra args and kwargs will be passed to the call, and must
    return a string for the message. The call will not happen until the message
    is required.
  loc : None | str | callable
    Information on the location to which the hint corresponds
    If callable, the extra args and kwargs will be passed to the call, and must
    return a string for the location. The call will not happen until the location
    is required.
  hints : None | list< :py:class:` ModelHint <partis.utils.ModelHint` >
    additional sub-hints supporting this hint
  """
  #-----------------------------------------------------------------------------
  def __init__( self,
    msg,
    loc = None,
    hints = None ):

    super().__init__(
      msg = msg,
      loc = loc,
      level = 'error',
      hints = hints )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class InternalModelError( ModelError ):
  """Error that indicates a bug in some model implementation

  Parameters
  ----------
  msg : str | callable
    A message for the hint.
    If callable, the extra args and kwargs will be passed to the call, and must
    return a string for the message. The call will not happen until the message
    is required.
  loc : None | str | callable
    Information on the location to which the hint corresponds
    If callable, the extra args and kwargs will be passed to the call, and must
    return a string for the location. The call will not happen until the location
    is required.
  hints : None | list< :py:class:` ModelHint <partis.utils.ModelHint` >
    additional sub-hints supporting this hint
  """
  #-----------------------------------------------------------------------------
  def __init__( self,
    msg,
    loc = None,
    hints = None ):

    super().__init__(
      msg = msg,
      loc = loc,
      level = 'error',
      hints = hints )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class CriticalModelError( ModelError ):
  """Error that indicates a bug in some model implementation

  Parameters
  ----------
  msg : str | callable
    A message for the hint.
    If callable, the extra args and kwargs will be passed to the call, and must
    return a string for the message. The call will not happen until the message
    is required.
  loc : None | str | callable
    Information on the location to which the hint corresponds
    If callable, the extra args and kwargs will be passed to the call, and must
    return a string for the location. The call will not happen until the location
    is required.
  hints : None | list< :py:class:` ModelHint <partis.utils.ModelHint` >
    additional sub-hints supporting this hint
  """
  #-----------------------------------------------------------------------------
  def __init__( self,
    msg,
    loc = None,
    hints = None ):

    super().__init__(
      msg = msg,
      loc = loc,
      level = 'critical',
      hints = hints )


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Loc:
  """Location information of source data from a parsed document

  Parameters
  ----------
  filename : str | None
    Filename of source document
  line : int | None
    Line number of source data in the document
  col : int | None
    Column number of source data in the document
  path : list[str] | None
    Path of source data in a hierarchical document
  """
  #-----------------------------------------------------------------------------
  def __init__( self,
    filename = None,
    line = None,
    col = None,
    path = None ):

    if filename is not None:
      filename = str(filename)

    if line is not None:
      line = int(line)

    if col is not None:
      col = int(col)

    if path is None:
      path = ['']

    if not ( isinstance( path, list ) and all( isinstance( s, str ) for s in path ) ):
      raise ValueError(
        f"`path` must be a list of strings: {path}")

    self._filename = filename
    self._line = line
    self._col = col
    self._path = path

    parts = list()

    _path = ".".join(self.path)

    if _path:
      parts.append( _path )

    if self.filename:
      parts.append( f"{self.filename}" )

    if self.line is not None:
      parts.append(f"line {self.line}")

    if self.col is not None:
      parts.append( f"col {self.col}" )

    self._str = ", ".join(parts)

  #-----------------------------------------------------------------------------
  @property
  def filename(self):
    """
    Returns
    -------
    filename : str | None
      Filename of source document
    """
    return self._filename

  #-----------------------------------------------------------------------------
  @property
  def line(self):
    """
    Returns
    -------
    line : int | None
      Line number of source data in the document
    """
    return self._line

  #-----------------------------------------------------------------------------
  @property
  def col(self):
    """
    Returns
    -------
    col : int | None
      Column number of source data in the document
    """
    return self._col

  #-----------------------------------------------------------------------------
  @property
  def path(self):
    """
    Returns
    -------
    path : list[str]
      Path of source data in a hierarchical document
    """
    return self._path

  #-----------------------------------------------------------------------------
  def __str__( self ):

    return self._str

  #-----------------------------------------------------------------------------
  def __repr__( self ):
    return self._str


  #-----------------------------------------------------------------------------
  def __call__( self,
    obj = None,
    key = None ):
    """Creates a new location in the same document

    Parameters
    ----------
    obj : CommentedBase | object | None
      Source data object.
    key : int | str | None
      Key/index for a mapping or sequence source data

    Returns
    -------
    loc : :class:`Loc <partis.schema_meta.base.Loc>`
    """

    _path = list(self.path)

    if key is not None:
      _path.append( str(key) )

    if isinstance( obj, CommentedBase ):
      # NOTE: ruamel appears to store line/col in zero-based indexing
      if (
        key is None
        or not ( isinstance(obj, CommentedMap) or isinstance(obj, CommentedSeq) )
        or obj.lc.data is None
        or (isinstance(obj, CommentedMap) and key not in obj)
        or (isinstance(obj, CommentedSeq) and ( key < 0 or key >= len(obj) ) ) ):

        return Loc(
          filename = self._filename,
          line = obj.lc.line + 1,
          col = obj.lc.col + 1,
          path = _path )

      else:
        return Loc(
          filename = self._filename,
          line = obj.lc.data[key][0] + 1,
          col = obj.lc.data[key][1] + 1,
          path = _path )

    return Loc(
      filename = self._filename,
      line = self._line,
      col = self._col,
      path = _path )
