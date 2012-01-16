# Create your views here.
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponse , HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.http import Http404
from session_messages import create_message
from django.contrib.auth import authenticate ,login ,logout
import settings
import os
from django.template.loader import render_to_string
from django.contrib.auth.models import UserManager
from django.contrib.auth.views import redirect_to_login
from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.utils import simplejson
from django.views.generic.list_detail import object_list
from django.db.models import F , Q


import datetime
import logging
import logging.config
import paypal


from payments.models import Fund,Donation
from payments.forms import FundForm
from profile.views import getPage
from institution.models import deliverEmail,UserProfile


mlogger = logging.getLogger(__name__)


@login_required(redirect_field_name='next')
def samplePaymentTesting(request):
    return render_to_response('payments/test.html',{},RequestContext(request))
    
@login_required(redirect_field_name='next')    
def acceptPayment(request,fundid):
    fundid = int(fundid)
    fund = Fund.objects.get(pk=fundid)
    amount = int(request.POST['amount'])    
    pp = paypal.PayPal()
    successurl = "http://%s%s/%s%s" %(request.institute.subdomain.strip(),settings.DOMAIN,"payments/review/",str(fund.id))
    failurl = "http://%s%s/%s%s" %(request.institute.subdomain.strip(),settings.DOMAIN,"payments/cancel/",str(fund.id))
    mlogger.debug(successurl)
    mlogger.debug(failurl)
    token = pp.SetExpressCheckout(amount,successurl,failurl)
    paypal_url = pp.PAYPAL_URL + token
    payload = {'paypal_url':paypal_url}
    return HttpResponseRedirect(paypal_url)
    
    
@login_required(redirect_field_name="next")
def enterAmount(request,fundid):
    mlogger.debug("hello enter the amount that you want to donate to this fund .......")
    fundid = int(fundid)
    fund = Fund.objects.get(pk=fundid)    
    return render_to_response('payments/enteramount.html',{'fund':fund},RequestContext(request))
    
    
@login_required(redirect_field_name='next')        
def paymentReview(request,fundid):
    pp = paypal.PayPal()
    fund = Fund.objects.get(pk=int(fundid))      
    if request.method == 'GET':
        token = request.GET.get('token')
        payerid = request.GET['PayerID']        
        paypal_details = pp.GetExpressCheckoutDetails(token,return_all = True)
        payload = {}
        payload['fund'] = fund
        if 'Success' in paypal_details['ACK']:            
            payload['ack'] = True
            payload['amount'] = paypal_details['AMT'][0]
            payload['currency'] = paypal_details['CURRENCYCODE'][0]
            payload['token'] = token
            payload['payerid'] = payerid            
            return render_to_response('payments/review.html', payload, RequestContext(request))
        else :
            create_message(request,"Some problem with the payment.Please try again............")
            return HttpResponseRedirect(reverse('displayfundsurl'))            
    if request.method == 'POST':        
        token = request.POST['token']
        payerid = request.POST['payerid']
        amount = request.POST['amount']        
        payment_details  = pp.DoExpressCheckoutPayment(token,payerid,amount)
       
        if 'Success' in payment_details['ACK']:        
            str = "Successfully donated the amount  %s to %s"%(amount,fund.fundname,)
            create_message(request,str)
            #note down this donation
            d = Donation()
            d.user = request.user
            d.fund = fund
            d.institute = request.institute
            d.donationamount = amount
            d.paypaltransactionid = payment_details['TRANSACTIONID']
            d.correlationid = payment_details['CORRELATIONID']
            d.save()
            fund.totaldonations = fund.totaldonations+float(amount)
            fund.save()
            
            # send mail to admin  of institute and the user about the donation ........................
            # and the admin of the site about the details of the donation            
            deliverEmail('amount_donated_subject.html','amount_donated.html',{'institute':request.institute,'fund':fund,'user':request.user,'amount':amount,'transactionid':payment_details['TRANSACTIONID']},request.user.email)
            adminemail = getInstituteAdminEmail()
            siteadmin = getAlumClubAdminEmail()            
            mainlist = adminemail+siteadmin
            mlogger.debug("Main email list = %s"%(unicode(mainlist)))
            deliverEmail('reference_donation_subject.html','reference_donation.html',{'institute':request.institute,'fund':fund,'user':request.user,'amount':amount,'transactionid':payment_details['TRANSACTIONID']},mainlist)
            return HttpResponseRedirect(reverse('displayfundsurl'))        
        else :
            create_message(request,"Some problem with the payment.Please try again............")
            return HttpResponseRedirect(reverse('displayfundsurl'))        

    
@login_required(redirect_field_name='next')     
def displayFunds(request):    
    mlogger.debug("displaying all the funds  .............")
    today = datetime.datetime.today().date()
    funds = Fund.objects.filter(institute__id=request.institute.id,deadline__gte=today,totaldonations__lt=F('totalamount')).order_by('-createddate')    
    
    page = getPage(request)    
    return object_list(request, queryset=funds,extra_context={'type':'open'},
                       template_object_name="fund", paginate_by=settings.FUNDS_PER_PAGE,
                       page=page,template_name="payments/funds.html")
    
 

@login_required(redirect_field_name='next')     
def addNewFund(request):
    mlogger.debug("adding new fund")
    if request.method == "GET":
        form = FundForm()
        return render_to_response('payments/addfund.html',{'form':form},RequestContext(request))
    elif request.method == "POST":
        form = FundForm(request.POST)
        if form.is_valid() :
            fund = form.save(commit=False)
            fund.institute = request.institute
            fund.user = request.user
            fund.save()
            create_message(request,"Created new fund successfully...............")
            return HttpResponseRedirect(reverse('displayfundsurl'))
        else :
            return render_to_response('payments/addfund.html',{'form':form},RequestContext(request))
            
            
@login_required(redirect_field_name='next')             
def viewFund(request,fundid):
    mlogger.debug("View a fund",fundid)
    fund = Fund.objects.get(pk=fundid)    
    return render_to_response('payments/viewfund.html',{'fund':fund},RequestContext(request))
    
    
@login_required(redirect_field_name='next')                 
def editFund(request,fundid):
    fundid = int(fundid)
    fund = Fund.objects.get(pk=fundid)
    if request.user.id == fund.user.id :
        if request.method == "GET" :
            mlogger.debug("the person who posted the fund is editing")
            form = FundForm(instance=fund)            
            return render_to_response('payments/addfund.html',{'form':form,'editmode':True},RequestContext(request))
        elif request.method == "POST":            
            form = FundForm(request.POST, instance=fund)
            if form.is_valid() :                
                form.save()                
                create_message(request,"Successfuly edited the fund")
                return HttpResponseRedirect(reverse('displayfundsurl'))
            else:
                return render_to_response('payments/addfund.html',{'form':form,'editmode':True},RequestContext(request))
    else :
        create_message(request,"You are not authorized to edit this fund")
        return HttpResponseRedirect(reverse('displayfundsurl'))
        
        
    

@login_required(redirect_field_name='next')                     
def deleteFund(request,fundid):
    Fund.objects.get(pk=int(fundid)).delete()
    create_message(request,"Deleted the fund")
    return HttpResponseRedirect(reverse('displayfundsurl'))
    
    
@login_required(redirect_field_name='next')                         
def cancelPayment(request,fundid):    
    create_message(request,"Oops some problem with the payment please try again")
    return HttpResponseRedirect(reverse('displayfundsurl'))
    
    
    
    
def getInstituteAdminEmail():
    emaillist = UserProfile.objects.filter(isadmin=True).values_list('user__email',flat=True)
    return list(emaillist)


def getAlumClubAdminEmail():
    emaillist = []
    for admin in settings.ADMINS :
        emaillist.append(admin[1])
    return emaillist


def displayClosedFunds(request):
    mlogger.debug("display closed funds")
    #funds which crossed their expiry date
    #funds which raised enough amount
    today = datetime.datetime.today().date()   
    funds = Fund.objects.filter(institute__id=request.institute.id).filter( Q(deadline__lt=today) | Q(totaldonations__gte=F('totalamount')) ).order_by('-createddate')
    page = getPage(request)    
    return object_list(request, queryset=funds,extra_context={'type':'close'},
                       template_object_name="fund", paginate_by=settings.FUNDS_PER_PAGE,
                       page=page,template_name="payments/funds.html")

 