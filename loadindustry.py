from django.core.management import setup_environ
import settings
setup_environ(settings)
import xlrd

from statistics.models import Industry
from statistics.models import Market



def loadIndustryData():
    ''' loads the industry data into two tables
        Industry and Market ''' 
    wb = xlrd.open_workbook(settings.SITE_ROOT+"/data/"+"industry-markets.xls")
    #First sheet contains the Industry and markets information
    sh = wb.sheet_by_name(u'Sheet1')
    
    last_industry = None
    for rownum in range(sh.nrows):        
        row = sh.row_values(rownum)
        industry = row[0].strip()
        
        if industry.lower() == "industry" :
            continue
        
        if len(industry) > 0 :             
            ids = Industry()
            ids.name = industry
            ids.save()
            last_industry = ids
        
        market = row[1].strip()
        
        if len(market) > 0 :
            #no market row invalid
            try :
                m = Market.objects.get(name__iexact=market)
                if last_industry is not None :
                        m.industries.add(last_industry)                         
            except Market.DoesNotExist :
                m = Market()
                m.name = market
                m.save()
                m.industries.add(ids)            
        else:
            continue
        


if __name__ == '__main__':
    loadIndustryData()
    