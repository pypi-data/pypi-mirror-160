from sphinx.util.docutils import SphinxDirective
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.writers.html import HTMLTranslator

from .common import (
    BaseNode,
    add_role_and_directive,
    add_visit_depart,
)

TAG = 'pre'

class preformatted_node(BaseNode): pass

def setup_preformatted(app):
    app.add_node(preformatted_node)
    add_role_and_directive(app, preformatted_node, 'preformatted')
    add_role_and_directive(app, preformatted_node, 'pre')

class PreformattedTranslator(HTMLTranslator):
    pass

add_visit_depart(PreformattedTranslator, preformatted_node.__name__, TAG)