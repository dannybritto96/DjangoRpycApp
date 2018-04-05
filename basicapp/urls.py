from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^operations/$',views.operations_menu,name='operations'),
    url(r'^ping/$',views.ping_view,name='ping'),
    url(r'^update/$',views.update_view,name='update'),
    url(r'^filelist/$',views.file_select,name='file_select'),
    url(r'^param_form/$',views.param_form,name='param_form'),
    url(r'^add_file/$',views.add_file,name='add_file'),
    url(r'^add_file/form/$',views.add_file_form,name='add_file_form')
]
