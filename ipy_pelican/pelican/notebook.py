"""
Notebook Tag
------------
This is a liquid-style tag to include a static html rendering of an IPython
notebook in a blog post.

Syntax
------
{% notebook filename.ipynb [ cells[start:end] ]%}

The file should be specified relative to the ``notebooks`` subdirectory of the
content directory.  Optionally, this subdirectory can be specified in the
config file:

    NOTEBOOK_DIR = 'notebooks'

The cells[start:end] statement is optional, and can be used to specify which
block of cells from the notebook to include.

Details
-------
Because the conversion and formatting of notebooks is rather involved, there
are a few extra steps required for this plugin:

- First, the plugin requires that the nbconvert package [1]_ to be in the
  python path. For example, in bash, this can be set via

      >$ export PYTHONPATH=/path/to/nbconvert/

- After typing "make html" when using the notebook tag, a file called
  ``_nb_header.html`` will be produced in the main directory.  The content
  of the file should be included in the header of the theme.  An easy way
  to accomplish this is to add the following lines within the header template
  of the theme you use:

      {% if EXTRA_HEADER %}
        {{ EXTRA_HEADER }}
      {% endif %}

  and in your ``pelicanconf.py`` file, include the line:

      EXTRA_HEADER = open('_nb_header.html').read().decode('utf-8')

[1] https://github.com/ipython/nbconvert
"""
import re
import os
from mdx_liquid_tags import LiquidTags
from ipy_pelican.util import copy_content, mkdir_p
import ipy_pelican.export as he
from bs4 import BeautifulSoup

separate_available = False

SYNTAX = "{% notebook /path/to/notebook.ipynb [ cells[start:end] ] [name:None] [refresh:False] %}"
FORMAT = re.compile(r"""^(\s+)?(?P<src>\S+)(\s+)?((cells\[)(?P<start>-?[0-9]*):(?P<end>-?[0-9]*)(\]))?(\s+)?(?:(?:name:)(?P<name>\S+))?(?:\s+)?(?:(?:refresh:)(?P<refresh>\S+))?(?:\s+)?$""")


def process_body(body):
    body = '\n'.join(body)

    # replace the highlight tags
    body = body.replace('highlight', 'highlight-ipynb')

    # specify <pre> tags
    body = body.replace('<pre', '<pre class="ipynb"')

    # create a special div for notebook
    body = '<div class="ipynb">\n\n' + body + "\n\n</div>"

    # specialize headers
    for h in '123456':
        body = body.replace('<h%s' % h, '<h%s class="ipynb"' % h)
    
    return body.split('\n')


def process_header(header):
    header = '\n'.join(header)

    # replace the highlight tags
    header = header.replace('highlight', 'highlight-ipynb')

    # specify all headers
    R = re.compile(r'^(h[1-6])', re.MULTILINE)
    repl = lambda match: '.ipynb ' + match.groups()[0]
    header = R.sub(repl, header)

    # substitude ipynb class for html and body modifiers
    # Not sure this is doing anything with latest ipython
    header = header.replace('html, body', '.ipynb div,')

    return header.split('\n')

@LiquidTags.register('notebook')
def notebook(preprocessor, tag, markup):
    match = FORMAT.search(markup)
    if match:
        argdict = match.groupdict()
        src = argdict['src']
        start = argdict['start']
        end = argdict['end']
        refresh = argdict['refresh']
        name = argdict['name']
    else:
        raise ValueError("Error processing input, "
                         "expected syntax: {0}".format(SYNTAX))
    if start:
        start = int(start)
    else:
        start = None

    if end:
        end = int(end)
    else:
        end = None

    if refresh == 'True':
        refresh = True
    else:
        refresh = False

    settings = preprocessor.configs.config['settings']
    notebook_output = generate_notebook_output(settings, src, refresh=refresh, start=start, end=end, name=name)
    body_lines, header_lines, resources, asset_path = notebook_output

    # start writing out files
    mkdir_p(asset_path)
    he._write_assets(resources, asset_path)

    if not notebook.header_saved:
        notebook.header_saved = True
        print ("\n *** Writing styles to _nb_header.html: "
               "this should be included in the theme.\n")
        lines = '\n'.join(header_lines).encode('utf-8')
        open('_nb_header.html', 'w').write(lines)

    body = preprocessor.configs.htmlStash.store('\n'.join(body_lines),
                                                safe=True)
    return body
notebook.header_saved = False

def generate_notebook_output(settings, src, refresh=False, start=None, end=None, name=None):
    # copy file to local content store
    nb_dir =  settings.get('NOTEBOOK_DIR', 'notebooks')
    nb_path = copy_content(nb_dir, src, refresh=refresh, name=name)

    if not os.path.exists(nb_path):
        raise ValueError("File {0} could not be found".format(nb_path))

    # generate asset paths
    asset_path, src_dir = _asset_path(nb_path, settings)

    header_lines, body_lines, resources = process_notebook(nb_path, start=start, end=end, src_dir=src_dir)

    return body_lines, header_lines, resources, asset_path

def process_notebook(nb_path, start=None, end=None, src_dir=None):
    """
    At this point we've got all the paths figured out and explicit. 

    Generate HTML and modify it using the original process_body, process_header
    """
    # Call the notebook converter
    body, resources = he.process_html_notebook(nb_path, start=start, end=end, src_dir=src_dir)

    soup = BeautifulSoup(body)
    head = soup.find_all('head')[0]
    body = soup.find_all('body')[0]

    # nbconvert needs actual string objects
    header_lines = [unicode(line) for line in head.contents]
    body_lines = [unicode(line) for line in body.contents]

    header_lines = process_header(header_lines)
    body_lines = process_body(body_lines)
    
    return header_lines, body_lines, resources


def _asset_path(nb_path, settings):
    """
    Returns the path to save the asset files and the dir to prepend
    to <img src="{src_dir}/image.png" />
    """
    asset_dir =  settings.get('NOTEBOOK_ASSETS', 'nb_assets')
    dir, fn = os.path.split(nb_path)
    # skip content/NOTEBOOK_DIR
    dir = '/'.join(dir.split('/')[2:])
    name, ext = os.path.splitext(fn)
    src_dir = os.path.join(asset_dir, dir, name)
    asset_path = os.path.join('output', src_dir)
    return asset_path, src_dir


#----------------------------------------------------------------------
# This import allows image tag to be a Pelican plugin
from liquid_tags import register

