from codecs import open
from os import path
from setuptools import setup, find_packages
from subprocess import check_output

here = path.abspath(path.dirname(__file__))

# check_output(
#     'pandoc --from=markdown --to=rst --output=' + path.join(here, 'README.rst') + ' ' + path.join(here, 'README.md'),
#     shell=True
# )

# with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
#     long_description = f.read()
long_description = "Sphinx extension with a builder for webslides"

install_requires = list()
with open(path.join(here, 'requirements.txt'), 'r', encoding='utf-8') as f:
    for line in f.readlines():
        install_requires.append(line)

setup(
    name='sphinx-webslides-builder',

    version='0.0.1',

    description='sphinx builder that outputs webslides',

    long_description=long_description,

    url='https://github.com/creativerigor/webslides-builder',

    author='Creative Rigor, LLC',

    author_email='creativerigor@gmail.com',

    license='MIT',

    # https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
    ],

    keywords='sphinx docs documentation webslides',

    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    install_requires=install_requires,
    
    package_data={'sphinx_webslides_builder/themes/webslides_base': [
        'theme.conf',
        '*.html',
        'static/css/*.css',
        'static/js/*.js',
    ]},

    include_package_data=True,

    entry_points = {
        'sphinx.builders': [
            'webslides = sphinx_webslides_builder',
        ],
    }
)
