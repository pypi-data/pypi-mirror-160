import copy

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
    get_generic_translator_class,
    add_visit_depart,
    add_role_and_directive,
    BaseNode,
    BaseClassNode,
)

TAG = 'div'

class div_node(BaseClassNode): pass
class div_wrap_node(BaseClassNode):
    classes=['wrap']
class grid_node(BaseClassNode):
    classes=['grid']
class column_node(BaseClassNode):
    classes=['column']
class center_node(BaseClassNode):
    classes=['aligncenter']
class flex_content_node(BaseClassNode):
    classes=['flex-content']
class content_left_node(BaseClassNode):
    classes=['content-left']
class content_center_node(BaseClassNode):
    classes=['content-center']
class content_right_node(BaseClassNode):
    classes=['content-right']
class overlay_node(BaseClassNode):
    classes=['overlay']
class cta_node(BaseClassNode):
    classes=['cta']
class number_node(BaseClassNode):
    classes=['number']
class benefit_node(BaseClassNode):
    classes=['benefit']
class text_cols_div_node(BaseClassNode):
    classes=['text-cols']
class embed_node(BaseClassNode):
    classes=['embed']
class youtube_node(BaseClassNode):
    youtube_attributes = {
        'data-youtube': None,
        'data-autoplay': None,
        'data-no-controls': None,
    }

    def __init__(self, youtube_id: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.youtube_attributes['data-youtube-id'] = youtube_id

    def show_controls(self):
        del(self.youtube_attributes['data-no-controls'])

class process_step_node(BaseClassNode):
    classes=['process']

    def __init__(self, *args, step_number: int = None, **kwargs):
        super().__init__(*args, **kwargs)
        if step_number is not None:
            self.add_step_number(step_number)

    def add_step_number(self, step_number: int):
        self.add_class(f"step-{step_number}")

class ProcessStepDirective(GenericDirective):
    required_arguments = 1
    node_type = process_step_node

    def run(self):
        node = super().run()[0]
        node.add_step_number(self.arguments[0])
        return [node]

class YoutubeDirective(GenericDirective):
    required_arguments = 1
    node_type = embed_node
    option_spec = copy.deepcopy(GenericDirective.option_spec)
    option_spec.update({
        'show-controls': directives.unchanged,
    })

    def run(self):
        node = super().run()[0]
        yt_node = youtube_node(self.arguments[0])
        if 'show-controls' in self.options:
            yt_node.show_controls()
        yt_node.add_attributes(yt_node.youtube_attributes)
        node += yt_node
        return [node]

ALLOWED_SIDEBAR_CONFIGS = [
    'sm', 'ms', 'sms'
]
class GridDirective(GenericDirective):
    
    node_type = grid_node
    option_spec = copy.deepcopy(GenericDirective.option_spec)
    option_spec.update({
        'alignment': directives.unchanged,
        'sidebar-config': directives.unchanged,
    })

    def run(self):
        node = super().run()[0]
        a = 'alignment'
        if a in self.options:
            requested_alignment = self.options[a]
            if requested_alignment == 'vertical':
                node.add_class('vertical-align')
            else:
                print(f'ERROR: Unknown grid alignment: {requested_alignment}, ignoring')
        sc = 'sidebar-config'
        if sc in self.options:
            requested_config = self.options[sc].lower()
            if requested_config in ALLOWED_SIDEBAR_CONFIGS:
                node.add_class(requested_config)
        return [node]

div_map = {
    'div': div_node,
    'div-wrap': div_wrap_node,
    'column': column_node,
    'center': center_node,
    'flex-content': flex_content_node,
    'content-left': content_left_node,
    'content-center': content_center_node,
    'content-right': content_right_node,
    'overlay': overlay_node,
    'cta': cta_node,
    'number': number_node,
    'benefit': benefit_node,
    'text-cols-div': text_cols_div_node,
}

def process_step_role(name, rawtext, text, lineno, inliner, options={}, content=[]):
    node = process_step_node()
    node.add_step_number(int(text))
    return [node], []

def setup_div(app):
    for label in div_map:
        node_type = div_map[label]
        app.add_node(node_type)
        add_role_and_directive(app, node_type, label)
    app.add_node(grid_node)
    app.add_node(process_step_node)
    app.add_node(embed_node)
    app.add_node(youtube_node)
    app.add_directive('grid', GridDirective)
    app.add_directive('process-step', ProcessStepDirective)
    app.add_role('process-step', process_step_role)
    app.add_directive('youtube', YoutubeDirective)
    # Convenience
    app.add_role('ps', process_step_role)

class DivTranslator(HTMLTranslator):
    pass

add_visit_depart(DivTranslator, grid_node.__name__, TAG)
add_visit_depart(DivTranslator, process_step_node.__name__, TAG)
add_visit_depart(DivTranslator, embed_node.__name__, TAG)
add_visit_depart(DivTranslator, youtube_node.__name__, TAG)
for node_type in div_map.values():
    add_visit_depart(DivTranslator, node_type.__name__, TAG)

