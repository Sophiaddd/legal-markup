# -*- coding: utf-8 -*-
# Companies Act 1980 (c.22) is not available on the opsi site
# could the hansard site at millbank systems be of assistance?


# Sample feed <entry>
'''<entry>
			<id>http://www.legislation.gov.uk/id/ukpga/1988/46</id>
			<title>European Communities (Finance) Act 1988 (repealed 16.1.1995)</title>
			<link rel="self" href="http://www.legislation.gov.uk/id/ukpga/1988/46"/>
			<link href="http://www.legislation.gov.uk/ukpga/1988/46/1995-01-16"/>
			<link rel="alternate" type="application/xml" href="http://legislation.data.gov.uk/ukpga/1988/46/1995-01-16/data.xml" title="XML"/><link rel="alternate" type="application/rdf+xml" href="http://legislation.data.gov.uk/ukpga/1988/46/1995-01-16/data.rdf" title="RDF/XML"/><link rel="alternate" type="application/xhtml+xml" href="http://legislation.data.gov.uk/ukpga/1988/46/1995-01-16/data.htm" title="HTML snippet"/><link rel="alternate" type="application/pdf" href="http://legislation.data.gov.uk/ukpga/1988/46/1995-01-16/data.pdf" title="PDF"/>
			<link rel="http://purl.org/dc/terms/tableOfContents" type="application/xml" href="http://www.legislation.gov.uk/ukpga/1988/46/contents" title="Table of Contents"/>
			<author><name/></author>
			<updated>2011-07-05T00:59:59+01:00</updated>
			<published>1988-11-15T00:00:00+01:00</published>
			<ukm:DocumentMainType Value="UnitedKingdomPublicGeneralAct"/><ukm:Year Value="1988"/><ukm:Number Value="46"/><ukm:ISBN Value="0105446882"/><ukm:CreationDate Date="1988-11-15"/>
			
			
			<category term="European Union"/>
			<summary>An Act to amend the definition of “the Treaties” and “the Community Treaties” in section 1(2) of the European Communities Act 1972 so as to include the decision of 24th June 1988 of the Council of the Communities on the Communities' system of own resources and the undertaking by the Representatives of the Governments of the member States, as confirmed at their meeting within the Council on 24th June 1988 in Luxembourg, to make payments to finance the Communities' general budget for the financial year 1988.</summary>
		</entry><entry>'''

#

#import urllib.request
import xml.etree.ElementTree

import network
import data

xmlns={ 'atom' : '{http://www.w3.org/2005/Atom}',
        'xhtml' : '{http://www.w3.org/1999/xhtml}',
        'xml' : '{http://www.w3.org/XML/1998/namespace}'}

def year2actlist(year, sort):
#    url='''http://www.legislation.gov.uk/ukpga/{0}/data.feed'''.format(year)
#    s=network.get(url)
#    e=xml.etree.ElementTree.fromstring(s)
#    print('Testing...''')
#    print(xmlns['atom'])
#    entries=e.findall('.//{atom}entry'.format(**xmlns))
#    result=[]
#
#    for e in entries:
#        #print('#', e)
#        result.append(e.find('{atom}title'.format(**xmlns)).text)
#

    if sort=='act':
        sort_code='ukpga'
    elif sort in ['regulations', 'order']:
        sort_code='uksi'
    else:
        raise Exception("Unknown sort".format(sort))
    result=[]
    url='''http://www.legislation.gov.uk/{1}/{0}/data.feed'''.format(year, sort_code)
    n=1
    for page in network.atom_feed(url):
        entries=page.findall('{atom}entry'.format(**xmlns))
        for entry in entries:
            title_element=entry.find('{atom}title'.format(**xmlns))
            en_titles=entry.findall("{atom}title/{xhtml}div/{xhtml}span[@{xml}lang='en']".format(**xmlns))
            if len(en_titles) > 0:
                title=en_titles[0].text
            else:
                title=title_element.text
            if title is None or len(title)==0:
                print(n)
                print(page)
                sys.exit()
            href=entry.find("{atom}link[@rel='self']".format(**xmlns)).attrib['href']
            title=data.normalise_title(title)
            result.append(data.ActInfo(title, year, href, sort))
        n=n+1
    return result

