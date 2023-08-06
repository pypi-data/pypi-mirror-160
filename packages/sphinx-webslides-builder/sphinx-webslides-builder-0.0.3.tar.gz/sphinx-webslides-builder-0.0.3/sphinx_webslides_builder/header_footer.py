from copy import deepcopy

from sphinx.util.docutils import SphinxDirective
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.writers.html import HTMLTranslator

from .div import div_wrap_node
from .span import span_node
from .common import (
    BaseNode,
    add_role_and_directive,
    add_visit_depart,
    GenericDirective,
)

TAG = 'header'

class header_node(BaseNode): pass
class footer_node(BaseNode): pass

def make_header_node():
    return make_node(header_node)

def make_footer_node():
    return make_node(footer_node)

def make_node(node_type):
    node = node_type()
    div = div_wrap_node()
    node += div
    active_node = div
    return node, active_node

def set_alignment(options: dict, active_node):
    ha = 'horizontal-alignment'
    if ha in options:
        requested_alignment = options[ha].lower()
        good_alignment = False
        # TODO: can it do center?
        if requested_alignment == 'right':
            class_alignment = 'alignright'
            good_alignment = True
        elif requested_alignment == 'left':
            class_alignment = 'alignleft'
            good_alignment = True
        elif requested_alignment == 'center':
            class_alignment = 'aligncenter'
            good_alignment = True
        else:
            print(f'ERROR: Bad requested header alignment {requested_alignment}, ignoring...')
        if good_alignment:
            span = span_node()
            span.add_class(class_alignment)
            active_node += span
            active_node = span
        del(options[ha])
    return active_node

class HeaderDirective(GenericDirective):
    node_type = header_node

    def run(self):
        node, active_node = make_node(self.node_type)        
        active_node = set_alignment(self.options, active_node)
        self._process_content(active_node)
        return [node]

class FooterDirective(HeaderDirective):
    node_type = footer_node

class HeaderConfigDirective(GenericDirective):
    node_type = header_node
    config_name = 'slide_header'
    option_spec = deepcopy(GenericDirective.option_spec)
    option_spec.update({
        'no-wrap': directives.unchanged,
    })

    def run(self):
        if 'no-wrap' in self.options:
            node = self.node_type()
            active_node = node
        else:
            node, active_node = make_node(self.node_type)        
        self.set_style(node)
        self._process_content(active_node)
        self.env.app.config[self.config_name] = deepcopy(node)
        return []

class FooterConfigDirective(HeaderConfigDirective):
    node_type = footer_node
    config_name = 'slide_footer'

def header_footer_default(app, docname, source):
    for item in ['slide_header', 'slide_footer']:
        try:
            del(app.config[item])
        except AttributeError:
            pass # config value not present, OK

def setup_header_footer(app):
    app.add_node(header_node)
    app.add_node(footer_node)
    app.add_directive('header-config', HeaderConfigDirective)
    app.add_directive('header', HeaderDirective)
    app.add_directive('footer-config', FooterConfigDirective)
    app.add_directive('footer', FooterDirective)
    app.connect('source-read', header_footer_default)

class HeaderFooterTranslator(HTMLTranslator):
    pass

add_visit_depart(HeaderFooterTranslator, header_node.__name__, TAG)
add_visit_depart(HeaderFooterTranslator, footer_node.__name__, 'footer')