# -*- coding: utf-8 -*-

import re

def group_search(L, s, end):
    '''Searches for a match between one element of L ending at position
    end in the string s.

    '''
    for x in L:
        pat=re.compile(x + '$', re.I)
        mobj=pat.search(s, endpos=end)
        if mobj is not None:
            return mobj
    return None

def match_maker(pattern):
    pat=re.compile(pattern)
    def match(func):
        def result(s):
            mobj=pat.search(s)
            if mobj:
                return(func(mobj))
        return result
    return match

def rule_maker(name, pattern):
    pat=re.compile(pattern)
    def rule(func):
        def result(s, log):
           for mobj in pat.finditer(s):
               replacement=func(mobj)
               log.append ((name, mobj.start(), mobj.end(), replacement))

           return(s, log)
        return result
    return rule

def complex_rule_maker(pattern):
    pat=re.compile(pattern)
    def rule(func):
        def result(s, log):
            for mobj in pat.finditer(s):
                l=func(mobj)
                log.append(l)
            return(s, log)
        return result
    return rule

def collapse(s, log):
    # assumes no conflicts at the moment
    log_s=sorted(log, key=lambda l: l[1])
    result=[]
    last=0
    print(log_s)
    for l in log_s:
        (name, start, end, replacement)=l
        if end is None or (last > 0 and last >= start):
            continue
        result.append(s[last:start])
        #print('''#### last={0}, start={1}'''.format(last, start))
        #print(s[last:start])
        result.append(replacement)
        last=end
    result.append(s[last:])

    return ''.join(result)

# simple_rule: matching object => replacement string for that object
# if match, mat


# (rule_name, start, end, replacement)
