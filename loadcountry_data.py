from django.core.management import setup_environ
import settings
setup_environ(settings) 



from location.models import Country,State
import os


def loadCountryData():
    f = open(os.path.join(os.path.join(settings.SITE_ROOT,"data"),"countrynames.csv"))
    lineno = 0
    while 1:
        line = f.readline()
        lineno = lineno + 1
        
        if lineno == 1 :
            #skip the header
            continue
        
        if line :
            print line
            array=line.split(",")
            c = Country()
            c.name = array[2].replace("\"","").strip()
            c.id = array[0]
            c.save()
        else :
            break
            
    print "Total lines read %d" %((lineno-1),) 
             

def loadStateData():
    f = open(os.path.join(os.path.join(settings.SITE_ROOT,"data"),"country_state.csv"))
    lineno = 0
    while 1:
        line = f.readline()
        lineno = lineno + 1
        
        if lineno == 1 :
            #skip the header
            continue
        
        if line :
            print line
            array=line.split(",")
            s = State()
            s.name = array[2].replace("\"","").strip()
            s.id = array[0]
            s.country = Country.objects.get(pk = array[1])
            s.save()            
        else :
            break
            
    print "Total lines read %d" %((lineno-1),) 



if __name__ == '__main__':
    loadCountryData()
    loadStateData()