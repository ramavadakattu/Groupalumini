from django.conf.urls.defaults import *


urlpatterns = patterns('payments.views',
        url(r'^$','displayFunds',name='displayfundsurl'),
        url(r'^closedfunds/$','displayClosedFunds',name='displayclosefundsurl'),
        url(r'^pay/(?P<fundid>[0-9]+)/$','acceptPayment',name='acceptpaymenturl'),
         url(r'^cancel/(?P<fundid>[0-9]+)/$','cancelPayment',name='cancelpaymenturl'),
        url(r'^viewfund/(?P<fundid>[0-9]+)/$','viewFund',name='viewfundurl'),
        url(r'^editfund/(?P<fundid>[0-9]+)/$','editFund',name='editfundurl'),
        url(r'^deletefund/(?P<fundid>[0-9]+)/$','deleteFund',name='deletefundurl'),        
        url(r'^enteramount/(?P<fundid>[0-9]+)/$','enterAmount',name='enteramounturl'),
        url(r'^review/(?P<fundid>[0-9]+)/$','paymentReview',name='paymentreviewurl'),
        url(r'^addnew/$','addNewFund',name='addnewfundurl'),        
       )
