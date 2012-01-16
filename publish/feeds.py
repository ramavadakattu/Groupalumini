from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Rss201rev2Feed
from publish.models import Entry
from institution.models import Institution,UserProfile



class LatestInstituteBlogPosts(Feed):
    title_template = 'publish/feeds/title.html'
    description_template = 'publish/feeds/description.html'
    
    
    def get_object(self, bits):        
        if len(bits) == 0:
            raise ObjectDoesNotExist
        self.institute = None
        #for the faculty feed        
        self.user = None
        
        if len(bits) >= 1:
            subdomain = bits[0]
            institute = Institution.objects.get(subdomain=subdomain)
        
        if len(bits) >= 2 :
            facultyname = bits[1]
            faculty_name = facultyname.replace("-"," ")
            profile = UserProfile.objects.get(fullname__iexact=faculty_name)
            self.user = profile.user
       
        return institute
    
    #Feed title
    def title(self, obj):
        if self.user is None :
                   return "%s Main Blog Feed " % obj.name
        else :
            return "Faculty Feed %s  Institute %s " % (self.user.get_profile().fullname,obj.name)

    def link(self, obj):        
        return obj.get_absolute_url()

    def description(self, obj):
        if self.user is None :
                   return "%s Main Blog Feed " % obj.name
        else :
            return "Faculty Research Feed %s  Institute %s " % (self.user.get_profile().fullname,obj.name)



    def items(self,obj):
        if self.user is None :
             return Entry.objects.filter(institute__id=obj.id,research_paper=False).order_by('-createddate')[:15]
        else:
             return Entry.objects.filter(institute__id=obj.id,user__id=self.user.id,research_paper=True).order_by('-createddate')[:15]

    def item_link(self, item):
        return "%s"%( item.get_absolute_url(),)

    def item_pubdate(self, item):
        return item.createddate
    
    def item_author_name(self, item):
        return item.user.get_profile().fullname

    
    