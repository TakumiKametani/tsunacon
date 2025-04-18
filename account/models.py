import uuid
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

GENDER_TYPE = [
    ('n', '未回答'),
    ('m', '男性'),
    ('w', '女性'),
    ('o', '他')
]

ACCOUNT_TYPES = [
    ('savings', '普通'),
    ('checking', '当座'),
]


def get_upload_to_contract(instance, filename):
    now = datetime.now()
    if isinstance(instance, Customer):
        identifier = f"{instance.last_name}_{instance.first_name}_customer"
    else:
        identifier = f"{instance.last_name}_{instance.first_name}_member"
    return f'contracts/{now.year}/{now.month}/{identifier}/{filename}'


def get_upload_to_resume(instance, filename):
    return f'resumes/{instance.member.user.username}/{filename}'


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='customuser_set', blank=True)
    terms_accepted = models.BooleanField(default=False, verbose_name='利用規約を読了しました')
    privacy_policy_accepted = models.BooleanField(default=False, verbose_name='プライバシーポリシーを読了しました')


class ServiceUseAgreement(models.Model):
    name = models.CharField(max_length=255)
    contract_file = models.FileField(upload_to=get_upload_to_contract)

    def __str__(self):
        return f"{self.name}: {self.contract_file.url}"


class ConfidentialityAgreement(models.Model):
    name = models.CharField(max_length=255)
    contract_file = models.FileField(upload_to=get_upload_to_contract)

    def __str__(self):
        return f"{self.name}: {self.contract_file.url}"


class OutsourcingAgreement(models.Model):
    name = models.CharField(max_length=255)
    contract_file = models.FileField(upload_to=get_upload_to_contract)

    def __str__(self):
        return f"{self.name}: {self.contract_file.url}"


class UserBaseModel(models.Model):
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name_kana = models.CharField(max_length=255, validators=[validate_katakana])
    first_name_kana = models.CharField(max_length=255, validators=[validate_katakana])
    phone = models.CharField(max_length=20)
    registration_date = models.DateTimeField(auto_now_add=True)
    service_use_contract = models.ForeignKey(ServiceUseAgreement, on_delete=models.CASCADE, null=True, blank=True)
    confidentiality_contract = models.ForeignKey(ConfidentialityAgreement, on_delete=models.CASCADE, null=True, blank=True)
    outsourcing_contract = models.ForeignKey(OutsourcingAgreement, on_delete=models.CASCADE, null=True, blank=True)
    postal_code = models.CharField(max_length=10, help_text="郵便番号ハイフンなし")
    address_1 = models.CharField(max_length=255, help_text="番地まで")
    address_2 = models.CharField(max_length=255, help_text="ビルやアパートの名称◎号室", null=True, blank=True)
    notification_email = models.EmailField(null=True, blank=True)

    class Meta:
        abstract = True


class UserTypeManager(models.Manager):
    pass


class UserType(TimeStampedModel):
    type_id = models.CharField(unique=True, max_length=10)
    name = models.CharField(max_length=50)

    objects = UserTypeManager()

    def __str__(self):
        return self.name


class MemberManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)

    def check_referral_id(self, referral_id):
        return self.filter(referral_id=referral_id).exists()

    def create_referral_id(self):
        referral_id = uuid.uuid4().hex[:5]
        if self.check_referral_id(referral_id):
            self.create_referral_id()
        return referral_id


class Member(UserBaseModel, TimeStampedModel):
    user_type = models.OneToOneField(UserType, related_name='members', on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='member_profiles')
    referral_id = models.CharField(max_length=100)
    last_modifier = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='member_last_modifier')
    last_modified = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_terminated = models.BooleanField(default=False)

    objects = MemberManager()

    def __str__(self):
        return f"{self.user_type} - {self.last_name} {self.first_name}({self.last_name_kana} {self.first_name_kana}) - {self.referral_id}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_type', 'user'], name='unique_user_type_user')
        ]


class MemberProfileManager(models.Manager):
    pass


class MemberProfile(TimeStampedModel):
    member = models.ForeignKey(Member, related_name='member', on_delete=models.CASCADE)
    gender = models.CharField(max_length=2, choices=GENDER_TYPE)
    birth = models.DateField(null=True, blank=True)
    description = models.TextField(null=True, blank=True, help_text='簡易的な経歴等の記載', verbose_name='自己PR')
    port_folio = models.URLField(null=True, blank=True)
    resume = models.FileField(upload_to=get_upload_to_resume, null=True, blank=True)  # 動的パス


    objects = MemberProfileManager()

class CustomerManager(models.Manager):
    pass


class Customer(UserBaseModel, TimeStampedModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='customer_profiles')
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name='組織・企業・団体名')
    customer_type = models.CharField(max_length=50, choices=CUSTOMER_TYPES)
    billing_email = models.EmailField(null=True, blank=True)
    payment_due_day = models.IntegerField(null=True, blank=True)
    referral_member = models.ForeignKey(Member, related_name='referral_member', blank=True, null=True, on_delete=models.CASCADE)
    service_started = models.DateField(null=True, blank=True)
    last_modifier = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL, related_name='customer_last_modifier')
    last_modified = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_terminated = models.BooleanField(default=False)

    objects = CustomerManager()

    def __str__(self):
        return f"{self.customer_type} - {self.name}"


class LoginStatusManager(models.Manager):
    pass


class LoginStatus(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    is_customer = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = LoginStatusManager()


class BankAccount(TimeStampedModel):
    bank_name = EncryptedCharField(max_length=255)
    branch_name = EncryptedCharField(max_length=255)
    account_number = EncryptedCharField(max_length=20)
    account_holder = EncryptedCharField(max_length=255)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default='savings')

    class Meta:
        abstract = True


class CustomerBankAccountManager(models.Manager):
    pass


class CustomerBankAccount(BankAccount):
    '''
    バーチャル口座番号を発行するので、顧客に支払いをしてもらう口座紐づきテーブル
    '''
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='customer_bank')

    objects = CustomerBankAccountManager()

    def __str__(self):
        return f"{self.customer} - {self.account_number} ({self.get_account_type_display()})"


class MemberBankAccountManager(models.Manager):
    pass


class MemberBankAccount(BankAccount):
    '''
    つな○○に報酬を支払うための口座紐づきテーブル
    '''
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='member_bank')

    objects = MemberBankAccountManager()

    def __str__(self):
        return f"{self.member} - {self.bank_name} - {self.account_number}"


class DiscountManager(models.Manager):
    pass


class Discount(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='discounts')
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # 数値指定の値引き
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)  # 割合での値引き

    objects = DiscountManager()

    def apply_discount(self, original_price):
        if self.discount_amount:
            return max(original_price - self.discount_amount, 0)
        elif self.discount_percentage:
            return max(original_price * (1 - self.discount_percentage / 100), 0)
        else:
            return original_price