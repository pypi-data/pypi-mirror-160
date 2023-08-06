from docutils import nodes
from docutils.parsers.rst import directives
from sphinx import addnodes
from sphinx.domains.python import(
  PyAttribute )

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class PartisAttribute( PyAttribute ):
  option_spec = PyAttribute.option_spec.copy()
  option_spec.update({
    'prefix': directives.unchanged })

  #-----------------------------------------------------------------------------
  def get_signature_prefix(self, sig):
    prefix = []

    text = self.options.get('prefix')

    if text:
      parts = [ p.strip() for p in text.split(' ') ]

      for p in parts:
        prefix.append(nodes.Text(p))
        prefix.append(addnodes.desc_sig_space())

    return prefix

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def setup(app):

  app.add_directive('partis_attr', PartisAttribute)
