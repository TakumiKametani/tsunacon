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


class CategoryManager(models.Manager):
    pass


class Category(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField()

    objects = CategoryManager()

    def __str__(self):
        return self.name


class TagManager(models.Manager):
    pass


class Tag(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    categories = models.ForeignKey(Category, related_name="categories", on_delete=models.CASCADE)

    objects = TagManager()

    def __str__(self):
        return self.name


class ProjectManager(models.Manager):
    pass


class Project(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    categories = models.ManyToManyField(Category)
    tags = models.ManyToManyField(Tag)
    grade = models.PositiveSmallIntegerField(null=True, blank=True)
    estimated_hours = models.IntegerField(help_text="見込時間（時間単位）")
    customer = models.ForeignKey(Customer, null=True, blank=True, on_delete=models.CASCADE)
    client_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS)
    entry_not_allowed = models.BooleanField(default=False)
    tuna_con = models.ForeignKey(Member, related_name='tuna_con_member', blank=True, null=True, on_delete=models.CASCADE)
    tuna_spa = models.ForeignKey(Member, related_name='tuna_spa_member', blank=True, null=True, on_delete=models.CASCADE)
    tuna_spa_helper = models.ForeignKey(Member, related_name='tuna_spa_member_helper', blank=True, null=True, on_delete=models.CASCADE)

    objects = ProjectManager()

    def __str__(self):
        return self.name


class EntryManager(models.Manager):
    pass


class Entry(TimeStampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    canceled = models.BooleanField(default=False)

    objects = EntryManager()


class ChatMessageManager(models.Manager):
    pass


class ChatMessage(TimeStampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    message = models.TextField()
    is_draft = models.BooleanField(default=False)

    objects = ChatMessageManager()


class CancellationManager(models.Manager):
    pass


class Cancellation(TimeStampedModel):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='cancellations')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='cancellations')
    tuna_type = models.ForeignKey(UserType, on_delete=models.CASCADE, related_name='cancellations')

    objects = CancellationManager()

    def __str__(self):
        return f"{self.project.name} - {self.member.name} - {self.tuna_type}"

