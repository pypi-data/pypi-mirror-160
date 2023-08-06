from sphinx.util.docutils import SphinxDirective
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.writers.html import HTMLTranslator

from .common import (
    add_class_to_tag,
    BaseClassNode,
    GenericDirective,
)

class description_list_node(BaseClassNode):
    classes = ['description']

class DescriptionListDirective(GenericDirective):
    node_type = description_list_node

def setup_description_list(app):
    app.add_node(description_list_node)
    app.add_directive('description-list', DescriptionListDirective)

class DescriptionListTranslator(HTMLTranslator):

    def visit_description_list_node(self, node):
        self.description_list_open = True
        content = '<ul>'
        for class_name in node['classes']:
            content = add_class_to_tag(
                content, 'ul', class_name
            )
        self.body.append(content)
    
    def depart_bullet_list(self, node):
        if not self.description_list_open:
            super().depart_bullet_list(node)

    def depart_description_list_node(self, node):
        self.description_list_open = False
        self.body.append('</ul>')