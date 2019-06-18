import datetime
import uuid

from django.db import models


class SoftDeletionQueryset(models.QuerySet):
    """Queryset implementing soft deletion behaviour"""

    def existing(self):
        return self.filter(deleted_at=None)

    def deleted(self):
        return self.exclude(deleted_at=None)

    def delete(self):
        now = datetime.datetime.utcnow()
        return super().update(
            deleted_at=now,
            updated_at=now
        )

    def hard_delete(self):
        return super().delete()


class SoftDeletionManager(models.Manager):
    """Customer manager for soft deletion."""

    queryset_class = SoftDeletionQueryset

    def __init__(self, *args, **kwargs):
        self.existing_only = kwargs.pop('existing_only', True)
        super().__init__(*args, **kwargs)

    def get_queryset(self):
        if self.existing_only:
            return self.queryset_class(self.model).existing()
        return self.queryset_class(self.model)


class SoftDeletionModelMixin(models.Model):
    """Model mixin implementing soft deletion as default."""

    deleted_at = models.DateField(blank=True, null=True, db_index=True)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(existing_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = datetime.datetime.utcnow()
        self.save()

    def hard_delete(self, **kwargs):
        super().delete(**kwargs)


class TimeStampedModelMixin(models.Model):
    """Mixin implementing timestamps to models"""

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False
    )
    updated_at = models.DateField(
        auto_now=True
    )

    class Meta:
        abstract = True


class ModelDefaultFieldsMixin(models.Model):
    """Mixin implementing default fields for all models."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.__class__.__name__} ID: {self.id}'


class BaseModel(ModelDefaultFieldsMixin,
                TimeStampedModelMixin,
                SoftDeletionModelMixin):

    class Meta:
        abstract = True


class BaseModelHardDelete(ModelDefaultFieldsMixin,
                          TimeStampedModelMixin):

    class Meta:
        abstract = True
