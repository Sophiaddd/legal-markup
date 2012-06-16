import csv
import opsi
import re

def toCitation(d):
    '''converts a dict to a Citation object'''
    
    return Citation(**d)

class Citation(object):
    def __init__(self, jurisdiction, sort, year, year_ref, N1, col, N2, annot, internal=None):
        self.jurisdiction=jurisdiction
        self.sort=sort
        self.year=year
        self.year_ref=year_ref
        self.N1=N1
        self.col=col
        self.N2=N2
        self.annot=annot
        self.internal=internal

    def dump(self):
        return {            
                'jurisdiction' : self.jurisdiction,
                'sort' : self.sort,
                'year' : self.year,
                'year_ref' : self.year_ref,
                'N1' : self.N1,
                'col' : self.col,
                'N2' : self.N2,
                'annot' : self.annot,
                'internal' : self.internal
                }
                

class Neutral_Citation(Citation):
    def __init__(self, year, court, number, subcourt, internal=None):
        super(Neutral_Citation, self).__init__('uk', 'neutral', year, True, None, court, number, subcourt, internal)

    def __str__(self):
        if subcourt is not None:
            s1=' ({0})'.format(subcourt)
        else:
            s1=''
        if internal is not None:
            s2=' ({0})'.format(internal)
        else:
            s2=''

        return '''[{0}] {1} {2}{3}{4}'''.format(year, court, number, s1, s2)

class Datastore(object):
    def __init__(self):
        pass

class Cases(Datastore):
    def __init__(self):
       super(Datastore, self).__init__()
       
       # get data from csv store

       # create indexes
 
    def get_case(self, first, second, year):
        '''Finds a case based on the first and second parts of its party list'''
        
        pass

class Info(object):
    def __init__(self, name, href):
        '''Name is the name the object will go by in text, href a link
        to a resource for that object.'''

        self.name=name
        self.href=href

class ActInfo(Info):
    def __init__(self, title, year, href, sort='act'):
        super().__init__(title, href)
        self.sort=sort
        self.year=year
#        self.title_prefix=truncate_act_title(year, title)

#    def cite(self):
#        Sort=self.sort[0].upper() + self.sort[1:]
#        return '''{0} {1} {2}'''.format(self.title_prefix, Sort, self.year)
#
#def truncate_act_title(year, t):
#    print('''t={0}, year={1}'''.format(t, year))
#    (t, N)=re.subn('(?i)\s*\(repealed[ .0-9]*\)\s*$', '', t)
#    (t, N)=re.subn('(?i)\s*(Act|Measure|Regulations|Order|Rules|Scheme|Resolution)\s*(\(Scotland|England|Wales|Northern Ireland\)){0}\s*$'.format(year), '', t)
#    if not N==1:
#        if re.search('Rules of the Supreme Court', t):
#            return t[:-5] # we aren't going to deal with this special case right now
#        raise Exception("Could not truncate [{0}] for year [{1}]".format(t, year))   
#
#    return t

def normalise_title(t):
    '''Removes 'the' from the start of a title to use as a key or a match.'''
    
    return re.sub('(?i)^the\s*', '', t)

def acts_by_year(year, sort):
    L=opsi.year2actlist(year, sort)
    print(len(L))
#    if sort!='act':
#        sys.exit()
    D={}
    for a in L:
        key=normalise_title(a.name)
        D[key]=a

    return(D, L)
