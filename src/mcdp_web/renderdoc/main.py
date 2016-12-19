# -*- coding: utf-8 -*-
from contracts import contract
from contracts.utils import raise_desc, indent
from mcdp_library import MCDPLibrary

from .highlight import html_interpret
from .markd import render_markdown
from .prerender_math import prerender_mathjax, PrerenderError
from mcdp_library_tests.tests import timeit_wall
from mcdp_web.renderdoc.highlight import mark_console_pres,\
    escape_ticks_before_markdown, escape_for_mathjax
import re
from mcdp_web.renderdoc.latex_preprocess import latex_preprocessing


__all__ = ['render_document']

@contract(returns='str', s=str, library=MCDPLibrary, raise_errors=bool)
def render_complete(library, s, raise_errors, realpath, generate_pdf=False):
    """
        Transforms markdown into html and then renders the mcdp snippets inside.
        
        s: a markdown string with embedded html snippets
        
        Returns an HTML string; not a complete document.
    """
    if isinstance(s, unicode):
        msg = 'I expect a str encoded with utf-8, not unicode.'
        raise_desc(TypeError, msg, s=s)

    # save the '\\' in mathjax before markdown
#     s = s.replace('\\\\', 'MATHJAX_BARBAR')
    
    # fixes for LaTeX
    s = latex_preprocessing(s)
    
    s = '<div style="display:none">Because of mathjax bug</div>\n\n\n' + s

    # cannot parse html before markdown, because md will take
    # invalid html, (in particular '$   ciao <ciao>' and make it work)
     
#     s = escape_ticks_before_markdown(s)
    s = s.replace('>`', '>&#96;')
#     print(indent(s, 'before markdown | '))
    
    s = render_markdown(s)
    
    # this escapes $ to DOLLAR
    s = escape_for_mathjax(s)
#     print(indent(s, 'before prerender_mathjax | '))
    # mathjax must be after markdown because of code blocks using "$"
    s = prerender_mathjax(s)
    
    
#     print(indent(s, 'after prerender_mathjax | '))
    
    
#     print(indent(html, 'after render_markdown'))

    html  = s
    html = html.replace('<p>DRAFT</p>', '<div class="draft">')
    
    html = html.replace('<p>/DRAFT</p>', '</div>')
    
    html = mark_console_pres(html)

#     print '\nafter render_markdown: %s' % html
    html2 = html_interpret(library, html, generate_pdf=generate_pdf,
                           raise_errors=raise_errors, realpath=realpath)

    from mcdp_report.gg_utils import embed_images_from_library
    html3 = embed_images_from_library(html=html2, library=library)
    
#     print '\nafter embed_images_from_library: %s' % html3
    
    
#     html3 = html3.replace('MATHJAX_BARBAR', '\\\\')
    
#     
#     if '$$' in html3 or '$' in html3:
#         try:
#             with timeit_wall('prerender_mathjax'):
#                 html4 = prerender_mathjax(html3)
#         except PrerenderError:
#             raise
#     else:
#         html4 = html3
#     print '\nafter prerender_mathjax: %s' % html4

    
    
#     html5 = html5.replace('~', '&nbsp;') 
    
    return html3
