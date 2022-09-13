#!/usr/bin/env python
# coding=utf-8
from rest_framework import serializers 
from tutorials.models import Tutorial,StudentAliyunOperation,StudentAliyunConfig,CommandGather,StudentCommandGather


class TutorialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tutorial
        fields = ('id',
                  'title',
                  'description',
                  'published')

class StudentAliyunOperationer(serializers.ModelSerializer):
    class Meta:
        model = StudentAliyunOperation
        fields=("student_id",
                "command_time",
                "command_content",
                "command_catalog",
                "command_result"
        )
        #fields = "__all__"
        depth = 1
#    def create(self, validated_data):
#        """接受客户端提交的新增数据"""
#        command_time = validated_data.get('command_time')
#        command_content = validated_data.get('command_content')
#        command_catalog = validated_data.get('command_catalog')
#        command_result = validated_data.get('command_result')
#        instance = Student.objects.create(command_time=command_time, command_content=command_content, command_catalog=command_catalog,command_result=command_result)
#        # instance = Student.objects.create(**validated_data)
#        print(instance)
#        return instance
class StudentAliyunConfiger(serializers.ModelSerializer):
    class Meta:
        model = StudentAliyunConfig
        #fields = "__all__"
        fields=("mobile_num",
                "pwd_home",
                "hostname",
                "logname",
                "platfrom",
                "learnsome")




class CommandGatherr(serializers.ModelSerializer):
    class Meta:
        model = CommandGather
        #fields = "__all__"
        fields=("command_id",
                "command_data",
                "command_updatatime")


class StudentCommandGatherr(serializers.ModelSerializer):
    class Meta:
        model = StudentCommandGather
        #fields = "__all__"
        fields=("student_command",
                "student_command_data",
                "student_iphone",
                "student_request_time",
                "student_response_time",
                "student_command_ok")

