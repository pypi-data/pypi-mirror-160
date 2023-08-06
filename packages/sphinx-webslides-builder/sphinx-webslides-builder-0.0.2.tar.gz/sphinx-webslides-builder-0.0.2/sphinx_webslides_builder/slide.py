from copy import deepcopy

from sphinx.util.docutils import SphinxDirective
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.writers.html import HTMLTranslator
from sphinx.util import logging

from .div import div_wrap_node, div_node
from .span import background_node
from .video import video_node
from .header_footer import make_header_node, set_alignment, make_footer_node
from .paragraph import paragraph_node
from .common import (
    add_class_to_tag,
    process_classes,
    GenericDirective,   
    BaseClassNode,
)

logger = logging.getLogger(__name__)

SECTION_TAG = 'section'

def source_read_handler(app, docname, source):
    app.config['slide_config'] = {}

def setup_slide(app):
    app.add_node(slide_node)
    app.add_directive('slide', Slide)
    app.add_directive('slide-config', SlideConfig)
    app.connect('source-read', source_read_handler)

class slide_node(BaseClassNode):
    pass

class SlideTranslator(HTMLTranslator):
    slide_open = False
    
    def visit_slide_node(self, node):
        if self.slide_open:
            self.body.append(f'</{SECTION_TAG}>')
        content = process_classes(f'<{SECTION_TAG}>', node, SECTION_TAG)
        self.body.append(content)

    def depart_slide_node(self, node):
            self.body.append('</section>')
            self.slide_open = False 

class Slide(GenericDirective):
    node_type = slide_node
    option_spec = deepcopy(GenericDirective.option_spec)
    option_spec.update({
        # wrap will be deprecated
        'wrap': directives.unchanged,
        'no-wrap': directives.unchanged,
        'wrap-size': directives.unchanged,
        'wrap-zoom-in': directives.unchanged,
        'background-image': directives.unchanged,
        'dark-background-image': directives.unchanged,
        'light-background-image': directives.unchanged,
        'background-image-location': directives.unchanged,
        'background-image-animation': directives.unchanged,
        'background-color': directives.unchanged,
        'vertical-alignment': directives.unchanged,
        'content-alignment': directives.unchanged,
        'card-size': directives.unchanged,
        'card-background': directives.unchanged,
        'flex-content': directives.unchanged,
        'full-screen': directives.unchanged,
        'background-video': directives.unchanged,
        'background-video-poster': directives.unchanged,
        'background-video-dark': directives.unchanged,
        'text-serif': directives.unchanged,
        'no-defaults': directives.unchanged,
        'header': directives.unchanged,
        'header-alignment': directives.unchanged,
        'footer': directives.unchanged,
        'footer-alignment': directives.unchanged,
    })

    def run(self):        
        if 'no-defaults' not in self.options:
            # get defaults and update with specific requests for this directive
            # i.e. requests override defaults
            slide_settings = deepcopy(self.env.app.config['slide_config'])
            slide_settings.update(
                self.options
            )
            self.options = slide_settings
        node = slide_node()
        active_node = node
        # Slide Node modifcations        
        active_node = self.set_horizontal_alignment(active_node)
        active_node = self.set_vertical_alignment(active_node)
        active_node = self.set_class_options(active_node)
        active_node = self.set_background_color(active_node)
        active_node = self.set_full_screen(active_node)
        active_node = self.set_text_serif(active_node)
        # Adding child nodes
        # Add before wrap
        active_node = self.set_background_image(active_node)        
        active_node = self.set_background_video(active_node)
        active_node = self.set_header(active_node)
        active_node = self.set_footer(active_node)
        # wrap
        active_node = self.check_wrap(active_node)  
        # after wrap
        active_node = self.check_card(active_node)
        active_node = self._process_content(active_node)      
        return [node]

    def set_header(self, node):
        return self.set_header_footer('header', 'header-alignment', node, make_header_node)
    
    def set_footer(self, node):
        return self.set_header_footer('footer', 'footer-alignment', node, make_footer_node)

    def set_header_footer(self, option_name, alignment_name, node, node_maker):
        if option_name in self.options:
            hf_node, hf_active_node = node_maker()
            # Need to wrap as paragraph when not using header
            # directive, paragraph wraps alignment span
            paragraph = paragraph_node()
            hf_active_node += paragraph
            hf_active_node = paragraph
            if alignment_name in self.options:
                hf_active_node = set_alignment(
                    {'horizontal-alignment': self.options[alignment_name]}, 
                    hf_active_node
                )
            hf_active_node += nodes.Text(self.options[option_name])
            node += hf_node
        return node
    
    def set_full_screen(self, node):
        fs = 'full-screen'
        if fs in self.options:
            node.add_class('fullscreen')
        return node
    
    def check_card(self, node):
        cs = 'card-size'
        active_node = node
        if cs in self.options:
            # TODO: probably need to verify size against
            # what is in the CSS
            requested_size = self.options[cs]
            div = div_node()
            node += div
            div.add_class(f'card-{requested_size}')
            active_node = div
            cb = 'card-background'
            if cb in self.options:
                div.add_class(self.options[cb])
        return active_node
    
    def set_background_color(self, node):
        bc = 'background-color'
        if bc in self.options:
            node.add_class(self.options[bc])
        return node

    def set_text_serif(self, node):
        ts = 'text-serif'
        if ts in self.options:
            node.add_class('text-serif')
        return node

    def set_background_video(self, node):
        bv = 'background-video'
        bvp = 'background-video-poster'
        if bv in self.options:
            video = video_node(
                poster_target=self.options[bvp],
                video_target=self.options[bv],
                dark=('background-video-dark' in self.options),
            )
            node += video
        return node

    def set_background_image(self, node):
        bi = 'background-image'
        if bi in self.options:
            background = background_node()
            background.set_background_image(
                self.options[bi]
            )
            node += background
            if 'dark-background-image' in self.options:
                background.set_dark()
            if 'light-background-image' in self.options:
                background.set_light()
            if 'background-image-animation' in self.options:
                background.set_animation()
            bil = 'background-image-location'
            if bil in self.options:
                background.add_location(self.options[bil])
        return node
    
    def check_wrap(self, node):
        active_node = node
        if 'no-wrap' not in self.options:
            div = div_wrap_node()
            active_node = div
            ws = 'wrap-size'
            if ws in self.options:
                div.add_class(f"size-{self.options[ws]}")
            node += div
            wzi = 'wrap-zoom-in'
            if wzi in self.options:
                div.add_class('zoomIn')
            if 'wrap' in self.options:
                logger.warning("\"wrap\" option on slide directive no longer used, will be removed soon!")
        ca = 'content-alignment'
        if ca in self.options:
            div = div_node()
            requested_alignment = self.options[ca]
            good_request = False
            if requested_alignment == 'left':
                div.add_class('content-left')
                good_request = True
            elif requested_alignment == 'center':
                div.add_class('content-center')
                good_request = True
            elif requested_alignment == 'right':
                div.add_class('content-right')
                good_request = True
            else:
                print(f'ERROR: Bad requested content alignment: {requested_alignment}, ignoring...')
            if good_request:
                active_node += div
                active_node = div
        return active_node

    def set_vertical_alignment(self, node):
        va = 'vertical-alignment'
        if va in self.options:
            requested_alignment = self.options[va].lower()
            if requested_alignment == 'top':
                node.add_class('slide-top')
            elif requested_alignment == 'bottom':
                node.add_class('slide-bottom')
            else:
                print(f'ERROR: Vertical alignment {requested_alignment} unknown, ignoring...')
        return node

class SlideConfig(Slide):

    def run(self):
        self.env.app.config['slide_config'] = deepcopy(self.options)
        return []