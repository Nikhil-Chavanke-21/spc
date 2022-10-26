# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.utils import timezone
from django.contrib.auth.models import User
#
class File(models.Model):
	file=models.BinaryField(max_length=4096*4096*4096, editable=True)
	filename=models.CharField(max_length=100)#primary_key=true
	filetype=models.CharField(max_length=50,null=True)
	md5sum=models.CharField(max_length=32,null=True)
	date_upload=models.DateTimeField(default=timezone.now)
	owner=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
	def __str__(self):
		return self.filename