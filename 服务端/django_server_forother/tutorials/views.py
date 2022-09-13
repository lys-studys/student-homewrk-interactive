from tutorials.models import Tutorial,StudentAliyunConfig,StudentAliyunOperation,CommandGather,StudentCommandGather
from tutorials.serializers import TutorialSerializer,StudentAliyunConfiger,StudentAliyunOperationer,CommandGatherr,StudentCommandGatherr
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from tutorials.utils import redis_conn
from django.db import models
from redis import*
from tutorials.sms_utils import send_sms
import uuid
from json import*
import json 
import time
import re
from itertools import chain
from tutorials.config import VER_TIME, IPH_TIME, UUID_TIME
class homework_message:
    def __init__(self):
        self.message = {}
        self.student_message = {}

    def send_one_message(self,student_iph):
        StudentCommandGather.objects.filter(student_iphone = student_iph, student_command_ok = 1, student_command_data = 0).update(student_command_ok = 0)

    def get_now_time(self):
        return str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def get_student_command_message(self, student_iph):
        cmd = CommandGather.objects.all().values('command_id')
        cmd1 = []
        for i in range(len(cmd)):
            cmd1.append(cmd[i]['command_id'])
        scmd1 = []
        scmd = StudentCommandGather.objects.filter(student_iphone = str(student_iph)).values('student_command')
        for i in range(len(scmd)):
            scmd1.append(scmd[i]['student_command'])
        result_cmd = []
        for i in range(len(cmd1)):
            if scmd1.count(cmd1[i]) == 0:
                result_cmd.append(cmd1[i])
        result = []
        for i in range(len(result_cmd)):
            result_temp = CommandGather.objects.filter(command_id = result_cmd[i]).values('command_data')
            result.append(result_temp)
        return result,result_cmd


    def get_student_message(self, student_iph):
        no_send_data = StudentCommandGather.objects.filter(student_iphone = student_iph,student_command_ok = 0).values('student_command')
        li = StudentAliyunConfig.objects.all()
        command_gather = {}
        student_command_temp,student_cmd= self.get_student_command_message(student_iph)
        for j in student_cmd:
            if len(StudentCommandGather.objects.filter(student_command=str(j),student_iphone=str(student_iph))) == 0:
                studentcommandgather = StudentCommandGather(student_command=str(j),student_iphone=str(student_iph),student_request_time = self.get_now_time())
                studentcommandgather.save()
            else :
                print("重复内容不予存储")

        for i in no_send_data:
            StudentCommandGather.objects.filter(student_command = i['student_command']).update(student_command_ok = 1,student_response_time = self.get_now_time())
            temp = i['student_command']
            no_send_command = CommandGather.objects.filter(command_id = temp).values('command_data')
            for j in no_send_command:
                number = json.loads(j['command_data'])
                command_gather[str(temp)] = number
        return command_gather

class question_factory(APIView):
    def __init__(self):
        global map
    def build_question(self, index, ver):
        #print("map 内容", self.map)
        #print("map ver", type(ver))
        if index not in self.map:
            serializer = TutorialSerializer(data=ver)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        obj = re.compile(r"<QueryDict: (?P<ver>.*)>", re.S)
        ver = obj.search(ver)['ver']
        return self.map[index].get_answer(eval(ver))

    def segiser(self, index, quesiton):
        self.map[index] = quesiton

question_factory.map = {}
class choice_question(APIView):
    def __init__(self, ver):
        self.push_var = ''
        self.use_time = 0
        self.ip = ''
        self.ver = ver
        self.question_fact = question_factory()

class choice_question_keep_alive(choice_question,APIView):
    def __init__(self, ver):
        super().__init__(ver)
        self.send_one_mess = homework_message()

    def get_answer(self, ver):
        if(str(ver['keep_alive'][0])!=''):
            if redis_conn.get(str(ver['iphone'][0]) + '-uuid') == str(ver['keep_alive'][0]):
                if ver['con_operation'][0] == 'config':
                    serializer = StudentAliyunConfiger(data = eval(str(ver['description'][0])))
                    if serializer.is_valid():
                        if StudentAliyunConfig.objects.filter(mobile_num=ver['iphone'][0]).exists():
                            self.send_one_mess.send_one_message(ver['iphone'][0])
                            return Response({"stat_save":"exist"})
                        else:
                            serializer.save()
                            self.send_one_mess.send_one_message(ver['iphone'][0])
                            return Response({"stat_save":"config_save"})
                    else:
                        return Response({"stat_save":"error"})
                elif ver['con_operation'][0] == 'operation':
                    mobile_num1 = str(ver['iphone'][0])
                    bool_id_all = StudentAliyunConfig.objects.get(mobile_num = mobile_num1).student_id
                    vers = eval(ver["description"][0])
                    vers["student_id"]= bool_id_all
                    serializer = StudentAliyunOperationer(data = vers)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({"stat_save":"operation_save"})
                    else:
                        return Response({"stat_save":"error"})
                    return Response({"uuid_result":"Yes"})
                elif ver["con_operation"][0] == 'command_homework':
                    StudentCommandGather.objects.filter(student_command = ver['description'][0],student_iphone = str(ver['iphone'][0])).update(student_command_data = 1,student_response_time = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
                    return Response({"student_command_ok":1})
            else :
                return Response({"uuid_result":"No"})
        else :
            return Response({"alive error":1})

    def after_factory(self, question_name):
        self.question_fact.segiser(str(question_name), self)

class choice_question_var(choice_question,APIView):
    def __init__(self, ver):
        super().__init__(ver)
    def get_answer(self, ver):
        if ver['description'][0] == redis_conn.get('ver'+str(ver["iphone"][0])):
            redis_conn.set(str(ver['iphone'][0])+str(ver['ip'][0]), str(ver['iphone'][0]))#, ex = 120)
            uuidOne = uuid.uuid1()
            redis_conn.set(str(ver['iphone'][0])+'-uuid', str(uuidOne))#, ex=1200)
            redis_conn.set(str('ip'+str(ver['iphone'][0])),str(ver['ip'][0]))
            return Response({"测试结果": str(uuidOne)})
        else:
            return Response({"测试结果":0})
    
    def after_factory(self, question_name):
        self.question_fact.segiser(str(question_name), self)

class choice_question_request_var(choice_question,APIView):
    def __init__(self, ver):
        super().__init__(ver)
    
    def get_answer(self, ver):
        mobile_number = ver['iphone'][0]
        result, errmsg = send_sms(mobile_number)
        #result = True
        #errmsg = {"verification_code":'123456'}
        self.push_var = result
        self.use_time = errmsg
        if result == False :
            return Response({"验证码": str(errmsg)})
        else:
            redis_conn.set('ver'+str(ver['iphone'][0]),str(errmsg['verification_code']), ex = VER_TIME)
            return Response({"验证码": "发送完成"})
    
    def after_factory(self, question_name):
        self.question_fact.segiser(str(question_name), self)


class choice_question_iphone(choice_question,APIView):
    def __init__(self, ver):
        super().__init__(ver)
    def get_answer(self, ver):
        keys = redis_conn.keys()
        if ver['iphone'][0] == redis_conn.get(str(ver['iphone'][0]) + str(ver['ip'][0]))and ver['ip'][0] == redis_conn.get('ip'+ver['iphone'][0]):
            return Response({"测试结果": 1})
        else:
            return Response({"测试结果": 0})
    
    def after_factory(self, question_name):
        self.question_fact.segiser(str(question_name), self)


class choice_question_bash_os_information(choice_question,APIView):
    def __init__(self, ver):
        super().__init__(ver)
    def get_answer(self, ver):
        return Response({"测试结果":"description"})
    
    def after_factory(self, question_name):
        self.question_fact.segiser(str(question_name), self)

class choice_question_default(choice_question, APIView):
    def __init__(self, ver):    
        super().__init__(ver)
    def get_answer(self, ver):
        serializer = TutorialSerializer(data=ver['description'][0])
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def after_factory(self, question_name):
        self.question_fact.segiser(str(question_name), self)

class choice_question_use(APIView):
    def __init__(self):
        global quesiton_keep
        global quesiton_var
        global quesiton_request
        global quesiton_iphone
        global quesiton_bash

    def make_factory(self):
        quesiton_keep.after_factory("keep")
        quesiton_var.after_factory("var")
        quesiton_request.after_factory("requests_var")
        quesiton_iphone.after_factory("iphone")
        quesiton_bash.after_factory("bash_os_information")

quesiton_keep = choice_question_keep_alive(None)
quesiton_var = choice_question_var(None)
quesiton_request = choice_question_request_var(None)
quesiton_iphone = choice_question_iphone(None)
quesiton_bash = choice_question_bash_os_information(None)


class SnippetList(APIView):
    def __init__(self):
        self.push_var = ''
        self.use_time = 0
        self.ip =''
        self.student_iph=''
        self.question_use = choice_question_use()
        self.question_use.make_factory()
        self.question_fact = question_factory()
        self.homework = homework_message()
    def put(self):
        pass

    def get(self, request, format=None):
        self.student_iph = request.GET['iph']
        snippets = Tutorial.objects.all()
        serializer = TutorialSerializer(snippets, many=True)
        get_homework = self.homework.get_student_message(self.student_iph)
        return Response(get_homework)

    def post(self, request, format=None):
        ver = request.data
        return self.question_fact.build_question(ver['title'],str(ver))

class SnippetDetail(APIView):
    def get_object(self, pk):
        try:
            return Tutorial.objects.get(pk=pk)
        except Tutorial.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = TutorialSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = TutorialSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
