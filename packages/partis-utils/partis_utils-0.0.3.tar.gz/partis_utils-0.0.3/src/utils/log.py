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
import threading
from types import MethodType
from copy import copy, deepcopy

from collections import OrderedDict as odict

log = logging.getLogger(__name__)

from .fmt import (
  f )

from .hint import (
  HINT_LEVELS,
  HINT_LEVELS_TO_NUM,
  hint_level_num,
  hint_level_name,
  ModelHint )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
log_levels = HINT_LEVELS_TO_NUM

# levels which are not defined in base logging module
custom_log_levels = [
  (k,n,v)
  for (k,n,v) in HINT_LEVELS
  if not hasattr( logging, k ) ]

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def add_log_level( logger, num, name ):
  """Add custom logging level to a logger
  """
  # uname = name.upper()
  name = name.lower()

  if hasattr(logger, name):
    # assumes that if the name is defined, level is already defined
    raise ValueError(f'Logging name conflict: {name}')

  # This method was inspired by the answers to Stack Overflow post
  # http://stackoverflow.com/q/2183233/2988730, especially
  # http://stackoverflow.com/a/13638084/2988730
  def log_for_level( self, message, *args, **kwargs):
    if self.isEnabledFor( num ):
      self._log( num, message, args, **kwargs )

  setattr( logger, name, MethodType( log_for_level, logger ) )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def getLogger( name = None ):
  """Get a named logger augmented with custom logging levels.

  Note
  ----
  This will not augment the root logger to avoid interfering with other packages
  """

  if name in getLogger.loggers:
    return getLogger.loggers[name]

  logger = logging.getLogger( name )

  if name is None:
    # NOTE: avoid polluting root logger namespace
    return logger

  for name, num, v in custom_log_levels:
    add_log_level( logger, num, name )

  getLogger.loggers[name] = logger

  return logger

getLogger.loggers = dict()


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def init_logging(
  level,
  rank = None,
  filename = None ):

  # adapted from logging/__init__.py

  _lock = threading.RLock()

  if _lock:
    _lock.acquire()

  try:

    # make sure custom hint levels are defined in loggers
    for name, num, v in custom_log_levels:
      logging.addLevelName( num, name.upper() )

    if isinstance( level, str ):
      log_level = hint_level_num( level )

    else:
      try:
        log_level = int( level )
      except:
        raise ValueError(
          f"Log verbosity must be string or integer {log_levels}: {level}")

    if log_level < logging.INFO:
      if rank is None:
        format = "{name}:{levelname}: {message}"
      else:
        format = "%d:{name}:{levelname}: {message}" % rank
    else:
      format = "{message}"

    if filename and os.path.exists(filename):
      os.remove( filename )

    root = logging.getLogger()

    for h in root.handlers[:]:
      root.removeHandler(h)
      h.close()

    fmt = HintFormatter(
      # level is needed here also to filter level nested hints
      level = log_level,
      fmt = format,
      style = '{' )

    handlers = list()

    h_stdout = logging.StreamHandler(
      stream = sys.stdout )

    h_stdout.setFormatter( fmt )
    handlers.append( h_stdout )

    # from rich.logging import RichHandler

    # h_stdout = RichHandler(
    #   show_level = False,
    #   show_time = False,
    #   show_path = False,
    #   rich_tracebacks = True )
    #
    # h_stdout.setFormatter( HintFormatter(
    #   # level is needed here also to filter level nested hints
    #   level = log_level,
    #   fmt = format,
    #   style = '{' ) )
    #
    # handlers.append( h_stdout )

    if filename:
      h_file = logging.FileHandler(
        filename,
        mode = 'a',
        encoding = 'ascii',
        errors = 'backslashreplace' )

      h_file.setFormatter( fmt )

      handlers.append( h_file )


    for h in handlers:

      root.addHandler( h )

    root.setLevel( log_level )

    logging.captureWarnings(True)

    logging.info( f"Initialized logging: {log_level}" )

  finally:
    if _lock:
      _lock.release()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def record_to_hint( record ):
  """converts a logging record msg to be a ModelHint
  """

  hints = list()

  if record.exc_info is not None:
    _type, _value, _traceback = record.exc_info

    hints.append( ModelHint.cast( _value ) )

  msg = record.msg

  if not isinstance( msg, ModelHint ):
    hint = ModelHint(
      msg,
      loc = record.name,
      level = hint_level_name(record.levelno),
      hints = hints )

  else:
    hint = type(msg)(
      msg = msg.msg,
      # NOTE: this overwrites the level of the original hint to be that was logged
      level = max( msg.level_num, record.levelno ),
      loc = msg.loc if msg.loc != '' else record.name,
      hints = msg.hints + hints )

  return hint

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class LogListHandler( logging.Handler ):
  """Collects log records in local list of hints

  Parameters
  ----------
  level : int
    The level enabled for the handler
  **kwargs :
    Keyword arguments passed to the ModelHint when casting
  """
  #-----------------------------------------------------------------------------
  def __init__(self, level = logging.NOTSET ):
    super().__init__( level )

    self._hints = list()
    self._logs = list()

  #-----------------------------------------------------------------------------
  @property
  def hints(self):
    return self._hints

  #-----------------------------------------------------------------------------
  @property
  def logs(self):
    return self._logs

  #-----------------------------------------------------------------------------
  def clear( self ):
    self.hints.clear()
    self.logs.clear()

  #-----------------------------------------------------------------------------
  def emit( self, record ):

    hint = record_to_hint( record )

    self._hints.append( hint )

    self._logs.append( hint.__getstate__() )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class LogChannelHandler( logging.Handler ):
  """Collects log records in local list

  Parameters
  ----------
  send_channel : SendChannel
  level : int
    The level enabled for the handler
  **kwargs :
    Keyword arguments passed to the ModelHint when casting
  """
  #-----------------------------------------------------------------------------
  def __init__(self, send_channel, level = logging.NOTSET, **kwargs ):
    super().__init__( level )

    self._send_channel = send_channel
    self._kwargs = kwargs

  #-----------------------------------------------------------------------------
  def emit(self, record):

    exc_info = None

    if record.exc_info is not None:
      type, value, traceback = record.exc_info

      exc_info = ModelHint.cast( value, **self._kwargs ).__getstate__()

    send_channel.send( dict(
      msg = record.msg,
      level = record.levelname,
      exc_info = exc_info ) )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class HintFormatter( logging.Formatter ):
  #-----------------------------------------------------------------------------
  def __init__( self, level, *args, **kwargs ):
    super().__init__( *args, **kwargs )

    self._level_num = hint_level_num( level )

  #-----------------------------------------------------------------------------
  def format( self, record ):
    if not isinstance( record.msg, ModelHint ):
      return super().format( record )

    hint = record.msg
    record.msg = ""

    base = super().format( record )

    fhint = hint.fmt(
      level = self._level_num )

    return base + fhint
