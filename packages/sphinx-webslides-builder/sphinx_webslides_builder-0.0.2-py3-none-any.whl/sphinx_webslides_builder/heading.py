from copy import deepcopy

from sphinx.util.docutils import SphinxDirective
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.writers.html import HTMLTranslator

from .common import (
    process_classes,
    GenericDirective,
    generic_visit,
    generic_depart,
    get_node,
    get_generic_directive,
    BaseClassNode,
    BaseNode,
)

class pseudo_heading_node(BaseClassNode): pass
class text_landing_node(BaseClassNode):
    classes=['text-landing']

def setup_heading(app):
    app.add_node(pseudo_heading_node)
    app.add_node(text_landing_node)
    app.add_role('ph1', heading_role(pseudo_heading_node, 'h1'))
    app.add_role('ph2', heading_role(pseudo_heading_node, 'h2'))
    app.add_role('ph3', heading_role(pseudo_heading_node, 'h3'))
    app.add_role('ph4', heading_role(pseudo_heading_node, 'h4'))
    app.add_role('ph5', heading_role(pseudo_heading_node, 'h5'))
    app.add_role('ph6', heading_role(pseudo_heading_node, 'h6'))
    app.add_role('tlh1', heading_role(text_landing_node, 'h1'))
    app.add_role('tlh2', heading_role(text_landing_node, 'h2'))
    app.add_role('tlh3', heading_role(text_landing_node, 'h3'))
    app.add_role('tlh4', heading_role(text_landing_node, 'h4'))
    app.add_role('tlh5', heading_role(text_landing_node, 'h5'))
    app.add_role('tlh6', heading_role(text_landing_node, 'h6'))
    app.add_directive('heading', HeadingDirective)
    app.add_directive('text-landing', TextLandingDirective)


def heading_role(node_type, tag: str):
    def role(name, rawtext, text, lineno, inliner, options={}, content=[]):
        node = node_type()
        node += nodes.Text(text)
        node['tag'] = tag
        return [node], []
    return role

class HeadingDirective(GenericDirective):
    required_arguments = 1
    node_type = pseudo_heading_node

    def run(self):
        node_list = super().run()
        node_list[0]['tag'] = self.arguments[0]
        return node_list

class TextLandingDirective(HeadingDirective):
    node_type = text_landing_node
    option_spec = deepcopy(HeadingDirective.option_spec)
    option_spec.update({
        'shadow': directives.unchanged,
    })

    def run(self):
        node = super().run()[0]
        if 'shadow' in self.options:
            node.add_class('text-shadow')
        return [node]

class HeadingTranslator(HTMLTranslator):

    def visit_pseudo_heading_node(self, node):
        generic_visit(self, node['tag'], node)
    
    def depart_pseudo_heading_node(self, node):
        generic_depart(self, node['tag'])
    
    def visit_text_landing_node(self, node):
        generic_visit(self, node['tag'], node)
    
    def depart_text_landing_node(self, node):
        generic_depart(self, node['tag'])