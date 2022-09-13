#!/usr/bin/env python
# coding=utf-8
import requests,json
from json import dumps
import socket
import os
import platform
import re
import sys
import pyinotify
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import threading
import time
filename='/var/tmp/exit.log'
thread_load='./config_command.log'
config_command='./config_command.log'
max_line=10
listen_time=5.8
directories = []
class config_change:
    def file_check_exist(self):
        if os.access("./config.py", os.F_OK):
            with open('./config.py', 'r', encoding='utf-8') as f:
                lines = f.readlines()
                global URL 
                URL = str(lines[1].split('\'')[1])
                global IPHONE_NUMBER
                IPHONE_NUMBER1 = lines[0].strip('\n')
                IPHONE_NUMBER = str(IPHONE_NUMBER1.split('\'')[1])
        else:
            with open('./config.py','w+',encoding='utf-8') as f:
                f.write('IPHONE_NUMBER=\'\'' + '\n')
                f.write('URL=\'http://121.40.138.226:8000/snippets/\'')
                print("\033[1;34;40m配置文件生成完成,为./config.py.\033[0m")
                print("\033[1;34;40m手机号配置方式: IPHONE_NUMBER=\'此处输入你的手机号\'\033[0m")
                print("\033[1;34;40m后续内容为访问路径,没要求不用修改\033[0m")
                print("\033[1;34;40m修改方式：终端(目前你所在行)输入:sudo vim ./config.py 回车即可\033[0m")
                print("\033[1;31;40m修改内容均不要加额外内容空格换行等\033[0m")
                sys.exit(0)
        open('config_command.log',mode='a') 
        #with open('./config_command.log','r',encoding='utf-8') as f:
        #    f.close()


class MyListenThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.client_aliyun = client()

    def write_config_command(self, str):
        #with open(config_command,'w+',encoding='utf-8') as fo:

        fo = open(config_command,"r+")
        if fo.seek(0,0) != fo.seek(0,2):
            fo.write ('\r\n')
        line = fo.write(str)
    
    def fun_timer(self):
        global timer
        params = {'iph':str(self.client_aliyun.iphone_num)}
        command_text = requests.get(URL, params = params).text
        if len(command_text) > 2:
            self.write_config_command(command_text)
        timer = threading.Timer(listen_time, self.fun_timer)
        timer.start()

    def run(self):
        timer = threading.Timer(2, self.fun_timer)
        timer.start()

class MyThreadEventHandler(pyinotify.ProcessEvent):
    def __init__(self):
        self.multi_event = pyinotify.IN_MODIFY    
        self.wm = pyinotify.WatchManager()                                   
        self.sol = Solution()
        self.sol_file = self.sol.get_log_file(filename)
        self.student_aliyun = student()
        self.client_aliyun = client()
        self.client_aliyun_inf = client_localInformation()
        self.client_aliyun_inf.set_localInformation()
        self.student_aliyun.ip = str(self.client_aliyun_inf.localInformation['ip'])
        self.client_aliyun.student_ip = self.student_aliyun.ip
        self.ope_fil = ope_file()
        self.student_aliyun.uuid=self.ope_fil.find_word('config.py','uuid') 
        self.infor_ver = {'iphone': self.client_aliyun.iphone_num, 'title': 'keep', 'description':'', "ip" : str(self.student_aliyun.ip), "keep_alive":self.student_aliyun.uuid, "con_operation":"command_homework"}

    def read_config_message(self):
        with open(thread_load, 'r') as fp:
            lines = fp.readlines()
            last_line = ''
            if len(lines) != 0:
                last_line = str(lines[-1])
            return last_line

    def process_IN_MODIFY(self,event):
        line = self.read_config_message()
        self.sol_file = self.sol.get_log_file(filename)
        if len(line) != 0:
            lines = json.loads(line)
        if len(line) != 0:
            for li in lines.keys():
                line = lines[li]
                line  = [str(json.dumps(val)).replace("\"",'\'') for val in line]
                directories.append(line)
                print("directories-->",directories)
                for i in directories:
                    result_directories =  self.sol.minWindow(self.sol_file, i)
                    if len(i) != 0:
                        if self.sol.minWindow(self.sol_file,i):
                            directories.pop(directories.index(i))
                            self.infor_ver['description'] = str(li)
                            req = requests.post(URL, data=self.infor_ver)

class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.eventhandler = MyThreadEventHandler()

    def run(self):
        notifier = pyinotify.Notifier(self.eventhandler.wm, self.eventhandler)                      
        self.eventhandler.wm.add_watch(thread_load,pyinotify.ALL_EVENTS)                    
        notifier.loop()

class Solution:
    def __init__(self):
        self.file_list_change = file_text()

    def get_log_file(self, inputfile):
        filesize = os.path.getsize(inputfile)
        dat_file = open(inputfile, 'r')
        last_line = ""
        lines = dat_file.readlines()
        count = len(lines)
        if count>10:
            num=10
        else:
            num=count
        i=1;
        lastre = []
        for i in range(1,(num+1)):
            lastre_temp = {}
            if lines :
                n = -i
                last_line = lines[n].strip()
                lastre_temp = self.file_list_change.change_text(lastre_temp, last_line)
                lastre_temp['command_catalog'] = '/'.join(lastre_temp['command_catalog'].split('/')[3:])
                if lastre_temp['command_catalog'] == '':
                    lastre_temp['command_catalog'] = '~'
                lastre.insert(0,str(lastre_temp))
        return lastre

    def issubsequence(self, s:str, t: str)->bool:
        for c in s:
            i = t.find(c)
            if i== -1:
                return False
            else:
                t = t[i+1:]
        return True

    def minWindow(self, S: list, T: list) -> str:
        cur = [-1] * len(S)
        for i, m_char in enumerate(S):
            if self.issubsequence(T[0],m_char):
                cur[i] = i
        for j in range(1, len(T)):
            last = -1
            new = [-1] * len(S)
            for i, m_char in enumerate(S):
                if last != -1 and self.issubsequence(T[j],m_char):
                    new[i] = last
                if cur[i] != -1:
                    last = cur[i]
            cur = new
        start, end = 0, len(S)
        for end_index, start_index in enumerate(cur):
            if start_index >= 0 and end_index - start_index < end - start:
                start, end = start_index, end_index
        return S[start: end + 1] if end < len(S) else ""
    
class file_text:
    def chang_list(self, list_text, curr_text):
        list_len = len(list_text)
        if list_len == max_line:
            list_text.pop(0)
        list_text = list_text.append(curr_text)

    def change_text(self, result_map, output):
        result=output.split(',')
        cmdTime=result[0].split(':', 1)[1][1:]
        cmdPath=result[2].split(':', 1)[1][1:]
        cmd=result[3].split(':', 1)[1][1:]
        
        cmdExit=result[4].split(':')[1]
        cmdExit=cmdExit.split('[')[1]
        cmdExit=cmdExit.split(']')[0]
        result_map["command_catalog"]=cmdPath
        result_map["command_time"]=cmdTime
        result_map["command_content"]=str(cmd)
        result_map["command_result"]=(int)(cmdExit)
        return result_map


class file_operation:
    def __init__(self):
        self.client_aliyun = client()
        self.student_aliyun = student()
        self.client_aliyun_inf = client_localInformation()
        self.client_aliyun_inf.set_localInformation()
        self.student_aliyun.ip = str(self.client_aliyun_inf.localInformation['ip'])

    def file_oper(self,output, infor_ver):
        result_map = {}
        result=output.split(',')
        cmdTime=result[0].split(':', 1)[1][1:]
        cmdPath=result[2].split(':', 1)[1][1:]
        cmd=result[3].split(':', 1)[1][1:]
        cmdExit=result[4].split(':')[1]
        cmdExit=cmdExit.split('[')[1]
        cmdExit=cmdExit.split(']')[0]
        result_map["command_catalog"]=cmdPath
        result_map["command_time"]=cmdTime
        result_map["command_content"]=str(cmd)
        result_map["command_result"]=(int)(cmdExit)
        infor_ver['description'] = str(result_map)
        req = requests.post(URL, data=infor_ver)
        if 'uuid_result' in req.text:
            print("\033[1;31;40m异地登录，异常退出！\033[0m")
            os._exit(0)
        result_map.clear()

class MyEventHandler(pyinotify.ProcessEvent):       
    def __init__(self, infor_ver):
        self.file_op = file_operation()
        self.file = open(filename, 'r')
        self.file.seek(0,2)
        self.infor_ver =  infor_ver
        self.file_line = file_text()
        self.result_map = {}
        self.result_list = []
        self.solution = Solution()
        
        self.sol = Solution()
        self.sol_file = self.sol.get_log_file(filename)
        self.student_aliyun = student()
        self.client_aliyun = client()
        self.client_aliyun_inf = client_localInformation()
        self.client_aliyun_inf.set_localInformation()
        self.student_aliyun.ip = str(self.client_aliyun_inf.localInformation['ip'])
        self.client_aliyun.student_ip = self.student_aliyun.ip
        self.ope_fil = ope_file()
        self.student_aliyun.uuid=self.ope_fil.find_word('config.py','uuid')
        self.infor_homework_ver = {'iphone': self.client_aliyun.iphone_num, 'title': 'keep', 'description':'', "ip" : str(self.student_aliyun.ip), "keep_alive":self.student_aliyun.uuid, "con_operation":"command_homework"}
        self.multi_event = pyinotify.IN_MODIFY
        self.wm = pyinotify.WatchManager()

    def read_config_message(self):
        with open(thread_load, 'r') as fp:
            lines = fp.readlines()
            last_line = ''
            if len(lines) != 0:
                last_line = str(lines[-1])
            return last_line

    def process_IN_MODIFY(self, event):
        line = self.file.readline()
        if line:
            if self.result_list:
                self.file_line.chang_list(self.result_list,self.file_line.change_text(self.result_map,line))
            else:
                self.result_list  = self.solution.get_log_file(filename)
            req = self.file_op.file_oper(line, self.infor_ver)
        line = self.read_config_message()
        self.sol_file = self.sol.get_log_file(filename)
        if len(line) != 0:
            lines = json.loads(line)
        if len(line) != 0:
            for li in lines.keys():
                for i in directories:
                    result_directories =  self.sol.minWindow(self.sol_file, i)
                    if len(i) != 0:
                        if self.sol.minWindow(self.sol_file,i):
                            directories.pop(directories.index(i))
                            self.infor_homework_ver['description'] = str(li)
                            req = requests.post(URL, data=self.infor_homework_ver)

class MyExitThread(threading.Thread):
    def __init__(self, infor_ver):
        threading.Thread.__init__(self)
        self.eventhandler = MyEventHandler(infor_ver)
    def run(self):
        notifier = pyinotify.Notifier(self.eventhandler.wm, self.eventhandler)              
        self.eventhandler.wm.add_watch(filename ,self.eventhandler.multi_event)                             
        notifier.loop()

class student:

    def __init__(self):
        self.iphone_num = IPHONE_NUMBER
        self.verification_code = ''
        self.stat_var = 0
        self.ip = ""
        self.uuid = ''

    def get_code(self):
        t = re.compile(r'^(13[0-9]|14[0|5|6|7|9]|15[0|1|2|3|5|6|7|8|9]|'
                         r'16[2|5|6|7]|17[0|1|2|3|5|6|7|8]|18[0-9]|'
                         r'19[1|3|5|6|7|8|9])\d{8}$')
        s = re.search(t,str(str(self.iphone_num)))
        if s:
            self.stat_var = 1
            print("\033[1;34;40m电话号有效，已经用" + str(self.iphone_num) + "手机号尝试登录，如想修改请修改./config.py文件\033[0m")
        else :
            self.stat_var = 0
            print("\033[1;31;40m手机号码异常，建议修改当前路径下的./config.py文件的手机号\033[0m")
        return self.stat_var
    def get_var(self):
        print("\033[1;34;40m请输入验证码:\033[0m")
        self.verification_code = input()
    
    def set_code(self):
        print("\033[1;34;40m验证码输入完成~~\033[0m")
        infor_ver = {'iphone': self.iphone_num, 'title': 'var', 'description': self.verification_code, 'ip' : str(self.ip), 'keep_alive':''}
        req = requests.post(URL, data=infor_ver)
        return req.json()["测试结果"]


class client:

    def __init__(self):
        self.iphone_num = IPHONE_NUMBER
        self.student_ip = ''
        self.iphone_stat = 0
        self.uuid = ''
    def judge(self):
        if IPHONE_NUMBER == '':
            return False;
        else :
            return True;

    def send_iphone_num(self, ip = ""):
        iphone_num_dect = {'iphone' : self.iphone_num, 'title': 'iphone', 'description':"发送手机号",'ip':str(self.student_ip), 'keep_alive': ''}
        req = requests.post(URL, data=iphone_num_dect)
        self.iphone_stat = req.json()['测试结果']
        return req.json()['测试结果']
    
    def requests_var(self, ip = ""):
        requests_var = {'iphone': self.iphone_num, 'title': "requests_var", 'description': str(ip), 'ip':'', 'keep_alive':''}
        req = requests.post(URL, data=requests_var)
        return req.json()['验证码']

class ope_file:

    def find_word(self, cur_file_name = 'config.py', find_str = 'world'):
        stat_line = ''
        with open(str(cur_file_name), 'a+') as f:
            f.seek(0)
            lines = f.readlines()
            for i in lines:
                if str(find_str) in i:
                    stat_line = str(i).split('=')[1]
                    stat_line = stat_line.split('\n')[0]
                    stat_line = stat_line.split('\'')[1]
            f.close()
        return stat_line

    def operation_file(self, Con_file_name = 'config.py',temp_file_name = 'temp_config.py', Old_str = 'world',New_str = 'Local'):
        stat_live = 0
        with open(str(Con_file_name), 'a+') as f:
            f.seek(0)
            lines = f.readlines()
            if str(Old_str) in lines:
                stat_live = 1
            else:
                f.write(New_str)
            f.close()

        if stat_live == 1:
            f_path = str(Con_file_name)
            f1 = open (f_path, "r+")
            open(str(temp_file_name), 'w').write(re.sub(str(Old_str), str(New_str), f1.read()))
            f1.close()
            if os.path.exists(str(Con_file_name)):
                os.remove(str(Con_file_name))
                os.rename(str(temp_file_name),str(Con_file_name))

class client_localInformation:
    def __init__(self):
        mobile_num = IPHONE_NUMBER
        self.localInformation = {}
        self.localInformation["mobile_num"] = mobile_num
    
    def get_localInformation(self):
        hostName = socket.gethostname()
        self.localInformation["hostname"] = hostName
        loginName = os.getlogin()
        self.localInformation["logname"] = loginName
        user_home = os.path.expanduser('~')
        self.localInformation["pwd_home"] = user_home
        machine = platform.platform()
        list = machine.split('-')
        machine = list[-3] + "-" + list[-2]
        self.localInformation["platfrom"] = machine
        self.localInformation["learnsome"] = None;
        self.localInformation["ip"] =  socket.gethostbyname(hostName)
        return self.localInformation
    
    def set_localInformation(self):
        self.localInformation = self.get_localInformation()

class client_logout:

    def __init__(self):
        self.student_aliyun = student()
        self.client_aliyun = client()
        self.client_aliyun_inf = client_localInformation()
        self.client_aliyun_inf.set_localInformation()
        self.student_aliyun.ip = str(self.client_aliyun_inf.localInformation['ip'])
        self.client_aliyun.student_ip = self.student_aliyun.ip
        self.ope_fil = ope_file()
        self.stat_code = 0;
        self.stat_var = 1;

    def client_logout_ex(self):
        self.stat_code = 0;
        self.stat_var = 1;
        if self.student_aliyun.get_code() != 1:
            sys.exit ()
        if self.client_aliyun.send_iphone_num(str(self.client_aliyun_inf.localInformation['ip'])) == 1 and self.ope_fil.find_word("config.py",'uuid') != '':
            self.stat_code = 1;
            self.student_aliyun.uuid =str(self.ope_fil.find_word("config.py", 'uuid'))
            print("\033[1;32;40m登录成功！！待到蟾宫折桂时,与你看尽长安花~~\033[0m")
        else:
            print("\033[1;34;40m向"+str(self.client_aliyun.iphone_num) + "发送验证码~~\033[0m")
            if self.client_aliyun.requests_var(str(self.client_aliyun_inf.localInformation['ip'])) != "发送完成":
                print("\033[1;32;40m验证码请求频繁,请稍后再试！\033[0m")
                self.stat_var = 0 
            else:
                self.stat_var = 1
                while 1:
                    num = 3
                    self.stat_get_code = 0
                    while  num > 0 and self.stat_get_code == 0 :
                        print("\033[1;34;40m请填写验证信息,只有"+str(num)+"次机会\033[0m")
                        self.student_aliyun.get_var()
                        self.stat_get_code = self.student_aliyun.set_code()
                        num -= 1
                    if num == 0 and self.stat_get_code == 0: 
                        print("\033[1;31;40m/登录失败！！\033[0m")
                        sys.exit()
                        break;
                    else:
                        self.stat_code = 1
                        self.student_aliyun.uuid = self.stat_get_code
                        temp_uuid = self.ope_fil.find_word("config.py", "uuid")
                        self.ope_fil.operation_file("config.py","temp_config.py",'uuid='+'\''+str(temp_uuid)+'\'', 'uuid='+'\''+str(self.student_aliyun.uuid)+'\'')
                        print("\033[1;32;40m登录成功！！待到蟾宫折桂时,与你看尽长安花~~\033[0m")
                        break;
        if self.stat_code == 1 and self.stat_var == 1:
            infor_cof_desc = self.client_aliyun_inf.get_localInformation()
            infor_cof = {'iphone':str(self.client_aliyun.iphone_num),'title':'keep','description':str(infor_cof_desc),"ip":str(self.student_aliyun.ip),"keep_alive": self.student_aliyun.uuid,"con_operation": "config"}
            req = requests.post(URL, data=infor_cof)
        infor_ver = {'iphone': self.client_aliyun.iphone_num, 'title': 'keep', 'description':'', "ip" : str(self.student_aliyun.ip), "keep_alive":self.student_aliyun.uuid, "con_operation":"operation"}

        st_result = os.stat(filename)
        st_size = st_result[6]
        exit_thread = MyExitThread(infor_ver)
        exit_thread.start()

if __name__ == '__main__':
    config_ch = config_change()
    config_ch.file_check_exist()
    client_log = client_logout()
    client_log.client_logout_ex()
    my_listen = MyListenThread()
    min_thread = MyThread()
    min_thread.start()
    my_listen.start()
