import time
import json

def format_json(json_file, string,type):
    j = json.load(open(json_file))      #读取文件
    i =0
    d = {}
    d1={}
    d1['date']=[]
    d1['temperature']=[]
    for key in j:
        key1 = string[i]
        list1123=list(key1)
        list1123.insert(2,'-')
        key1=''.join(list1123)
        i = i+1
        d[key1] = j[key]

    for key in d:
        d1['date'].append(key)
        d1['temperature'].append(d[key])
    jsObj = json.dumps(d1)
    fileObject = open(type+'.json', 'w')
    fileObject.write(jsObj)
    fileObject.close()


    return j
