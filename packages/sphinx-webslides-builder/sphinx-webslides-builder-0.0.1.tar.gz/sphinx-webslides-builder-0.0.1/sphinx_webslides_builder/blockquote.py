from copy import deepcopy

from sphinx.util.docutils import SphinxDirective
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.writers.html import HTMLTranslator

from .paragraph import paragraph_node

TAG = 'blockquote'

from .common import (
    BaseClassNode,
    BaseNode,
    add_role_and_directive,
    add_visit_depart,
    GenericDirective,
    create_role,
)

class blockquote_node(BaseNode): pass
class text_quote_node(BaseClassNode):
    classes = ['text-quote']
class cite_node(BaseNode): pass

class TextQuoteDirective(GenericDirective):
    node_type = text_quote_node
    option_spec = deepcopy(GenericDirective.option_spec)
    option_spec.update({
        'citation': directives.unchanged
    })

    def run(self):
        node = super().run()[0]
        cite = 'citation'
        if cite in self.options:
            citation = cite_node()
            paragraph = paragraph_node()
            citation += nodes.Text(self.options[cite])
            paragraph += citation
            node += paragraph
        return [node]

class BlockquoteDirective(TextQuoteDirective):
    node_type = blockquote_node

def setup_blockquote(app):
    app.add_node(text_quote_node)
    app.add_node(cite_node)
    app.add_role('text-quote', create_role(text_quote_node))
    app.add_role('blockquote', create_role(blockquote_node))
    app.add_directive('text-quote', TextQuoteDirective)
    app.add_directive('blockquote', BlockquoteDirective)
    add_role_and_directive(app, cite_node, 'cite')

    # Convenience
    app.add_role('tq', create_role(text_quote_node))
    app.add_role('bq', create_role(blockquote_node))

class BlockquoteTranslator(HTMLTranslator):
    pass

add_visit_depart(BlockquoteTranslator, text_quote_node.__name__, TAG)
add_visit_depart(BlockquoteTranslator, blockquote_node.__name__, TAG)
add_visit_depart(BlockquoteTranslator, cite_node.__name__, 'cite')