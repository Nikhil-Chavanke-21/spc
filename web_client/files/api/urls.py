from django.conf.urls import url
from .views import (
	FileView, 
	FileRetrieve,
	FileUpdate,
	FileDelete,
	FileUpload,
	LoginAPIView
)
#
from django.conf.urls import include
from rest_framework_jwt.views import obtain_jwt_token
#

urlpatterns = [
	#
    url('api-auth/', include('rest_framework.urls')),
    url(r'^api-token-auth/', obtain_jwt_token),
    #
    url(r'^login/$',LoginAPIView.as_view(), name='login-api'),
	url(r'^upload/$', FileUpload.as_view(), name="file_upload"),
	url(r'^(?P<filename>[\w-]+)/edit/$', FileUpdate.as_view(), name="file_update"),
	url(r'^(?P<filename>[\w-]+)/delete/$', FileDelete.as_view(), name="file_delete"),
    #url(r'^(?P<filename>[\w-]+)/$', FileRetrieve.as_view(), name="file_retrieve"),
    url(r'^$', FileView.as_view(), name="file_view"),  
]