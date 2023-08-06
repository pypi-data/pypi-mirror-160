from sphinx.util.docutils import SphinxDirective
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.writers.html import HTMLTranslator

from .common import (
    generic_visit,
    generic_depart,
)

TAG = 'figure'
CAPTION_TAG = 'figcaption'

# TODO: The Figure directive will need to be replaced
# to allow complex caption contents like links and svg
# The legend functionality is also problematic

class FigureTranslator(HTMLTranslator):
    """ webslides needs a figure tag
    around the image.  No super() because
    visit_figure adds a div that ruins things"""
    
    def visit_figure(self, node):
        generic_visit(self, TAG, node)

    def depart_figure(self, node):
        generic_depart(self, TAG)

    def visit_caption(self, node):
        generic_visit(self, CAPTION_TAG, node)

    def depart_caption(self, node):
        generic_depart(self, CAPTION_TAG)