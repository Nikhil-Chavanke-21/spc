from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from matplotlib.pyplot import get
from rest_framework.generics import (
	ListAPIView, 
	RetrieveAPIView,
	UpdateAPIView,
	DestroyAPIView,
	CreateAPIView
)
from rest_framework.permissions import(
	IsAuthenticated,
	IsAdminUser,
	AllowAny
	)
from .permissions import IsOwner
from files.models import File
from .serializers import FileSerializer, LoginSerializer

class FileUpload(CreateAPIView):
	serializer_class=FileSerializer
	def perform_create(self, serializer):
		serializer.is_valid()
		serializer.save(owner=self.request.user)
		return Response(serializer.data, status=HTTP_201_CREATED)

class FileView(ListAPIView):
	serializer_class=FileSerializer	
	permission_classes=[IsOwner, IsAuthenticated]
	def get_queryset(self):
		user=self.request.user
		return user.file_set.all()

class FileRetrieve(RetrieveAPIView):
	serializer_class=FileSerializer
	lookup_field='filename'
	def get_queryset(self):
		user=self.request.user
		return user.file_set.all()

class FileUpdate(UpdateAPIView):
	queryset=File.objects.all()
	serializer_class=FileSerializer
	lookup_field='filename'

class FileDelete(DestroyAPIView):
	queryset=File.objects.all()
	serializer_class=FileSerializer
	lookup_field='filename'

from rest_framework.response import Response
from rest_framework.views import APIView

class LoginAPIView(APIView):
	permission_classes=[AllowAny]
	serializer_class=LoginSerializer
	def post(self, request, *args, **kwargs):
		data=request.data
		serializer=LoginSerializer(data=data)
		if serializer.is_valid(raise_exception=True):
			new_data=serializer.data
			return Response(new_data, status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
