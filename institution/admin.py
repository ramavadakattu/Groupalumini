import models
from django.contrib import admin


from institution.models import UserProfile , FacultyInstitute , StudentInstitute , Student , Faculty , Institution


admin.site.register(models.FacultyInstitute)
admin.site.register(models.StudentInstitute)

admin.site.register(models.Student)
admin.site.register(models.Faculty)
admin.site.register(models.Institution)






class StudentInline(admin.StackedInline):
    model = models.Student
    extra = 0



class FacultyInline(admin.StackedInline):
    model = models.Faculty
    extra = 0
    
    
class UserProfileAdmin(admin.ModelAdmin):
      inlines = [StudentInline,FacultyInline]



admin.site.register(models.UserProfile, UserProfileAdmin) 

     

