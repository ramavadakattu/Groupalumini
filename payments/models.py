from django.db import models
from institution.models import Institution
from django.contrib.auth.models import User

import datetime

# Create your models here.

class Fund(models.Model):
      fundname = models.CharField(max_length=100)
      totalamount = models.FloatField()
      totaldonations = models.FloatField(default=0)
      description = models.TextField()
      deadline = models.DateField()
      currency = models.CharField(max_length=15,null=True,blank=True)
      institute = models.ForeignKey(Institution)
      user = models.ForeignKey(User)
      createddate = models.DateTimeField(auto_now_add=True)
      updateddate = models.DateTimeField(auto_now=True)
      #is this fund opened for payment
      #if the total donations is greater than that of total amount  of the fund
      #then that particular Fund is closed
      open = models.BooleanField(default=False)
      
      def __unicode__(self):
        return "%s "%(self.fundname)
        
        
      def getTotalPeople(self):
          ''' get total people who has donated to  this fund '''
          emaillist =  self.donation_set.values_list('user__email',flat=True)
          return len(set(emaillist))
          
          
      def getFundStatus(self):
          ''' is it closed or open ''' 
          type='open'
          today = datetime.datetime.today().date()   
          if self.deadline < today :
               type = 'close'
               
          if self.totaldonations >= self.totalamount :
                type = 'close'
            
          return type      
                
                


class Donation(models.Model):
    fund = models.ForeignKey(Fund)
    user = models.ForeignKey(User)
    institute = models.ForeignKey(Institution)
    donationamount = models.FloatField()
    createddate = models.DateTimeField(auto_now_add=True)
    updateddate = models.DateTimeField(auto_now=True)
    paypaltransactionid = models.CharField(max_length=125)
    correlationid = models.CharField(max_length=125)
    
    
    def __unicode__(self):
        return " Donation amount = %s , Paypal Transaction Id %s Fund Name = %s  Institute =%s "%(self.donationamount,self.paypaltransactionid,self.fund.fundname,self.institute.name)
        
        
    
    
    
    
    
    
    
      
