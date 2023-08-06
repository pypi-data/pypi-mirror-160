import importlib
import inspect
import sys
import dis


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def get_assigned_name(frame, sep = '_'):
  """Gets the variable name(s) assigned by the return value of the function

  This should be called with the previous frame that called the function.
  The assigned name is determined by dissasembling the code of the given frame,
  starting at the last executed instruction, and looking forward until the return
  value can be traced to being stored in the first 'permanent' variable,
  or discarded if it is never assigned.
  If the return value is used as an argument to another function, the new return
  value of the function is then traced instead.
  Assignment to keyword arguments are tracked, but do not terminate the tracing.
  For example, the following should print ``a_x_y_z``, concatenting the names
  assigned to the return value of ``f()`` up to where the result is assigned to ``a``,
  including intermediate assignment to keyword arguments ``x``, ``y``, and ``z``.
  However, the eventual name is available within ``f()`` before it actually
  returns.

  .. code-block:: python

    def f():
      import inspect
      from partis.utils.inspect import get_assigned_name
      return get_assigned_name( inspect.currentframe().f_back )

    def g( x = None, y = None, z = None ):
      return x or y or z

    a = g(
      x = g(
        y = g(
          z = f() ) ) )

    print(a)

  .. note::

    This function's behaviour is **not defined in all cases**.
    Since this uses static analysis to look forward in the code, it is in general
    not possible to know the assigned name without actually running the
    program.
    It will also not handle more complicated intermediate expressions that
    reinterpret the return value such as un-packing, comprehensions, etc.

  Adapted from: https://stackoverflow.com/a/41586688/14845092
  """

  try:

    # track a list of names to which the returned object is assigned
    obj_tracer = list()

    stack = list()

    for instr in dis.get_instructions(frame.f_code):

      opname = instr.opname
      val = instr.argval

      if opname.startswith('CALL_FUNCTION'):

        if opname == 'CALL_FUNCTION':
          n = val + 1

        elif opname == 'CALL_FUNCTION_KW':

          n = val + 2

          _args = stack[-n+1:-1][::-1]
          _kw = stack[-1][::-1]

          if obj_tracer in _args:
            # extract the name of the keyword that references the object and
            # add to the list of names
            idx = _args.index(obj_tracer)

            obj_tracer.append(_kw[idx])

        res = obj_tracer if ( instr.offset == frame.f_lasti or any(v is obj_tracer for v in stack[-n:]) ) else ''
        stack = stack[:-n]
        stack.append(res)

        # continue down a chain of function calls, since keyword arguments are
        # only temporary storage.

      elif opname in [
        # (co_varnames)
        'STORE_FAST',
        # (co_names)
        'STORE_GLOBAL',
        'STORE_NAME',
        # (co_cellvars++co_freevars)
        'STORE_DEREF' ]:

        res = stack.pop()

        if res is obj_tracer:
          obj_tracer.append(val)

          # terminate when stored into a variable
          break

      elif opname in [
        'STORE_ATTR']:

        if stack[-1] is obj_tracer:
          obj_tracer.append(val)

        attr = stack.pop()
        res = stack.pop()

        if res is obj_tracer:
          obj_tracer.append(val)
          obj_tracer.append(attr)

          # terminate when stored into a variable
          break

      elif opname in [
        'STORE_ANNOTATION',
        'RETURN_VALUE' ]:

        stack.pop()

      elif opname in [
        # (co_varnames)
        'LOAD_FAST',
        # (co_names)
        'LOAD_GLOBAL',
        'LOAD_NAME',
        # (co_consts)
        'LOAD_CONST',
        # (co_cellvars++co_freevars)
        'LOAD_DEREF',
        'IMPORT_FROM' ]:

        # usually objects onto which an attribute is assigned, by convention
        # the object name should go first
        stack.append(val)

      elif opname in [
        'LOAD_ATTR']:

        # objects onto which an attribute is assigned, by convention
        # the object name should go first
        stack.append( stack.pop() + sep + val )

      elif opname == 'IMPORT_NAME':
        stack.pop()
        stack.pop()
        stack.append(val)

      elif opname in [
        'GET_LEN' ]:

        stack.push(stack[-1])

      elif opname in [
        'BUILD_TUPLE',
        'BUILD_LIST',
        'BUILD_SET',
        'BUILD_STRING' ]:

        items = stack[-val:]
        stack = stack[:-val]
        stack.append(items)

      elif opname == 'BUILD_MAP':
        items = stack[-2*val:]
        stack = stack[:-2*val]
        stack.append(items)

      elif opname == 'BUILD_CONST_KEY_MAP':
        keys = stack.pop()
        values = stack[-val:]
        stack = stack[:-val]
        stack.append(keys + items)

      elif opname == 'POP_TOP':
        res = stack.pop()

        if res is obj_tracer:
          # terminate when discarded
          break


      else:
        pass

    # reverse order
    return sep.join([ name for name in obj_tracer[::-1] if name ])

  except Exception as e:
    # import traceback as tb
    # tb.print_exc()
    pass

  return None


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def caller_module( depth = 1 ):
  """Obtains the module of the caller

  Returns
  -------
  module : ModuleType

  """
  frame = inspect.currentframe().f_back

  for i in range(depth):
    frame = frame.f_back

  module_name = None
  module = None

  try:

    if "__module__" in frame.f_locals:
      module_name = frame.f_locals["__module__"]

    elif "__name__" in frame.f_globals:
      module_name = frame.f_globals["__name__"]

    if module_name is None:
      raise ValueError(f"Caller module name not found")

    module = importlib.import_module( module_name )

  finally:
    del frame

  return module

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def caller_class_var( depth = 1 ):
  """Obtain the class name and class variable of function called within a class
  constructor namespace.

  Returns
  -------
  clsname : None | str
    Class '__qualname__'
  varname : None | str
  """

  clsname = None
  varname = None

  frame = inspect.currentframe().f_back

  for i in range(depth):
    frame = frame.f_back

  try:
    info = inspect.getframeinfo(frame)

    if '__qualname__' in frame.f_locals:

      if frame.f_locals['__qualname__'].split('.')[-1] == info.function:
        clsname = frame.f_locals['__qualname__']

    varname = get_assigned_name(frame)

  finally:
    del frame

  return clsname, varname


#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def make_dynamic_class_name(*,
  default_name,
  module = None,
  name = None,
  depth = 1 ):

  if module is None:
    module = caller_module(
      depth = depth + 1 )

  if isinstance( module, str ):
    module = importlib.import_module( module )

  if name is None:
    clsname, varname = caller_class_var(
      depth = depth + 1 )

    if clsname and varname:
      name = f'{clsname}_{varname}'

    elif varname:
      name = f'{varname}'

    elif clsname:
      name = f'{clsname}_{default_name}'

    else:
      name = default_name

  _name = name
  _idx = 1

  while hasattr( module, _name ):
    _name = name + f'_{_idx}'
    _idx += 1

  name = _name

  return module, name
