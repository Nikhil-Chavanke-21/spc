from rest_framework.serializers import ModelSerializer, CharField
from files.models import File

from django.db import models
#
from django.contrib.auth.models import User
#
from django.db.models import Q
#
class FileSerializer(ModelSerializer):
	class Meta:
		model=File
		fields=['filename','filetype','md5sum','file']
	def create(self, validated_data):
		print(validated_data)
		filename=validated_data['filename']
		filetype=validated_data['filetype']
		md5sum=validated_data['md5sum']
		file=validated_data['file']
		file_obj=File(
			filename=filename,
			filetype=filetype,
			md5sum=md5sum,
			file=file,
			)
		file_obj.save()
		return validated_data

class LoginSerializer(ModelSerializer):
	token=CharField(allow_blank=True, read_only=True)
	username=CharField(required=False,allow_blank=True)
	class Meta:
		model=User
		fields=[
			'username',
			'password',
			'token',
		]
		extra_kwargs={'password':{'write_only':True}}
	def validate(self, data):
		user_obj=None
		username=data.get("username",None)
		password=data["password"]
		if not username:
			raise ValidationError("A username is required to login.")
		user=User.objects.filter(
			Q(username=username)
			)
		if user.exists() and user.count()==1:
			user_obj=user.first()
		else:
			raise ValidationError("This username does not exist.")
		if user_obj:
			if not user_obj.check_password(password):
				raise ValidationError("Incorrect credentials. Please try again.")
		data["token"]="SOME RANDOM TOKEN"
		return data	