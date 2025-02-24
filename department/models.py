from django.db import models
from account.models import Customer, CustomUser, UserBaseModel
from utils.abs_model import TimeStampedModel

class Department(models.Model):
    name = models.CharField(max_length=255, verbose_name='部署名/所属名等')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

class Person(UserBaseModel, TimeStampedModel):
    '''
    顧客が大企業、大きな団体の場合、複数人で使用することになるので、子として企業、団体が登録ができるようにする
    '''
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='person_profiles')
    parent = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
