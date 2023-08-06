from sphinx.util.docutils import SphinxDirective
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.writers.html import HTMLTranslator

from .common import (
    BaseNode,
    GenericDirective,
    add_visit_depart
)

class web_node(BaseNode): pass
class iframe_node(BaseNode): pass
class figcaption_node(BaseNode): pass

# tag to node
web_map = {
    'figure': web_node,
    'iframe': iframe_node,
    'figcaption': figcaption_node, 
}

class WebDirective(GenericDirective):
    node_type = web_node
    required_arguments = 1

    def run(self):
        node = super().run()[0]
        iframe = iframe_node()
        node += iframe
        if self.content:
            figcaption = figcaption_node()
            figcaption = self._process_content(figcaption)
            node += figcaption
        iframe['attributes'] = {
            'src': self.arguments[0],
            'width': '800',
            'height': '600',
        }
        return [node]

def setup_web(app):
    for node_type in web_map.values():
        app.add_node(node_type)
    app.add_directive('web', WebDirective)

class WebTranslator(HTMLTranslator):
    pass

for tag in web_map:
    node_type = web_map[tag]
    add_visit_depart(WebTranslator, node_type.__name__, tag)