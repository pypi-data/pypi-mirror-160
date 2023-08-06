import inspect
from collections.abc import (
  Mapping,
  Sequence )

import trio

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
async def aval( val, *args, **kwargs ):
  """Returns a value from plain data, callable, or coroutine
  """

  if callable( val ):
    val = val( *args, **kwargs )

  if inspect.isawaitable( val ):
    val = await val

  return val

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class AsyncTarget:
  """Provides an asynchronous return value using an event driven callback
  """

  #-----------------------------------------------------------------------------
  def __init__( self, t = 0.25 ):
    self._t = t
    self._noval = object()
    self._result = self._noval
    self._error = self._noval

  #-----------------------------------------------------------------------------
  def on_result( self, result = None ):
    self._result = result

  #-----------------------------------------------------------------------------
  def on_error( self, error = None ):
    self._error = error

  #-----------------------------------------------------------------------------
  async def wait( self ):
    while self._result is self._noval and self._error is self._noval:
      await trio.sleep( self._t )

    if self._result is self._noval:
      self._result = None

    if self._error is self._noval:
      self._error = None

    return self._result, self._error

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TrioFuture:
  """Wrapping class to store the result of running an awaitable
  """

  #-----------------------------------------------------------------------------
  def __init__( self, f ):
    self._f = f
    self._res = None
    self._exc = None
    self._nursery = None

  #-----------------------------------------------------------------------------
  async def run( self,
    nursery,
    re_raise = True,
    cancel_on_complete = False ):
    """Runs the awaitable within a given nursery
    """
    self._nursery = nursery

    try:
      self._res = await self._f

      if cancel_on_complete:
        nursery.cancel()

    except Exception as e:
      self._exc = e

      if re_raise:
        raise

  #-----------------------------------------------------------------------------
  @property
  def result( self ):
    if self._exc is not None:
      raise self._exc

    return self._res

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
async def wait_all( awaitables ):
  """Runs and waits for all awaitables to complete, returning the result

  An exception is raised if any awaitable raises an exception.

  Parameters
  ----------
  awaitables : Sequence[ awaitable ] | Mapping[ object, awaitable ]
    Sequence or mapping of awaitables to run.

  Returns
  -------
  results : Sequece | Mapping
    Result of each awaitable in the original sequence or mapping
  """

  if isinstance( awaitables, Mapping ):
    futures = [ ( k, TrioFuture(f) ) for k, f in awaitables.items() ]

    async with trio.open_nursery() as nursery:

      for k, f in futures:
        nursery.start_soon( f.run, nursery )

    return type(awaitables)( [ ( k, f.result ) for k, f in futures ] )

  if isinstance( awaitables, Sequence ):
    futures = [ TrioFuture(f) for f in awaitables ]

    async with trio.open_nursery() as nursery:

      for f in futures:
        nursery.start_soon( f.run, nursery )

    return [ f.result for f in futures ]
