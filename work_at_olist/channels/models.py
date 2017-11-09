from django.db import models
from django.db import IntegrityError
from mptt.models import MPTTModel, TreeForeignKey


class Channel(MPTTModel):
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

    def save(self, *args, **kwargs):
        """Override save to check it channel name is unique"""
        if Channel.objects.filter(name=self.name, parent=None):
            raise IntegrityError('Channel name already exists.')
        else:
            super(Channel, self).save(*args, **kwargs)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = (('name', 'tree_id'),)

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, name, parent=None):
        return cls.objects.create(name=name, parent=parent)

    @classmethod
    def get_all_channels(cls):
        return cls.objects.filter(parent=None)

    def get_full_path(self):
        """get the path from the root to the category"""
        ancestors = self.get_ancestors(include_self=True)
        # start from 1 because 0 is the root of the tree
        return '/'.join([node.name for node in ancestors[1:]])

    def add_category(self, path):
        """path is a list containing the path to the category"""
        head, *tail = path
        parent, _ = Channel.objects.get_or_create(name=head,
                                                       parent=self)
        for element in tail:
            parent, _ = Channel.objects.get_or_create(name=element,
                                                           parent=parent)

    def get_categories_count(self):
        tree_id = self.tree_id
        count = Channel.objects.filter(tree_id=tree_id).count()
        return count - 1  # not including the root

    def get_category(self, name):
        """get a category name"""
        try:
            category = Channel.objects.get(tree_id=self.tree_id, name=name)
            return category
        except Category.DoesNotExist:
            raise

    def get_all_categories(self):
        """
        get all the categories of this channel
        the result is a list of paths
        """
        all_categories = Channel.objects.filter(tree_id=self.tree_id)
        return [category.get_full_path() for category in all_categories[1:]]
