from django.db import models
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from mptt.models import MPTTModel, TreeForeignKey


class Channel(MPTTModel):
    name = models.CharField(max_length=255)
    path = models.TextField(null=False)
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True
    )

    class MPTTMeta:
        """
        Insertion in the tree is ordered by name
        """
        order_insertion_by = ['name']

    class Meta:
        """
        Unique constraint to prevent duplicate category
        in the same tree level
        """
        unique_together = (('name', 'parent'),)

    def save(self, *args, **kwargs):
        """
        Override to call clean for manually created objects
        """
        self.clean()
        super(Channel, self).save(*args, **kwargs)

    def clean(self):
        """
        Strip leading and trailing spaces and
        check for channel name uniqueness
        """
        self.name = self.name.strip()
        if self.pk is None and self.is_channel():
            if Channel.objects.filter(name=self.name, parent=None).exists():
                raise ValidationError('Channel name already exists.')

    def __str__(self):
        return self.name

    @classmethod
    def create(cls, name, parent=None):
        """
        Create a channel with custom name
        name: the name of the channel
        returns: the created channel instance
        """
        return cls.objects.create(name=name, parent=parent)

    @classmethod
    def get_all_channels(cls):
        """
        Get all the channels as a queryset
        returns: queryset
        """
        return cls.objects.filter(parent=None)

    @property
    def channel(self):
        """
        Get the channel this category belongs to
        returns: instance of channel
        """
        return self.get_root()

    def is_channel(self):
        """
        Check if is instance of a channel
        returns: boolean
        """
        return self.parent == None

    def add_category(self, path):
        """
        Add a new category to the channel
        path: list containing the path to the category
        returns: the category added
        """
        head, *tail = path
        parent, _ = Channel.objects.get_or_create(name=head,
                                                  parent=self)
        path = parent.name
        parent.path = path
        parent.save()
        for element in tail:
            parent, _ = Channel.objects.get_or_create(name=element,
                                                      parent=parent)
            path = '/'.join([path, parent.name])
            parent.path = path
            parent.save()
        return parent

    def get_categories_count(self):
        """
        Get the number of categories in this channel
        returns: count of categories that belongs to this
        channel
        """
        tree_id = self.tree_id
        count = Channel.objects.filter(tree_id=tree_id).count()
        return count - 1  # not including the root

    def get_category(self, name):
        """
        Get the category by the name in this channel
        name: the lookup name (exact match)
        return: a category or raise does not exist error
        """
        try:
            category = Channel.objects.get(tree_id=self.tree_id, name=name)
            return category
        except Channel.DoesNotExist:
            raise

    def get_all_categories_paths(self):
        """
        Get all the categories of this channel
        the result is a list of strings (paths)
        returns: all paths of categories that belongs
        to this channel
        """
        all_categories = self.get_descendants(include_self=True)
        return [category.path for category in all_categories[1:]]
