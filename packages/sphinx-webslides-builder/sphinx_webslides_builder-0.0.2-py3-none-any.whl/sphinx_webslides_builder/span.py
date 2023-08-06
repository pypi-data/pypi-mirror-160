from copy import deepcopy

from sphinx.util.docutils import SphinxDirective
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.writers.html import HTMLTranslator

from .common import (
    process_classes,
    GenericDirective,
    add_attribute_to_tag,
    create_role,
    get_generic_directive,
    add_role_and_directive,
    get_generic_translator_class,
    get_node,
    create_role,
    BaseNode,
    BaseClassNode,
    add_visit_depart,
)

TAG = 'span'

class span_node(BaseClassNode):pass
class text_label_node(BaseClassNode):
    classes = ['text-label']
class try_node(BaseClassNode):
    classes = ['try']
class span_raw_node(span_node): pass

ALLOWED_BACKGROUND_LOCATIONS = [
    'right-bottom',
    'left-bottom',
]
class background_node(span_node):
    classes=['background']

    def __init__(self, *args, 
        dark: bool = False, 
        light: bool = False, 
        animation: bool = False, 
        image_url: str = None, 
        location: str = None,
        **kwargs):
        super().__init__(*args, **kwargs)
        if dark:
            self.set_dark()
        if light:
            self.set_light()
        if animation:
            self.set_animation()
        if image_url is not None:
            self.set_background_image(image_url)
        if location is not None:
            self.add_location(location)

    def set_background_image(self, url: str):
        self['style'] = f"background-image:url('{url}')"

    def set_dark(self):
        self.add_class('dark')
    
    def set_light(self):
        self.add_class('light')

    def set_animation(self):
        self.add_class('anim')

    def add_location(self, requested_location):
        if requested_location in ALLOWED_BACKGROUND_LOCATIONS:
            self.add_class(f'background-{requested_location}')
            self['classes'].pop(self['classes'].index('background'))



class BackgroundImageDirective(GenericDirective):
    node_type = background_node
    required_arguments = 1
    option_spec = deepcopy(GenericDirective.option_spec)
    option_spec.update({
        'dark': directives.unchanged,
        'light': directives.unchanged,
        'animation': directives.unchanged,
        'location': directives.unchanged,
    })

    def run(self):
        node = super().run()[0]
        node.set_background_image(
            self.arguments[0]
        )
        if 'dark' in self.options:
            node.set_dark()
        if 'light' in self.options:
            node.set_light()
        if 'animation' in self.options:
            node.set_animation()
        loc = 'location'
        if loc in self.options:
            requested_location = self.options[loc].lower()
            node.add_location(requested_location)
        return [node]

def setup_span(app):
    app.add_node(span_node)
    app.add_node(span_raw_node)
    app.add_node(background_node)
    app.add_node(text_label_node)
    app.add_node(try_node)
    add_role_and_directive(app, try_node, 'try')
    add_role_and_directive(app, span_node, 'span')
    app.add_role('span-raw', raw_span_role)
    add_role_and_directive(app, text_label_node, 'text-label')
    app.add_directive('background-image', BackgroundImageDirective)
    app.add_role('background-image', create_role(background_node))
    
    # Convenience
    add_role_and_directive(app, text_label_node, 'tl')

def raw_span_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    node = span_raw_node()
    node['content'] = text
    return [node], []

class SpanTranslator(HTMLTranslator):
    
    def visit_span_node(self, node):
        content = f'<{TAG}>'
        content = process_classes(content, node, TAG)
        if 'style' in node:
            content = add_attribute_to_tag(
                content,
                TAG,
                'style',
                node['style']
            )
        self.body.append(content)
    
    def depart_span_node(self, node):
        self.body.append(f'</{TAG}>')

    def visit_span_raw_node(self, node):
        self.body.append(f"<{TAG}>{node['content']}")
    
    def depart_span_raw_node(self, node):
        self.depart_span_node(node)

    def visit_text_label_node(self, node):
        self.visit_span_node(node)

    def depart_text_label_node(self, node):
        self.depart_span_node(node)
        
    def visit_try_node(self, node):
        self.visit_span_node(node)

    def depart_try_node(self, node):
        self.depart_span_node(node)

