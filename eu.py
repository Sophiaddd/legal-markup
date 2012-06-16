#

# export PYTHONIOENCODING=utf-8
# will allow you to read the text on an xterm screen

import re
import urllib.request, urllib.parse, urllib.error
import time
import os
import csv

trace=True
file_dir='files'

# http://eur-lex.europa.eu/en/tools/TableSectors.htm
# describes descriptors.

def get_celex_doc(celex_no):
    url=mk_celex_url(celex_no)
    filepath=os.path.join(file_dir, celex_no)
    if os.path.isfile(filepath):
        if trace:
            print(("retrieving {0}".format(filepath)))
        file=open(filepath, 'r')
        return(url, file.read())
    else:
        if trace:
            print(("getting {0} ...".format(url)))
        page=urllib.request.urlopen(url)
        html=page.read()
        file=open(filepath, 'w')
        file.write(html)
        file.close()
        return(url, html)

def mk_celex_url(celex_no):
    celex_url="http://eur-lex.europa.eu/LexUriServ/LexUriServ.do?uri=CELEX:{celex_number}:{language}:NOT".format(celex_number=celex_no, language="EN")
    return celex_url

def get_page(year, case_number, doc_type):
    celex_no="{sector}{year}{descriptor}{number:0>4}".format(sector="6", year=year, descriptor=doc_type, number=case_number)
    (url, html)=get_celex_doc(celex_no)
    page_value=html
    return (url, page_value)

def page_ok(url, html):
    #need to check for "plsql" error
    # ERROR : plsql code=-2
    # in the body
    empty=re.search('''(?i)<h1>No.documents.matching.criteria''', html)
    bad=re.search('''(?i)<body>ERROR''', html)
    if empty or bad:
        if trace:
            print(("{0} no document.".format(url)))
        return False
    else:
        return True

def unpack(neutral_citation):
    (x, short_year)=re.split('/', neutral_citation)
    (court_code, case_number)=re.split('-', x)
	
    if int(short_year) < 53:
        century_prefix="20"
    else:
        century_prefix="19"
	
    year="{0}{1}".format(century_prefix, short_year)

    return(case_number, short_year, year)

def get_data(neutral_citation):
	
    (case_number, short_year, year) = unpack(neutral_citation)

    data={}
    data['neutral_citation']=neutral_citation
    data['jurisdiction']='European Union'
    data['court']='European Court of Justice'
    for i in ['ag_name', 'ag_date', 'ag_url', 'coram', 'coram_date', 'coram_url', 'long_title']:
        data[i]=None

    # Advocate General's conclusion
    (cc_url, cc)=get_page(year, case_number, "CC")

    if page_ok(cc_url, cc):
        #print("cc page ok at {0}".format(cc_url))
        mobj=re.search('''(?i)Opinion.of.((Mr|Mrs).)?Advocate.General.(.*?).delivered.on.([^<]*)''', cc)
        if mobj:
            data['ag_name']=mobj.group(3)
            ag_date_unparsed=mobj.group(4)
            t=time.strptime(ag_date_unparsed.replace('.','').strip(), "%d %B %Y")
            data['ag_date']="{0}/{1}/{2}".format(t.tm_mday, t.tm_mon, t.tm_year)
            data['ag_url']=cc_url

        #print("no cc page")

    (cj_url, cj)=get_page(year, case_number, "CJ")
    if page_ok(cj_url, cj):
        mobj=re.search('''(?i)Judgment.of.the.Court.\(([^)]*?)\).of.([^<]*)''', cj)
        data['coram']=mobj.group(1)
        coram_date_unparsed=mobj.group(2)
        t=time.strptime(coram_date_unparsed.replace('.','').strip(), "%d %B %Y")
        data['coram_date']="{0}/{1}/{2}".format(t.tm_mday, t.tm_mon, t.tm_year)
        data['coram_url']=cj_url

        #print("cj ok at {0} - {1} - {2}".format(cj_url, coram, coram_date))

    # Obtaining meta-data
    (cn_url, cn)=get_page(year, case_number, "CN")
    data['party1']=None
    data['party2']=None
    data['long_title']=None

    if page_ok(cn_url, cn):
        mobj=re.search('''(?is)<p>(\w*):([^<]*)</p>[^<]*<p>(\w*):([^<]*)''', cn)
        if mobj:
            role1=mobj.group(1)
            data['party1']=mobj.group(2)
            role2=mobj.group(3)
            data['party2']=mobj.group(4)
            data['long_title']='''{0} v {1}'''.format(data['party1'], data['party2'])
    
    # fixup - lets hope there aren't too many of these.
#    if year==2010 and case_number==406:
#        ag="Bot"
#        ag_date="29/11/2022"

    #return(neutral_citation, coram_url, coram, coram_date, ag_url, ag, ag_date, long_name)
    return data

def bulk_get(L):
    result_list=[]
    
    for neutral_citation in L:
        result={}
        print(neutral_citation)
        (case_number, short_year, year)=unpack(neutral_citation)
        result['celex_document_data']=get_data(neutral_citation)
        result['curia_list_data']=get_curia_list(case_number, short_year)
        result['curia_status_data']=get_curia_status(case_number, short_year)
        result_list.append(result)
    return result_list

def get_curia_list(case_number, short_year):
    curia_url='''http://curia.europa.eu/juris/documents.jsf?lgrec=en&language=en&num=C-{0}%252F{1}&page=1'''.format(case_number, short_year)
    page=urllib.request.urlopen(curia_url)
    table=[]
    html=page.read()
    pat=re.compile('''<tr\s*class="table_document_ligne"[^>]*>\s*''')
    s=html
    mobj=pat.search(s)
    while mobj:
        row=[]
        s=s[mobj.end():]
        # eat td's
        tdpat=re.compile('''<td[^>]*>(.*?)</td>\s*''')
        tdmatch=tdpat.match(s)
        while tdmatch:
            row.append(tdmatch.group(1).strip())
            s=s[tdmatch.end():]
            tdmatch=tdpat.match(s)
        linkmatch=re.match('''<td[^>]*>\s*<div\s*id="docHtml"[^>]*.*?<a.*?href="([^"]*)"''',s)
        if linkmatch:
            url=linkmatch.group(1)
#            info=parse_curia_info(url)
#            row.append(info)
            row.append(url)
        else:
#            row.append(None)
            row.append(None)
        table.append(row)
        mobj=pat.search(s)
        
    return table

def get_curia_status(case_number, short_year):
    info={}
    url='''http://curia.europa.eu/juris/liste.jsf?language=en&num=C-{0}/{1}'''.format(case_number, short_year)
    result_page=urllib.request.urlopen(url)
    result_html=result_page.read()
    mobj= re.search('''href="([^"]*)"[^>]*>[^<]*<img[^>]*title="Case\s*information''', result_html)
    if mobj:
        info_url=mobj.group(1)
    else:
        return info
    page=urllib.request.urlopen(info_url)
    html=page.read()
    mobj=re.search('''(?is)<h3>Advocate.General[^<]*</h3>(.*?)<h3>''', html)
    if mobj:
        x=re.sub('''<[^>]*>''', '', mobj.group(1))
        x=re.sub('''\n''', '', x)
        x=x.strip()
        info['ag_name']=x
    return(info)

def normalise(result):
    info=result['celex_document_data']
    if info['ag_name'] is None:
        info['ag_name']=result['curia_status_data']['ag_name']
    if info['ag_date'] is None:
        curia_list_data=result['curia_list_data']
        oplist=[x for x in curia_list_data if re.search('(?i)Opinion', x[1])]
        if oplist:
            ag_date=oplist[0][2]
    return result

def display(result):
    info=result['celex_document_data']
    print('''{coram_url}, {ag_name}, {ag_url}, {ag_date}, {long_title}, {neutral_citation}, 'European Union' , 'European Court of Justice', {coram}, {coram_date}'''.format(**info))

def write(result_list):
    writer=csv.DictWriter(open('output.csv', 'w'), ['coram_url', 'ag_name', 'ag_url', 'ag_date', 'long_title', 'neutral_citation', 'jurisdiction' , 'court', 'coram', 'coram_date'], extrasaction="ignore")


    for result in result_list:
        info=result['celex_document_data']
        writer.writerow(info)
        
copyright_cases_2011=['C-283/10', 'C-70/10', 'C-431/09', 'C-403/08', 'C-324/09', 'C-271/10', 'C-168/09', 'C-406/10', 'C-162/10', 'C-145/10', 'C-462/09']
cc2011=copyright_cases_2011 

