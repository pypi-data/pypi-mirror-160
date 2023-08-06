
import sys
import types
import importlib

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class LazyModule ( types.ModuleType ):
  """A module that lazily imports sub-modules/packages
  """

  #-----------------------------------------------------------------------------
  def __init__( self, name ):
    super().__init__( name )

    self._p_children = list()

  #-----------------------------------------------------------------------------
  def define( self,
    children ):
    """
    Parameters
    ----------
    children : list<str>
      list of sub-modules/packages that should be importable
    """

    self._p_children = children

  #-----------------------------------------------------------------------------
  def __getattribute__( self, name ):

    try:
      return super().__getattribute__(name)

    except AttributeError as e:

      if name in self._p_children:
        child = importlib.import_module(f"{self.__name__}.{name}")
        setattr( self, name, child )
        return child

      raise AttributeError(
        f"'{type(self).__name__}' object has no attribute '{name}'") from e
