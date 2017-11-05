from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(
        max_length=255,
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

    @classmethod
    def create(cls, name, parent=None):
        return cls.objects.create(name=name, parent=parent)


class Channel(models.Model):
    categories = models.OneToOneField(
        Category,
        on_delete=models.CASCADE,
        related_name='root_of',
    )
    name = models.CharField(
        max_length=255,
        null=False,
        blank=False,
        unique=True,
    )

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, name):
        cls.objects.create(name=name)


@receiver(pre_save, sender=Channel)
def create_root_categories(sender, instance, **kwargs):
    '''
    add categories root if it doesnt exist
    '''
    if not hasattr(instance, 'categories'):
        cat = Category.create(instance.name)
        instance.categories = cat
