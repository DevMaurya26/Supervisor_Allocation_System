from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Allocation_File(models.Model):
    Created_at = models.DateTimeField(auto_now_add=True,)
    file_name = models.CharField(max_length=100)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    exam_name = models.CharField(max_length=250)

    
    def __str__(self):
        return str(self.file_name)
    
class Change_reqs(models.Model):
    requestor_id  = models.ForeignKey(User,on_delete=models.CASCADE)
    reqtor_name = models.CharField(max_length=100)
    file_name = models.CharField(max_length=400)
    previous_details = models.CharField(max_length=300)
    college = models.CharField(max_length=250)
    req_date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)



