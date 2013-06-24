import ipy_pelican.pelican.notebook as nb

markup = "/abs/path/to/notebook.ipynb cells[0:] name:some_name.ipynb refresh:True"

vars = nb._vars(markup)
assert vars['start'] == 0
assert vars['end'] is None 
assert vars['refresh'] is True 
assert vars['name'] == 'some_name.ipynb'
assert vars['src'] == '/abs/path/to/notebook.ipynb'

markup = "/abs/path/to/notebook.ipynb name:some_name.ipynb refresh:True"

vars = nb._vars(markup)
assert 'start' not in vars
assert 'end' not in vars
assert vars['refresh'] is True 
assert vars['name'] == 'some_name.ipynb'
assert vars['src'] == '/abs/path/to/notebook.ipynb'

markup = "/abs/path/to/notebook.ipynb name:bob cells[:10]"

vars = nb._vars(markup)
assert vars['start'] is None
assert vars['end'] == 10
assert vars['name'] == 'bob'
assert vars['src'] == '/abs/path/to/notebook.ipynb'

# out of order
markup = "/abs/path/to/notebook.ipynb refresh:True name:some_name.ipynb cells[0:]"

vars = nb._vars(markup)
assert vars['start'] == 0
assert vars['end'] is None 
assert vars['refresh'] is True 
assert vars['name'] == 'some_name.ipynb'
assert vars['src'] == '/abs/path/to/notebook.ipynb'

#output_only
markup = "/abs/path/to/notebook.ipynb refresh:True name:some_name.ipynb cells[0:] output_only:True"

vars = nb._vars(markup)
assert vars['start'] == 0
assert vars['end'] is None 
assert vars['refresh'] is True 
assert vars['name'] == 'some_name.ipynb'
assert vars['src'] == '/abs/path/to/notebook.ipynb'
assert vars['output_only'] is True 
