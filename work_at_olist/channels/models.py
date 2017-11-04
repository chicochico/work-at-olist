from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False
    )
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True
    )

    def __str__(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = (('name', 'parent'),)
        verbose_name_plural = 'categories'


class Channel(models.Model):
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        unique=True,
    )
    categories = models.OneToOneField(
        Category,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='root_of',
    )

    def __str__(self):
        return self.name

