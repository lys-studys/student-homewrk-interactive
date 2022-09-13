from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from tutorials import views

urlpatterns = [
    url(r'^snippets/$', views.SnippetList.as_view()),
    url(r'^question_factory/$', views.question_factory.as_view()),
    #url(r'^snippets/$', views.choice_question.as_view()),
    #url(r'^snippets/$', views.choice_question_keep_alive.as_view()),
    #url(r'^snippets/$', views.choice_question_var.as_view()),
    #url(r'^snippets/$', views.choice_question_request_var.as_view()),
    #url(r'^snippets/$', views.choice_question_iphone.as_view()),
    ##url(r'^snippets/$', views.choice_question_bash_os_information.as_view()),
    #url(r'^snippets/$', views.choice_question_default.as_view()),
    url(r'^snippets/(?P<pk>[0-9]+)/$', views.SnippetDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
