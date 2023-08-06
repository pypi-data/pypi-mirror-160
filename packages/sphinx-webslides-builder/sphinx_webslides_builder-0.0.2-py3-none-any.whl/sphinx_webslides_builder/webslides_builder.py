from os import path
from typing import Any, Dict, Iterator, Set, Tuple
import shutil
from pathlib import Path

from docutils.io import StringOutput
from docutils.nodes import Node
from sphinx.builders import Builder
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.util.osutil import ensuredir, os_path

from .webslides_writer import WebslidesWriter, WebslidesTranslator

class WebslidesBuilder(StandaloneHTMLBuilder):
    name = 'webslides'
    default_translator_class = WebslidesTranslator
    
