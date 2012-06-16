# -*- coding: utf-8 -*-

# to do - local cache abstraction

import xmlrpc.client
import getpass

username="Francis Davey"
blog_url='''http://quistis.vm.bytemark.co.uk/xmlrpc.php'''

# Perhaps include a force getting of remote?
# Do blogs get version numbered?

def password_check(func):
    def result(*args, **kwargs):
        print(kwargs.keys())
        if 'password' in kwargs:
            print('password is', kwargs['password'])
            if kwargs['password'] is None:
                kwargs['password']=getpass.getpass()
        return func(*args, **kwargs)
    return result

@password_check
def get(id, password=None):
#    if password is None:
#        password=getpass.getpass()
    s=xmlrpc.client.ServerProxy(blog_url)
    #password=getpass.getpass()

    print('getting blog with id:', id)
    rpl=s.metaWeblog.getPost(id, username, password)
    return rpl

@password_check
def put(id, content, password=None):
    s=xmlrpc.client.ServerProxy(blog_url)
    existing_post=s.metaWeblog.getPost(id, username, password)
    existing_post.update(content)
    rpl=s.metaWeblog.editPost(id, username, password, existing_post)
    return rpl
