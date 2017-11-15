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
        """
        Override save to check it channel name is unique
        """
        if Channel.objects.filter(name=self.name, parent=None):
            raise IntegrityError('Channel name already exists.')
        else:
            self.name = self.name.strip()  # remove trailing white spaces
            super(Channel, self).save(*args, **kwargs)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = (('name', 'parent'),)

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, name, parent=None):
        """
        Create a channel with name
        """
        return cls.objects.create(name=name, parent=parent)

    @classmethod
    def get_all_channels(cls):
        """
        Get all the channels as a queryset
        """
        return cls.objects.filter(parent=None)

    @property
    def channel(self):
        """
        Get the channel this category belongs to
        """
        return self.get_root()

    @property
    def path(self):
        """
        Get the path from the root to the category
        returns a string
        """
        ancestors = self.get_ancestors(include_self=True)
        # start from 1 because 0 is the root of the tree
        return '/'.join([node.name for node in ancestors[1:]])

    def add_category(self, path):
        """
        Add a new category to the channel
        path is a list containing the path to the category
        returns the category added
        """
        head, *tail = path
        parent, _ = Channel.objects.get_or_create(name=head.strip(),
                                                  parent=self)
        for element in tail:
            parent, _ = Channel.objects.get_or_create(name=element.strip(),
                                                      parent=parent)
        # return the added category
        return parent

    def get_categories_count(self):
        """
        Get the number of categories in this channel
        """
        tree_id = self.tree_id
        count = Channel.objects.filter(tree_id=tree_id).count()
        return count - 1  # not including the root

    def get_category(self, name):
        """
        Get the category by the name in this channel
        return a category or raise does not exist error
        """
        try:
            category = Channel.objects.get(tree_id=self.tree_id, name=name)
            return category
        except Channel.DoesNotExist:
            raise

    def get_all_categories(self):
        """
        Get all the categories of this channel
        the result is a list of strings (paths)
        """
        all_categories = self.get_descendants(include_self=True)
        return [category.path for category in all_categories[1:]]

