ipy_pelican
===========

IPython and Pelican tools

This project will be in flux as it's pulling from a couple different places. 



Proper Credit
-------------
Most of the pelican/liquid stuff was taken from Jake Vanderplas' [pelican-plugins branch](https://github.com/jakevdp/pelican-plugins/tree/liquid_tags)


Usage:
------
**pelican.conf**

    import ipy_pelican.pelican.plugins as plugins
    PLUGINS = [plugins.notebook, plugins.include_code]

**Markdown**

    {% notebook /a/long/path/outside/of/pelican/content.ipynb cells[3:5] name:renamed.ipynb refresh:False %}

*   notebook has been modified so that it can reference notebooks outside of the Pelican/content directory. What it does is copy the file over so it can be committed. 
*   You can rename the file by using the name attribute, this is for making a point-in-time copy of the notebook, since it may change later and mess up the cells range. 
*   refresh controls whether building the article will overwrite the local copy, useful for when you're modifying the notebook and article in tandem. 

Image Files
-----------
This version will output the Notebook figures as files and references them in the body. The notebook images will be places in output/nb_assets/*notebook_name* 

NOTE: You have to turn off Output Directory deletion for this to work. The image files are generated in a step **before** the clean_output function is called in pelican. https://github.com/getpelican/pelican/issues/927 references change the ordering in pelican. Until then, 

    DELETE_OUTPUT_DIRECTORY = True

will wipe out the nb_assets. 

Notes
------

All of this works for me locally. I'm running the dev of nbconvert, which is in flux atm. I'll try to keep this tracked to the latest version. 

Tips
-----
I have a Mercurial hook to prevent me from comitting refresh:True. 

    [hooks]
    pretxncommit.refresh = python:ipy_pelican.refresh_check.check_refresh_hook
    
