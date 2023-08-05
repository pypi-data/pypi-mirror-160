from bs4 import BeautifulSoup
from docutils import nodes
from sphinx.util.docutils import SphinxDirective
from docutils.parsers.rst import directives
from sphinx.writers.html import HTMLTranslator

def add_class_to_tag(html: str, tag_name: str, class_name: str) -> str:
    return add_attribute_to_tag(html, tag_name, 'class', class_name)

def add_attribute_to_tag(html: str, tag_name: str, attribute_name: str, value: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')
    # value None is for attributes that do not assign
    if value is None:
        result = None
    else:
        result = soup.find(tag_name).get(attribute_name, []) + [value]
    soup.find(tag_name)[attribute_name] = result
    # bs4 adds a close tag, removing
    return str(soup).replace(f'</{tag_name}>', '')

def process_classes(content: str, node, tag_name: str) -> str:
    for class_name in node['classes']:
        content = add_class_to_tag(
            content, tag_name, class_name
        )
    return content

def process_attributes(content: str, node, tag_name: str) -> str:
    a = 'attributes' 
    if a in node:
        for label in node[a]:
            content = add_attribute_to_tag(
                content,
                tag_name,
                label,
                node[a][label],
            )
    return content

def process_style(content: str, node, tag_name: str) -> str:
    if 'style' in node:
        content = add_attribute_to_tag(
            content,
            tag_name,
            'style',
            node['style']
        )
    return content

def create_role(node_type, classes: list = None):
    def role(name, rawtext, text, lineno, inliner, options={}, content=[]):
        node = node_type()
        if classes is not None:
            node['classes'] = classes
        node += nodes.Text(text)
        return [node], []
    return role

class GenericDirective(SphinxDirective):
    option_spec = {
        'classes': directives.unchanged,
        'horizontal-alignment': directives.unchanged,
    }
    has_content = True

    def run(self):
        node = self.node_type()
        return self.generic_process(node)

    def generic_process(self, node):
        node = self.set_horizontal_alignment(node)
        node = self.set_class_options(node)
        if self.has_content:
            node = self._process_content(node)
        return [node]    
    
    def _process_content(self, node):        
        par = nodes.paragraph()
        self.state.nested_parse(self.content, self.content_offset, par)
        node += par
        return node

    def set_class_options(self, node):
        if 'classes' not in node:
            node['classes'] = []
        if 'classes' in self.options:
            node['classes'] = node['classes'] + self.options['classes'].split(' ')
        return node

    def set_horizontal_alignment(self, node):
        ha = 'horizontal-alignment'
        if ha in self.options:
            requested_alignment = self.options[ha].lower()
            if requested_alignment == 'center':
                node.add_class('aligncenter')
            elif requested_alignment == 'left':
                node.add_class('alignleft')
            elif requested_alignment == 'right':
                node.add_class('alignright')
            else:
                print(f'ERROR: Horizontal alignment {requested_alignment} unknown, ignoring...')
        return node

    

def create_directive(requested_node_type):
    class SimpleDirective(GenericDirective):
        node_type = requested_node_type

    return SimpleDirective

def generic_visit(translator, tag: str, node):
    content = f'<{tag}>'
    content = process_classes(content, node, tag)
    content = process_style(content, node, tag)
    content = process_attributes(content, node, tag)
    translator.body.append(content)

def generic_depart(translator, tag):
    translator.body.append(f'</{tag}>')

def create_generic_visit(tag: str):
    def a_visit(self, node):
        generic_visit(self, tag, node)
    return a_visit

def create_generic_depart(tag: str):
    def a_depart(self, node):
        generic_depart(self, tag)
    return a_depart

def get_generic_translator_class(tag: str, node_types: list):
    class GenericClass(HTMLTranslator):
        pass
    for node_type in node_types:
        GenericClass = add_visit_depart(GenericClass, node_type, tag)
    return GenericClass

def add_visit_depart(GenericClass, node_type:str, tag: str):
    setattr(
        GenericClass, 
        f'visit_{node_type}', 
        create_generic_visit(tag),
    )
    setattr(
        GenericClass, 
        f'depart_{node_type}', 
        create_generic_depart(tag),
    )
    return GenericClass

def get_generic_directive(requested_node_type) -> GenericDirective:
    class AGenericDirective(GenericDirective):
        node_type = requested_node_type

    return AGenericDirective

def get_node(node_name: str, classes: list = None, input_parent_class=None):
    if input_parent_class is None:
        ParentClass = nodes.Element
    else:
        ParentClass = input_parent_class
    class temp_node(ParentClass):
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if classes is not None:
                if 'classes' in self:
                    self['classes'] = self['classes'] + classes
                else:
                    self['classes'] = classes

    temp_node.__name__ = f'{node_name}_node'
    return temp_node

def add_role_and_directive(app, node_type, name: str):
    app.add_directive(name, get_generic_directive(node_type))
    app.add_role(name, create_role(node_type))

class BaseNode(nodes.Element):
    pass

class BaseClassNode(BaseNode):
    classes = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        if 'classes' in self:
            self['classes'] = self['classes'] + self.classes
        else:
            self['classes'] = self.classes

    def add_class(self, class_name: str):
        self['classes'] = self['classes'] + [class_name]

    def add_attributes(self, attribute_dict):
        a = 'attributes'
        if a in self:
            self[a].update(attribute_dict)
        else:
            self[a] = attribute_dict
