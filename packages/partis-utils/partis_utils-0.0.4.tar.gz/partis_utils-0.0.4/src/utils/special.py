
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class NoType:
  """Class indicating a type which no class is a sub-class
  """
  pass

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class SpecialType:
  """Base class for special values
  """

  #-----------------------------------------------------------------------------
  def __str__( self ):
    return self.__class__.__name__[:-4]

  #-----------------------------------------------------------------------------
  def __hash__( self ):
    return hash(str(self))

  #-----------------------------------------------------------------------------
  def __eq__( self, other ):
    return type(self) == type(other)

  #-----------------------------------------------------------------------------
  def __ne__( self, other ):
    return type(self) != type(other)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class NotSetType( SpecialType ):
  """Marks a value that is not set, or otherwise undefined.

  Note
  ----
  This is intended as an alternative to using ``None`` to distinguish parameter
  values that where never specified from ones that have a specified value of ``None``,
  but may often be set by methods that assume that ``None`` is intended to be
  used as the 'Not Set' value.
  """
  pass

notset = NotSetType()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class RequiredType( SpecialType ):
  """Marks a parameter that is required, without a default value, and must not
  be None or otherwise undefined.
  """
  pass

required = RequiredType()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class OptionalType( SpecialType ):
  """Marks a parameter that is optional, without a default value, but may be None.
  """
  pass

optional = OptionalType()

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class DerivedType( SpecialType ):
  """Marks a parameter that is derived, without a default value, but will be
  constructed from other value(s).
  """
  pass

derived = DerivedType()
