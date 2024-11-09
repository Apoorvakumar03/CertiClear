
'''
class User(models.Model):
    uid = models.IntegerField()
    uname = models.CharField(max_length=100)
    uemail = models.EmailField()
    role = models.CharField(max_length=50)

    def __str__(self):
        return self.uname

'''
from django.db import models

class User(models.Model):
    uid = models.IntegerField(primary_key=True)
    uname = models.CharField(max_length=100)
    uemail = models.EmailField()
    upassword = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
    role=models.CharField(max_length=50,default=None)
    department=models.CharField(max_length=50,default=None)
    def __str__(self):
        return self.uname
class requestData(models.Model):
    uid=models.CharField(max_length=10, primary_key=True)
    # Library Department Examination Department Lab Department Hostel Department Faculty Department  Security Department
    libD= models.CharField(max_length=100)
    labD=models.CharField(max_length=100)
    examD=models.CharField(max_length=100)
    hostelD=models.CharField(max_length=100)
    hoD=models.CharField(max_length=100)
    secD=models.CharField(max_length=100)
    #secD hoD hostelD libD examD labD
    def __str__(self):
        return self.uid
