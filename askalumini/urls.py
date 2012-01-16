from django.conf.urls.defaults import *
from voting.views import vote_on_object
from askalumini.models import Question,Answer

question_args = {
        'model':Question ,
        'allow_xmlhttprequest': True,
    }

answer_args = {
        'model':Answer ,
        'allow_xmlhttprequest': True,
    }


urlpatterns = patterns('askalumini.views',
        url(r'^$','askHome',name='askaluminiurl'),                               
        url(r'^questions/(?P<questionno>\d+)/$','displayQuestion',name='displayquestionurl'),
        url(r'^askquestions/$','askQuestion',name='askquestionurl'),
          url(r'^editquestions/(?P<questionno>\d+)/$','editQuestion',name='editquestionurl'),
            url(r'^deletequestions/(?P<questionno>\d+)/$','deleteQuestion',name='deletequestionurl'),
        url(r'^postcomment/$','postComment',name="postcommneturl")
       )

urlpatterns += patterns('',
        (r'^voting/question/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$', vote_on_object,question_args),
        (r'^voting/answer/(?P<object_id>\d+)/(?P<direction>up|down|clear)vote/?$', vote_on_object,answer_args),
    )

