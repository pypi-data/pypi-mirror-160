import time
import decimal

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class TimerMono:
  """A monotonic time that uses the system set time as the reference point,
  including time elapsed during sleep.
  """

  #-----------------------------------------------------------------------------
  def __init__( self, timer = None, prec = None ):

    if timer is None:
      timer = time.perf_counter

    self._timer = timer

    self._time_abs = time.time()
    self._time_rel = self._timer()
    self._ctx = decimal.Context( prec = prec )
    self._prev_ctx = None

  #-----------------------------------------------------------------------------
  def __call__( self ):
    with self as ctx:
      return (
        ctx.create_decimal(self._time_abs)
        + ctx.create_decimal(self._timer() - self._time_rel) )

  #-----------------------------------------------------------------------------
  def create( self, *args ):
    with self as ctx:
      return sum([
        ctx.create_decimal(x)
        for x in args ])

  #-----------------------------------------------------------------------------
  def __enter__(self):
    self._prev_ctx = decimal.getcontext()
    decimal.setcontext(self._ctx)

    return self._ctx

  #-----------------------------------------------------------------------------
  def __exit__(self, type, value, traceback):

    decimal.setcontext(self._prev_ctx)
    self._prev_ctx = None

    # do not handle any other exceptions here
    return False

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
timer = TimerMono( prec = 32 )
