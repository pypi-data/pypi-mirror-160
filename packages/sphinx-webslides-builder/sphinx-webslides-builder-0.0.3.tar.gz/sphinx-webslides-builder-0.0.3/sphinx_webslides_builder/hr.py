from sphinx.util.docutils import SphinxDirective
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.writers.html import HTMLTranslator

from .common import (
    generic_visit,
    BaseNode,
    GenericDirective,
)

TAG = 'hr'

class topic_shift_node(BaseNode): pass

def topic_shift_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    node = topic_shift_node()
    return [node], []

class TopicShiftDirective(GenericDirective):
    node_type = topic_shift_node

def setup_hr(app):
    app.add_node(topic_shift_node)
    app.add_role('hr', topic_shift_role)
    app.add_directive('hr', TopicShiftDirective)

class HRTranslator(HTMLTranslator):

    def visit_topic_shift_node(self, node):
        generic_visit(self, TAG, node)

    def depart_topic_shift_node(self, node):
        pass