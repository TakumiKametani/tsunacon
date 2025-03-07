from django.db import models
from account.models import CustomUser
from utils.abs_model import TimeStampedModel
# Create your models here.

ANNOUNCE_TYPE = [
    ('all', '未ログインの方も含む'),
    ('membership', 'ログインしている方へ'),
    ('customer', '顧客様へ'),
    ('member', 'つな会員様へ'),
    ('employee', '従業員へ'),
]

class Announcement(TimeStampedModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    target_audience = models.CharField(max_length=50, choices=ANNOUNCE_TYPE, help_text='周知するタイプの選択')

    def __str__(self):
        return self.title


class UserAnnouncement(TimeStampedModel):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'announcement')

    def __str__(self):
        return f"{self.user.username} - {self.announcement.title}"