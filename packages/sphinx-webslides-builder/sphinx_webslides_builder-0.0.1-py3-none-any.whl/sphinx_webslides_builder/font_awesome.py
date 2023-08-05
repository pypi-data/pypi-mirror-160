from copy import deepcopy

from sphinx.util.docutils import SphinxDirective
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.writers.html import HTMLTranslator

from .common import (
    BaseClassNode,
    add_class_to_tag,
    GenericDirective,
)

class fa_node(BaseClassNode):
    pass

class fa_large_node(BaseClassNode):
    classes = ['large']

class fa_span_node(nodes.Element):
    pass

def fa_role_maker(span: bool=False, large: bool = False):
    def fa_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
        if span:
            # TODO: this should really add a span node with fa_node inside
            node = fa_span_node()
        elif large:
            node = fa_large_node()
        else:
            node = fa_node()
        node['fa_type'] = text
        return [node], []
    return fa_role

class FontAwesomeDirective(GenericDirective):
    required_arguments = 1
    optional_arguments = 4

    option_spec = deepcopy(GenericDirective.option_spec)
    option_spec.update({
        'span': directives.unchanged,
        'large': directives.unchanged,
    })

    def run(self):
        # TODO: This should be handled better, i.e.
        # span node containing fa node
        if 'span' in self.options:
            self.node_type = fa_span_node
        elif 'large' in self.options:
            self.node_type = fa_large_node
        else:
            self.node_type = fa_node
        node = super().run()[0]
        node['fa_type'] = self.arguments[0]
        return [node]

def setup_fa(app):
    app.add_node(fa_node)
    app.add_node(fa_span_node)
    app.add_role('font-awesome', fa_role_maker())
    app.add_role('font-awesome-span', fa_role_maker(span=True))
    app.add_directive('font-awesome', FontAwesomeDirective)
    # Convenience
    app.add_role('fa', fa_role_maker())
    app.add_role('fa-span', fa_role_maker(span=True))
    app.add_role('fa-l', fa_role_maker(large=True))

class FontAwesomeTranslator(HTMLTranslator):
    
    def visit_fa_node(self, node):
        fa_type = node['fa_type']
        content = f"""<svg class=\"{fa_type}\">
    <use xlink:href=\"#{fa_type}\"></use>
</svg>"""
        for class_name in node.get('classes', []):
            content = add_class_to_tag(content, 'svg', class_name)
        self.body.append(content)

    def visit_fa_span_node(self, node):
        self.body.append('<span>')
        self.visit_fa_node(node)

    def depart_fa_node(self, node):
        pass
    
    def depart_fa_span_node(self, node):
        self.body.append('</span>')

    def visit_fa_large_node(self, node):
        self.visit_fa_node(node)

    def depart_fa_large_node(self, node):
        self.depart_fa_node(node)