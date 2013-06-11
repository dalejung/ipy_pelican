{%- extends 'fullhtml.tpl' -%}

{%- block header -%}<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>[{{nb.metadata.name}}]</title>
{% for css in resources.inlining.css -%}
<style type="text/css">
{{css}}
</style>
{% endfor %}

<style type="text/css">
/* Overrides of notebook CSS for static HTML export */
body {
  overflow: visible;
  padding: 8px;
}
.input_area {
  padding: 0.4em;
}

pre {
    border: none;
    margin: 0px;
    font-size: 13px;
}

pre.ipynb {
   color: black;
   background: #f7f7f7;
   border: 0;
   box-shadow: none;
   margin-bottom: 0;
   padding: 0;
}

div.ipynb {
    font-size: 15px;
}

/* Need higher precedence to override pelican main.css */
div.ipynb .rendered_html table, 
div.ipynb .rendered_html table tr, 
div.ipynb .rendered_html table th, 
div.ipynb .rendered_html table td 
{
    border: 1px solid black;
    border-collapse: collapse;
    margin: 1em 2em;
    padding: 4px;
}
</style>

<script src="https://c328740.ssl.cf1.rackcdn.com/mathjax/latest/MathJax.js?config=TeX-AMS_HTML" type="text/javascript">

</script>
<script type="text/javascript">
init_mathjax = function() {
    if (window.MathJax) {
        // MathJax loaded
        MathJax.Hub.Config({
            tex2jax: {
                inlineMath: [ ['$','$'], ["\\(","\\)"] ],
                displayMath: [ ['$$','$$'], ["\\[","\\]"] ]
            },
            displayAlign: 'left', // Change this to 'center' to center equations.
            "HTML-CSS": {
                styles: {'.MathJax_Display': {"margin": 0}}
            }
        });
        MathJax.Hub.Queue(["Typeset",MathJax.Hub]);
    }
}
init_mathjax();
</script>
</head>
{%- endblock header -%}

{% block data_png %}
{% if output.key_png %}
<img src="{{output.key_png}}">
{% else %}
<img src="data:image/png;base64,{{output.png}}">
{% endif %}
{%- endblock data_png %}

