import sys

from .fmt import (
  indent_lines,
  line_segment )

from .hint import (
  Loc,
  ModelHint )

from pyflakes import (
  checker )

Checker = checker.Checker

if sys.version_info >= (3, 8):
  import ast

else:
  from typed_ast import ast3 as ast
  checker.ast = ast
  checker.FOR_TYPES = tuple([getattr(ast, k.__name__) for k in checker.FOR_TYPES])

  Checker._ast_node_scope = {
    getattr(ast, k.__name__) : v
    for k,v in Checker._ast_node_scope.items() }

from pyflakes.messages import (
  UndefinedName,
  UnusedImport,
  UnusedVariable )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def check_attrs( obj, name ):
  attrs = name.split('.')

  _obj = obj

  for i, attr in enumerate(attrs):
    try:
      _obj = getattr( _obj, attr )

    except AttributeError as e:
      return '.'.join(attrs[:i]), '.'.join(attrs[i:])

  return name, ''

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def lint_python( src, locals, embed_func ):
  hints = list()

  src_lines = src.splitlines()

  if embed_func:
    fsrc = "def func():\n  __noop__ = 0\n{}".format(indent_lines(2, src))
    ix = 2
    iy = 2
  else:
    fsrc = src
    ix = 0
    iy = 0

  filename = ''

  try:

    tree = ast.parse(fsrc, filename = filename)

  except SyntaxError as e:

    lineno = e.lineno - iy
    col = e.offset - ix

    idx = lineno - 1
    offset = col - 1

    loc = Loc( line = lineno, col = col )

    line = src_lines[idx]

    hints.append( ModelHint(
      e.msg,
      loc = loc,
      level = 'error',
      hints = [
        line,
        ' '*offset + '^' + ' '*(len(line) - offset - 1 ) ] ) )

  else:

    file_tokens = checker.make_tokens(fsrc)
    w = Checker(tree, file_tokens=file_tokens, filename=filename)
    w.messages.sort(key=lambda m: m.lineno)

    for m in w.messages:
      if m.lineno - iy <= 0:
        # likely disliked '__noop__' in wrapping code being un-used
        continue

      message = m.message
      message_args = m.message_args

      lineno = m.lineno - iy
      col = m.col - ix

      idx = lineno - 1
      offset = col

      line = src_lines[idx]

      if type(m) in [ UnusedImport, UnusedVariable ]:
        level = 'warning'
      else:
        level = 'error'

      if isinstance( m, UndefinedName ) and locals:

        name = m.message_args[0]

        _, _name = line_segment(
          text = line,
          sep = r"[^a-zA-Z0-9_\.]",
          offset = offset )

        contains, missing = check_attrs( locals, _name )

        if not missing:
          continue

        if contains:
          offset += len(contains)
          level = 'warning'
          message = "unknown attribute '%s' of name '%s'"
          message_args = (missing, contains)

      msg = message % message_args

      loc = Loc( line = lineno, col = offset + 1 )

      hints.append( ModelHint(
        msg,
        loc = loc,
        level = level,
        hints = [
          line,
          ' '*offset + '^' + ' '*(len(line) - offset - 1 ) ] ) )

  return hints
