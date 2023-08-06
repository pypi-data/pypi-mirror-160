from sphinx.util.docutils import SphinxDirective
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.writers.html import HTMLTranslator

from .common import (
    BaseNode,
    add_role_and_directive,
    add_visit_depart,
    GenericDirective,
    BaseClassNode,
)

TAG = 'video'
VIDEO_TARGET_ATTRIBUTE_NAME = 'poster'
SOURCE_TARGET_ATTRIBUTE_NAME = 'src'

VIDEO_ATTRIBUTES = [
    'autoplay',
    'muted',
    'loop',
]

class video_node(BaseClassNode):
    def __init__(self, *args, dark: bool = False, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_class('background-video')
        if dark:
            self.add_class('dark')
        self.add_data(**kwargs)
        self.add_attributes(
            {attr: None for attr in VIDEO_ATTRIBUTES}
        )

    def add_data(self, poster_target: str = None, video_target: str = None):
        if poster_target is not None:
            self.add_target('poster', poster_target)
        if video_target is not None:
            source = video_source_node(target=video_target)
            self += source
    
    def add_target(self, attribute_name: str, target: str):
        a = 'attributes'
        if a not in self:
            self[a] = {}        
        self[a].update({
            attribute_name: target,
        })


class video_source_node(BaseClassNode): 
    def __init__(self, *args, target: str = None, **kwargs):
        super().__init__(*args, **kwargs)
        if target is not None:
            self.add_attributes({
                'src': target,
            })
        # TODO: LIkely need to set this based on target
        self.add_attributes({
            'type': "video/mp4",
        })

class VideoDirective(GenericDirective):
    node_type = video_node
    required_arguments = 2

    def super(self):
        node = super().run()[0]
        node.add_data(
            poster_target=self.arguments[0],
            video_target=self.arguments[1],
        )
        return [node]

def setup_video(app):
    app.add_node(video_node)
    app.add_node(video_source_node)
    app.add_directive('video', VideoDirective)

class VideoTranslator(HTMLTranslator):
    pass
add_visit_depart(VideoTranslator, video_node.__name__, TAG)
add_visit_depart(VideoTranslator, video_source_node.__name__, 'source')

