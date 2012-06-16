# -*- coding: utf-8 -*-

# Eats a bailii file and gets information from it
#

# Reference:
# Neutral Citation
# http://www.lexum.com/ccc-ccr/neutr/neutr.jur_en.html


# http://www.austlii.edu.au/techlib/standards/mnc.html
# http://www.bailii.org/bailii/citation.html


import os
import re
import data
from matching import match_maker

def normalise_party(s):
    '''Normalises a case title'''

    (s, N)=re.subn('(?is)&amp;\s*(Anor|Ors)\s*$', '', s)
    (s, N)=re.subn('(?is)(Ltd|GmbH)\s*$', '', s)
    s=s.strip()
    return(s)
    

@match_maker('<title>(.*?)</title>')
def title(m):
    raw=m.group(1)
    (name, ref, _ )=re.split('(\[\d{4}.*)', raw)
    A=re.split(' v ', name)
    for i in range(0, len(A)):
        A[i]=normalise_party(A[i])
    (first, second)=A
        
    return {'title': dict(raw=raw, name=name, ref=ref, first=first, second=second)}

divisions={
    'c': 'chancery',
    'q' : 'queens bench', 
    'f' : 'family'}

@match_maker('(?is)<court>(.*?)</court>')
def court(m):
    court_data=m.group(1)
    C=[None]*3
    if re.search('(?is)high court of justice', court_data):
        C[0]='ew'
        C[1]='hc'
        C[2]='?'
        for key in divisions:
            value=divisions[key]
            if re.search('(?is){0}\s*division'.format(value), court_data):
                C[2]=key
    return {'court' : C }

@match_maker('(?is)URL:\s*<i>(.*?)</i>')
def url(m):
    return {'url' : m.group(1) }

@match_maker('Neutral Citation Number: \[(\d{4})]\ ([A-Z]{4})( [a-zA-Z]+)? (\d+)( \([a-zA-Z]+\))?')
def neutral_citation(m):
    year=m.group(1)
    g3=m.group(3)
    if g3 is not None:
        court=m.group(2) + ' ' + g3.strip()
    else:
        court=m.group(2)

    g5=m.group(5)
    if g5 is not None:
        ssc=m.group(5).strip()
    else:
        ssc=None
    
    C=data.Neutral_Citation(year, court, m.group(4), ssc)

    return {'neutral_citation' : C.dump() , 'citation': C.dump()}
    

def get(filename):
    html_file=open(filename, 'r')
    html=html_file.read()

    return html

def parse(html):
    D={}

    D.update(title(html))
    D.update(url(html))
    D.update(court(html))
    D.update(neutral_citation(html))

    return (D)

def parse_file(filename):
    html=get(filename)
    return parse(html)
