from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from mptt.models import MPTTModel, TreeForeignKey
from mptt.fields import TreeOneToOneField


class CategoryTree(MPTTModel):
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

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = (('name', 'tree_id'),)
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, name, parent=None):
        return cls.objects.create(name=name, parent=parent)

    def get_full_path(self):
        """get the path from the root to the category"""
        ancestors = self.get_ancestors(include_self=True)
        # start from 1 because 0 is the root of the tree
        return '/'.join([node.name for node in ancestors[1:]])


class Channel(models.Model):
    categories = TreeOneToOneField(
        CategoryTree,
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
        return cls.objects.create(name=name)

    def add_category(self, path):
        """path is a list containing the path to the category"""
        head, *tail = path
        parent, _ = CategoryTree.objects.get_or_create(name=head,
                                                       parent=self.categories)
        for element in tail:
            parent, _ = CategoryTree.objects.get_or_create(name=element,
                                                           parent=parent)

    def get_categories_count(self):
        tree_id = self.categories.tree_id
        count = CategoryTree.objects.filter(tree_id=tree_id).count()
        return count - 1  # not including the root

    def get_category(self, name):
        """get a category path by its name"""
        tree_id = self.categories.tree_id
        try:
            category = CategoryTree.objects.get(tree_id=tree_id, name=name)
            return category.get_full_path()
        except Category.DoesNotExist:
            raise

    def get_all_categories(self):
        """
        get all the categories of this channel
        the result is a list of lists
        """
        all_categories = CategoryTree.objects.get(root_of=self).get_family()
        return [category.get_full_path() for category in all_categories[1:]]


@receiver(pre_save, sender=Channel)
def create_root_categories(sender, instance, **kwargs):
    """add categories root if it doesnt exist"""
    if not hasattr(instance, 'categories'):
        cat = CategoryTree.create(instance.name + '_root')
        instance.categories = cat
