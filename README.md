ipy_pelican
===========

IPython and Pelican tools

This project will be in flux as it's pulling from a couple different places. 

Most of the pelican/liquid stuff is taken verbatum from:

https://github.com/jakevdp/pelican-plugins/tree/liquid_tags

*Author: Jake Vanderplas <jakevdp@cs.washington.edu>*

Usage:
------

    import ipy_pelican.pelican.plugins as plugins
    PLUGINS = [plugins.notebook, plugins.include_code]
