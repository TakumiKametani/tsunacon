from django.db import models

class TimeStampedOrderingMixin(models.Model):
    class Meta:
        abstract = True

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        fields = list(cls._meta.fields)
        custom_fields = [f for f in fields if f.name not in ['created', 'modified']]
        cls._meta.ordering = [f.name for f in custom_fields] + ['created', 'modified']

class TimeStampedModel(TimeStampedOrderingMixin):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


