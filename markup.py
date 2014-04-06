# -*- coding: utf-8 -*-

import re
import matching
import urllib
import data
import sys
from matching import rule_maker, complex_rule_maker

def diagnostic(s, start, end):
    return s[max(0, start-24) : min(len(s)-1, start+24)]

def html_link(href, content):
    '''Creates html for a hyperlink to href.'''

    return('''<a href="{0}">{1}</a>'''.format(href, content))

def markdown_link(href, content):
    '''Creates a link in the markdown language.'''

    return('''[{0}]({1})'''.format(content, href))

@rule_maker('wikipedia', '''(?is)(wikipedia article) ((?P<q>"|&quot;|')(.*?)(?P=q))''')
def wikipedia(m, link):
    #link=html_link
    s=m.group(4)
    r=s[0].upper() + s[1:].lower()
    (r, N)=re.subn(' ', '_', r)

#    '''"
#    print(("s=[{0}]\nr=[{1}]".format(s,r)))
#    print(("g3=[{0}]".format(m.group(3))))
#    print((m.group('q')))
    #return '{0} &quot;<a href="http://en.wikipedia.org/wiki/{1}" class="wikipedia">{2}</a>&quot;'.format(m.group(1), r, s)
    #
    return '{0} &quot;{hyperlink}&quot;'.format(m.group(1), hyperlink=link(r, s))

# '(?is)act\s*(\d{4}'
#@complex_rule_maker('(?is)(?P<sort>act|regulations|order)\s*(?P<year>\d{4})')
#def act(m):
#    mg=m.groupdict()
#    year=mg['year']
#    sort=mg['sort'].lower()
#    s=m.string
#    diagnostic_string=diagnostic(s, m.start(), m.end())
#    print("act:", diagnostic_string)
#    (actdict, actlist)=data.acts_by_year(year, sort)
#    escaped_act_titles=map(lambda act: re.escape(act.title_prefix), actlist )
#    pat_string='|'.join(escaped_act_titles) + '$'
#    pat=re.compile(pat_string, re.I)
#    mobj=pat.search(s, endpos=m.end())
#    if mobj is None:
#        #print(pat_string)
#        #print(year)
#        print('''Unrecognised act reference: {0}'''.format(s[m.start()-16:m.end()+16]))
#        return('ukpga', -1, None,  diagnostic_string)
#    act_name='{0} Act {1}'.format(mobj.group(0), year)
#    act=actdict[act_name]
#    href=act.href
#    return ('ukpga', mobj.start(), m.end(), '''<a href="{0}">{1}</a>'''.format(href, act.cite()))
#

@complex_rule_maker('(?is)(?P<sort>act|regulations|order)\s*(?P<year>\d{4})')
def act(m, link):
    #link=html_link
    s=m.string
    mg=m.groupdict()
    year=mg['year']
    sort=mg['sort'].lower()
    diagnostic_string=diagnostic(s, m.start(), m.end())
    (actdict, actlist)=data.acts_by_year(year, sort)
    print(actlist)
    print(sort, year)
    print([x for x in map(lambda act: act.name, actlist)])
    i=0
    for name in map(lambda act: act.name, actlist):
        print("Name:", i, name)
        print(actlist[i].href, actlist[i].name)
        print(re.escape(name))
        i=i+1

    escaped_act_titles=map(lambda act: re.escape(act.name), actlist )

#    pat_string='|'.join(escaped_act_titles) + '$'
#    pat=re.compile(pat_string, re.I)
#    mobj=pat.search(s, endpos=m.end())
    mobj=matching.group_search(escaped_act_titles, s, m.end())
    if mobj is None:
#        #print(pat_string)
#        #print(year)
        print('''Unrecognised act reference: {0}'''.format(s[m.start()-16:m.end()+16]))
        return('ukpga', -1, None,  diagnostic_string)
#    act_name='{0} Act {1}'.format(mobj.group(0), year)
    act=actdict[mobj.group(0)]
    href=act.href
    #return ('ukpga', mobj.start(), m.end(), '''<a href="{0}">{1}</a>'''.format(href, mobj.group(0)))
    return ('ukpga', mobj.start(), m.end(), link(href, mobj.group(0)))
#    

def transform(html, link=html_link):
   log=[]
   #link=markdown_link#html_link
   (html, log) = wikipedia(html, log, link)
   (html, log) = act(html, log, link)
   #print log
   return matching.collapse(html, log)

