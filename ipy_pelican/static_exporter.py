import os.path

from IPython.utils.traitlets import Unicode

from nbconvert.exporters import fullhtml
from IPython.config import Config

TEMPLATE_PATH = os.path.dirname(os.path.realpath(__file__)) + '/templates'

class FullHtmlStaticExporter(fullhtml.FullHtmlExporter):
    """
    Exports a full HTML document with display assets outputted to files
    """
    _default_config = Config({
        'ExtractFigureTransformer':{'enabled':True},
        'CSSHtmlHeaderTransformer':{'enabled':True}
    }) 
    
    template_file = Unicode(
            'static_fullhtml', config=True,
            help="Name of the template file to use")    

    def __init__(self, *args, **kwargs):
        super(FullHtmlStaticExporter, self).__init__(*args, **kwargs)

        # environment should be created in Exporter.__init__
        # add our module specific template path
        self.environment.loader.searchpath.append(TEMPLATE_PATH)
