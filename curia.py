import mechanize
import re

br=mechanize.Browser()
br.open("http://curia.europa.eu/jcms/jcms/j_6/")
br.select_form(nr=2) # the search form
br["numero_affaire"]="C-237/10"
response=br.submit()
info=response.info()
body=response.read()

m1=re.search('''<span\s*class="decision_links"''', body)
m2=re.search('''href="([^"]*)"''', body[m1.end():])

newurl=m2.group(1)
response2=br.open(newurl)
info2=response2.info()
body2=response2.read()

s="Advocate.General"
ss='''(?i)<h3>{0}[^<]*</h3>[^<]*<p>\s*</?p>[^<]*<p>([^<]*)</p>'''.format(s)
mobj=re.search(ss, body)

#http://curia.europa.eu/juris/documents.jsf?lgrec=en&language=en&num=C-406%252F09&page=1

#http://curia.europa.eu/juris/liste.jsf?pro=&lgrec=en&nat=&oqp=&dates=&lg=&language=en&jur=C%2CT%2CF&cit=none%252CC%252CCJ%252CR%252C2008E%252C%252C%252C%252C%252C%252C%252C%252C%252C%252Ctrue%252Cfalse%252Cfalse&num=C-6%252F89&td=ALL&pcs=O&avg=&page=1&mat=or&jge=&for=&cid=210435

#http://curia.europa.eu/juris/fiche.jsf?id=C%3B406%3B9%3BRP%3B1%3BP%3B1%3BC2009%2F0406%2FJ&pro=&lgrec=en&nat=&oqp=&dates=&lg=&language=en&jur=C%2CT%2CF&cit=none%252CC%252CCJ%252CR%252C2008E%252C%252C%252C%252C%252C%252C%252C%252C%252C%252Ctrue%252Cfalse%252Cfalse&num=C-406%252F09&td=ALL&pcs=O&avg=&mat=or&jge=&for=&cid=218015

#http://curia.europa.eu/juris/fiche.jsf?pro=&lgrec=en&nat=&oqp=&dates=&lg=&language=en&num=C-406%252F09&td=ALL&pcs=O&avg=&mat=or&jge=&for=&cid=218015

#http://curia.europa.eu/juris/liste.jsf?language=fr&jur=C,T,F&num=C-162/10&td=ALL#

#http://curia.europa.eu/juris/liste.jsf?language=en&num=C-162/10
