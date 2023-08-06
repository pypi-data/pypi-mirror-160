# Overview

A sphinx extesion to make slides with [Webslides](https://webslides.tv/#slide=1).

# Installation

```
pip install sphinx-webslides-builder
```

# Usage

## Summary

1. Start a sphinx document
2. Modify the `conf.py`
3. Create content (and add to `index.rst`)
4. sphinx build the document

## Details

`sphinx-quickstart` a sphinx document as normal.

`conf.py` modifications:

```
extensions = [
    'sphinx_webslides_builder',
]

html_theme = 'webslides_theme'
```

Examples of slides can be seen in the
example_doc, specifically `keynote.rst` for an 
example slide deck.

Simple single slide example:

Create `deck.rst` in your sphinx doc folder and add:

```
.. slide::

    :ph1:`A Level 1 Heading`

    Some amazing content
```

Build the slides:

```
sphinx-build -b webslides sphinx_document_folder sphinx_document_folder/_webslides_build
```

Open `sphinx_document_folder/_webslides_build/deck.html`.

Full docs coming soon.

# Markdown Support

To use markdown as shown in some of the examples,
installation and configuration of 
[myst-parser](https://myst-parser.readthedocs.io/en/latest/)
is required.

# Running / Developing Locally

Make sure you add the webslides dependencies:

```
bash .github/scripts/get_webslides.sh
pip install -e .
```