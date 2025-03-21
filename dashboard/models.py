from django.db import models
from account.models import Customer, Member, UserType
from utils.abs_model import TimeStampedModel

DRAFT = "draft"
REGISTRATION_COMPLETE = "registration_complete"
PROJECT_CANCELED = "project_canceled"
PROJECT_ACCEPTED = "project_accepted"
IN_PROGRESS = "in_progress"
COMPLETION = "completion"
REVIEW = "review"
PROJECT_COMPLETED = "project_completed"


STATUS = [
    (DRAFT, '下書'),
    (REGISTRATION_COMPLETE, '登録完了'),
    (PROJECT_CANCELED, 'キャンセル'),
    (PROJECT_ACCEPTED, '請負済'),
    (IN_PROGRESS, '遂行中'),
    (COMPLETION, '遂行完了'),
    (REVIEW, 'レビュー'),
    (PROJECT_COMPLETED, '案件完了'),
]


class Grade(TimeStampedModel):
    """
    つなスパの時給を登録していく。そこから自動計算。
    Grade-1 1000
    Grade-2 1200
    Grade-3 1500
    Grade-4 1800
    Grade-5 2000
    Grade-6 2500
    Grade-7 3000
    Grade-8 3500
    Grade-9 4000
    """
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Project(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE)
    estimated_hours = models.IntegerField(help_text="見込時間（時間単位）")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS)
    entry_not_allowed = models.BooleanField(default=False)
    tuna_con = models.ForeignKey(Member, related_name='tuna_con_member', blank=True, null=True, on_delete=models.CASCADE)
    tuna_spa = models.ForeignKey(Member, related_name='tuna_spa_member', blank=True, null=True, on_delete=models.CASCADE)
    tuna_spa_helper = models.ForeignKey(Member, related_name='tuna_spa_member_helper', blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Entry(TimeStampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    canceled = models.BooleanField(default=False)


class ChatMessage(TimeStampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    message = models.TextField()
    is_draft = models.BooleanField(default=False)


class Cancellation(TimeStampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='cancellations')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='cancellations')
    tuna_type = models.ForeignKey(UserType, on_delete=models.CASCADE, related_name='cancellations')

    def __str__(self):
        return f"{self.project.name} - {self.member.name} - {self.tuna_type}"


class MainTag(TimeStampedModel):
    name = models.CharField(max_length=255)


class SubTag(TimeStampedModel):
    main = models.ForeignKey(MainTag, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)


