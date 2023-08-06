from sphinx.util.docutils import SphinxDirective
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.writers.html import HTMLTranslator

from .common import (
    process_classes,
    GenericDirective,
    add_attribute_to_tag,
    create_role,
    create_directive,
    generic_visit,
    generic_depart,
    get_node,
    get_generic_translator_class,
    add_role_and_directive,
    BaseNode,
    BaseClassNode,
    add_visit_depart,
)

TAG = 'p'

class paragraph_node(BaseNode): pass
class text_subtitle_node(BaseClassNode, paragraph_node):
    classes=['text-subtitle']
class text_symbols_node(BaseClassNode, paragraph_node):
    classes=['text-symbols']
class text_intro_node(BaseClassNode, paragraph_node):
    classes=['text-intro']
class text_center_node(BaseClassNode, paragraph_node):
    classes=['aligncenter']
class text_year_node(BaseClassNode, paragraph_node):
    classes=['year']
class text_title_node(BaseClassNode, paragraph_node):
    classes=['title']
class text_summary_node(BaseClassNode, paragraph_node):
    classes=['summary']
class text_context_node(BaseClassNode, paragraph_node):
    classes=['text-context']
class text_pull_right_node(BaseClassNode, paragraph_node):
    classes=['text-pull-right']

paragraph_map = {
    'paragraph': paragraph_node,
    'text-subtitle': text_subtitle_node,
    'text-symbols': text_symbols_node,
    'text-intro': text_intro_node,
    'text-center': text_center_node,
    'year': text_year_node,
    'title': text_title_node,
    'summary': text_summary_node,
    'text-context': text_context_node,
    'text-pull-right': text_pull_right_node,
}

def setup_paragraph(app):
    for label in paragraph_map:
        node_type = paragraph_map[label]
        app.add_node(node_type)
        add_role_and_directive(app, node_type, label)
    # Convenience label
    add_role_and_directive(app, text_intro_node, 'ti')
    add_role_and_directive(app, text_center_node, 'c')
    add_role_and_directive(app, text_center_node, 'tsym')
    add_role_and_directive(app, text_subtitle_node, 'tsub')
    add_role_and_directive(app, text_context_node, 'tc')
    add_role_and_directive(app, text_pull_right_node, 'tpr')

class ParagraphTranslator(HTMLTranslator):
    
    def visit_paragraph(self, node):
        """ Filter blank paragraphs

        webslides is very sensitive to blank paragraphs
        AND sphinx really likes to produce them.
        """
        if node.astext() != '':
            super().visit_paragraph(node)

    def depart_paragraph(self, node):
        if node.astext() != '':
            super().depart_paragraph(node)

for thing in paragraph_map.values():
    add_visit_depart(
        ParagraphTranslator,
        thing.__name__,
        TAG,
    )