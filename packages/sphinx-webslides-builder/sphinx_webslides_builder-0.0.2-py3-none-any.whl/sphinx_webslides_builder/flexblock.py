import copy

from sphinx.util.docutils import SphinxDirective
from docutils import nodes
from docutils.parsers.rst import directives
from sphinx.writers.html import HTMLTranslator

from .common import (
    add_class_to_tag,
    GenericDirective,
    BaseNode,
    BaseClassNode,
)

class flexblock_list_node(BaseNode): pass
class flexblock_list_border_node(BaseClassNode, flexblock_list_node):
    classes = ['border']
class flexblock_list_reasons_node(BaseClassNode, flexblock_list_node):
    classes = ['reasons']
class flexblock_list_steps_node(BaseClassNode, flexblock_list_node):
    classes = ['steps']
class flexblock_list_clients_node(BaseClassNode, flexblock_list_node):
    classes = ['clients']
class flexblock_list_features_node(BaseClassNode, flexblock_list_node):
    classes = ['features']
class flexblock_list_metrics_node(BaseClassNode, flexblock_list_node):
    classes = ['metrics']
class flexblock_list_activity_node(BaseClassNode, flexblock_list_node):
    classes = ['activity']
class flexblock_list_gallery_node(BaseClassNode, flexblock_list_node):
    classes = ['gallery']
class flexblock_list_spec_node(BaseClassNode, flexblock_list_node):
    classes = ['specs']
class text_cols_list_node(BaseNode): pass

class FlexblockDirective(GenericDirective):
    node_type = flexblock_list_node
class FlexblockBorderDirective(GenericDirective):
    node_type = flexblock_list_border_node
class FlexblockReasonsDirective(GenericDirective):
    node_type = flexblock_list_reasons_node
class FlexblockStepsDirective(GenericDirective):
    node_type = flexblock_list_steps_node
class FlexblockClientsDirective(GenericDirective):
    node_type = flexblock_list_clients_node
class FlexblockFeaturesDirective(GenericDirective):
    node_type = flexblock_list_features_node
class FlexblockMetricsDirective(GenericDirective):
    node_type = flexblock_list_metrics_node
class FlexblockActivityDirective(GenericDirective):
    node_type = flexblock_list_activity_node
class FlexblockGalleryDirective(GenericDirective):
    node_type = flexblock_list_gallery_node
class FlexblockSpecDirective(GenericDirective):
    node_type = flexblock_list_spec_node
class TextColsDirective(GenericDirective):
    node_type = text_cols_list_node

def setup_flexblock(app):
    app.add_node(flexblock_list_node)
    app.add_node(flexblock_list_border_node)
    app.add_node(flexblock_list_reasons_node)
    app.add_node(flexblock_list_steps_node)
    app.add_node(flexblock_list_clients_node)
    app.add_node(flexblock_list_features_node)
    app.add_node(flexblock_list_metrics_node)
    app.add_node(flexblock_list_activity_node)
    app.add_node(flexblock_list_gallery_node)
    app.add_node(flexblock_list_spec_node)
    app.add_node(text_cols_list_node)
    app.add_directive('flexblock', FlexblockDirective)
    app.add_directive('flexblock-border', FlexblockBorderDirective)
    app.add_directive('flexblock-reasons', FlexblockReasonsDirective)
    app.add_directive('flexblock-steps', FlexblockStepsDirective)
    app.add_directive('flexblock-clients', FlexblockClientsDirective)
    app.add_directive('flexblock-features', FlexblockFeaturesDirective)
    app.add_directive('flexblock-metrics', FlexblockMetricsDirective)
    app.add_directive('flexblock-activity', FlexblockActivityDirective)
    app.add_directive('flexblock-gallery', FlexblockGalleryDirective)
    app.add_directive('flexblock-spec', FlexblockSpecDirective)
    app.add_directive('text-cols', TextColsDirective)

class FlexblockTranslator(HTMLTranslator):
    flexblock_open = False
    flexblock_classes = []
    description_list_open = False
    text_cols_open = False
    flexblock_div_open = False

    def visit_flexblock_list_node(self, node):
        self.flexblock_div_open = True
        self.base_visit_flexblock_list_node(node)

    def depart_flexblock_list_node(self, node):
        self.base_depart_flexblock_list_node(node)
        self.flexblock_div_open = False
    
    def base_visit_flexblock_list_node(self, node):
        self.flexblock_open = True
        self.flexblock_classes = copy.deepcopy(node['classes'])

    def base_depart_flexblock_list_node(self, node):
        pass

    def visit_flexblock_list_border_node(self, node):
        self.base_visit_flexblock_list_node(node)

    def depart_flexblock_list_border_node(self, node):
        self.base_depart_flexblock_list_node(node)
    
    def visit_flexblock_list_reasons_node(self, node):
        self.body.append("<div class=\"bg-white shadow\">")
        self.base_visit_flexblock_list_node(node)

    def depart_flexblock_list_reasons_node(self, node):
        self.base_depart_flexblock_list_node(node)
        self.body.append("</div>")
    
    def visit_flexblock_list_steps_node(self, node):
        self.base_visit_flexblock_list_node(node)

    def depart_flexblock_list_steps_node(self, node):
        self.base_depart_flexblock_list_node(node)
        
    def visit_flexblock_list_clients_node(self, node):
        self.base_visit_flexblock_list_node(node)

    def depart_flexblock_list_clients_node(self, node):
        self.base_depart_flexblock_list_node(node)
    
    def visit_flexblock_list_features_node(self, node):
        self.flexblock_div_open = True
        self.base_visit_flexblock_list_node(node)

    def depart_flexblock_list_features_node(self, node):
        self.flexblock_div_open = False
        self.base_depart_flexblock_list_node(node)
    
    def visit_flexblock_list_metrics_node(self, node):
        self.flexblock_div_open = True
        self.base_visit_flexblock_list_node(node)

    def depart_flexblock_list_metrics_node(self, node):
        self.flexblock_div_open = False
        self.base_depart_flexblock_list_node(node)
    
    def visit_flexblock_list_activity_node(self, node):
        self.flexblock_div_open = True
        self.base_visit_flexblock_list_node(node)

    def depart_flexblock_list_activity_node(self, node):
        self.flexblock_div_open = False
        self.base_depart_flexblock_list_node(node)
    
    def visit_flexblock_list_gallery_node(self, node):
        self.flexblock_div_open = True
        self.base_visit_flexblock_list_node(node)

    def depart_flexblock_list_gallery_node(self, node):
        self.flexblock_div_open = False
        self.base_depart_flexblock_list_node(node)
    
    def visit_flexblock_list_spec_node(self, node):
        self.flexblock_div_open = True
        self.base_visit_flexblock_list_node(node)

    def depart_flexblock_list_spec_node(self, node):
        self.flexblock_div_open = False
        self.base_depart_flexblock_list_node(node)
    
    def visit_text_cols_list_node(self, node):
        self.text_cols_open = True

    def depart_text_cols_list_node(self, node):
        pass

    def visit_bullet_list(self, node):
        # TODO: not sure how to handle this better
        # Not portable as written
        # Could consider combining
        if not self.description_list_open:
            super().visit_bullet_list(node)
            if self.flexblock_open:
                self.body[-1] = add_class_to_tag(self.body[-1], 'ul', 'flexblock')
                for class_name in self.flexblock_classes:
                    self.body[-1] = add_class_to_tag(self.body[-1], 'ul', class_name)
                self.flexblock_open = False
                self.flexblock_classes = []
            elif self.text_cols_open:
                self.body[-1] = add_class_to_tag(self.body[-1], 'ul', 'text-cols')
                self.text_cols_open = False

    def visit_list_item(self, node):
        super().visit_list_item(node)
        if self.flexblock_div_open:
            self.body.append('<div>')

    def depart_list_item(self, node):
        if self.flexblock_div_open:
            self.body.append('</div>')
        super().depart_list_item(node)
