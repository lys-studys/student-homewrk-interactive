from django.db import models
from datetime import datetime
# Create your models here.

class StudentAliyunConfig(models.Model):
    student_id = models.AutoField(primary_key=True)#student_id为主键,自增
    mobile_num = models.CharField(max_length=11, default='')
    pwd_home   = models.CharField(max_length=500, default='')
    hostname   = models.CharField(max_length=100, default='')
    logname    = models.CharField(max_length=50, default='')
    platfrom   = models.CharField(max_length=20, default='')
    learnsome  = models.TextField(null=True) 

class StudentAliyunOperation(models.Model):
    student_id = models.IntegerField()
    command_time  = models.DateTimeField()
    command_content = models.CharField(max_length=100, default='')
    command_catalog = models.CharField(max_length=100, default='')
    command_result = models.IntegerField(default=2)

class CommandGather(models.Model):
    command_id = models.AutoField(primary_key=True)
    command_data = models.CharField(max_length=1000, default='')
    command_updatatime = models.DateTimeField(default=datetime.now)


class StudentCommandGather(models.Model):
    student_command = models.IntegerField()
    student_command_data = models.IntegerField(default=0)
    student_iphone = models.CharField(max_length=11, default='')
    student_request_time = models.DateTimeField(default=datetime.now)
    student_response_time = models.DateTimeField(default=datetime.now)
    student_command_ok = models.IntegerField(default = 0)



class Tutorial(models.Model):
    title = models.CharField(max_length=70, blank=False, default='')
    description = models.CharField(max_length=200,blank=False, default='')
    published = models.BooleanField(default=False)
