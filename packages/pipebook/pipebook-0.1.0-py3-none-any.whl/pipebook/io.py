from toga.sources import TreeSource
import yaml

KEYS="level,name,typeof,size,value".split(',')

def d(l,n,t,s,v=""): return {"level": l, "name": n, "typeof": t, "size":s, "value": v}

def typeof(value): return type(value).__name__

def is_num(t): return t == "float" or t == "int" or "date" in t

def obj2tree(yml):
    s = len(yml)
    roots = [d(0,key,"dict",s) for key in yml]
    source = TreeSource(data=roots, accessors=roots[0].keys())
    for root in source._roots:
        append_dict(1, root, yml[root.name])
    return source

def append_dict(l, root, dobj):
    print(root.name)
    for k,v in dobj.items():
        t = typeof(v)
        s = len(v) if not is_num(t) else "-"
        child = root._source.append(root, **d(l, k, t, s, v))
        #print(f'dict[{l}]: {k}<{t}>')
        if ('dict' == t):
            append_dict(l+1, child, v)
        elif ('list' == t):
            append_list(l+1, child, v)

def append_list(l, root, lobj):
    print(root.name)
    for k,v in enumerate(lobj):
        t = typeof(v)
        s = len(v) if not is_num(t) else "-"
        child = root._source.append(root, **d(l, k, t, s, v))
        #print(f'list[{l}]: {k}<{t}>')
        if ('dict' == t):
            append_dict(l+1, child, v)
        elif ('list' == t):
            append_list(l+1, child, v)
