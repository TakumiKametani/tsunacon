from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from encrypted_model_fields.fields import EncryptedCharField
from utils.abs_model import TimeStampedModel
from utils.validators import validate_katakana

CUSTOMER_TYPES = [
    ('company', '企業'),
    ('organization', '組織'),
    ('individual', '個人'),
    ('sole_proprietor', '個人事業主'),
    ('group', '団体'),
]

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    #
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)


class Contract(TimeStampedModel):
    ym = datetime.now()
    contract_file = models.FileField(upload_to=f'contracts/{ym.year}/{ym.month}/')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}: {self.ym.year}/{self.ym.month}"

class UserBaseModel(models.Model):
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name_kana = models.CharField(max_length=255, validators=[validate_katakana])
    first_name_kana = models.CharField(max_length=255, validators=[validate_katakana])
    phone = models.CharField(max_length=20)
    registration_date = models.DateTimeField(auto_now_add=True)
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, blank=True)
    postal_code = models.CharField(max_length=10, help_text="郵便番号ハイフンなし")
    address_1 = models.CharField(max_length=255, help_text="番地まで")
    address_2 = models.CharField(max_length=255, help_text="ビルやアパートの名称◎号室", null=True, blank=True)
    notification_email = models.EmailField(null=True, blank=True)

    class Meta:
        abstract = True


class Customer(UserBaseModel, TimeStampedModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='customer_profiles')
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name='組織・企業・団体名')
    customer_type = models.CharField(max_length=50, choices=CUSTOMER_TYPES)
    billing_email = models.EmailField(null=True, blank=True)
    payment_due_day = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.customer_type} - {self.name}"


class UserType(TimeStampedModel):
    type_id = models.PositiveSmallIntegerField(unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Member(UserBaseModel, TimeStampedModel):
    user_types = models.ManyToManyField(UserType, related_name='members')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='member_profiles')
    referral_id = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user_types} - {self.last_name} {self.first_name}({self.last_name_kana} {self.first_name_kana}) - {self.referral_id}"


class BankAccount(TimeStampedModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    bank_name = EncryptedCharField(max_length=255)
    branch_name = EncryptedCharField(max_length=255)
    account_number = EncryptedCharField(max_length=20)
    account_holder = EncryptedCharField(max_length=255)

    def __str__(self):
        return f"{self.bank_name} - {self.account_number}"

