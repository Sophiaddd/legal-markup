import wordpress

local_in=open('temp-local-copy.html', 'r', encoding='utf-8')
local_copy=local_in.read()

content={
    'description' : local_copy
    }

wordpress.put(17, content, password='jb6drmq5')
