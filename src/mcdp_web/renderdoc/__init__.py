# -*- coding: utf-8 -*-
"""

    create Tag
    
        Tag(name="P", attrs={'class':class}))
        
    use add_class
    
    
    to get all the string inside, use:
        
        s = " ".join(element.strings) # note: strings
        
    Because if <p>ciao<span>come</span></p>
    then p.string is None.
    
    
    Search by ID:
    
        element = soup.find("tagName", id='lookfor'})
        if element is not None:
            
            
    Use e.attrs --- it's a dict:
    
        if 'href' in tags.attrs:
            ...
        if tag.has_attr('href':
            ...
        if 'specific' == tag.attr.get('href', 'missing'):
            ...

"""