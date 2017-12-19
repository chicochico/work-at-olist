from django.db import models
from django.core.exceptions import ValidationError
from mptt.models import MPTTModel, TreeForeignKey


class CategoryManager(models.Manager):
    """
    Categories manager
    """
    def get_queryset(self):
        """
        A category is a tree node with a parent
        """
        return super(CategoryManager, self).get_queryset().exclude(parent=None)


class ChannelManager(models.Manager):
    """
    Class for managing channels
    """
    def get_queryset(self):
        """
        A channel is a tree node without a parent
        """
        return super(ChannelManager, self).get_queryset().filter(parent=None)


class Node(MPTTModel):
    name = models.CharField(max_length=255)
    path = models.TextField(null=True, blank=True)
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

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        """
        Override to call clean for manually created objects
        """
        self.full_clean()
        super(Node, self).save(*args, **kwargs)

    @property
    def subcategories(self):
        """
        Get all the subcategories of this node
        returns: queryset of subcategories that belong to this node
        """
        return self.get_descendants(include_self=False)

    @property
    def subcategories_count(self):
        """
        Get the number of subcategories in this node
        returns: count of subcategories that belongs to this node
        """
        return Category.objects.filter(tree_id=self.tree_id).count()


class Category(Node):
    objects = CategoryManager()

    class Meta:
        proxy = True
        verbose_name_plural = 'Categories'

    def clean(self):
        """
        Strip leading and trailing empty spaces
        check if parent is present, and create path
        if empty
        """
        if self.parent is None:
            raise ValidationError(
                {'parent': 'Parent cannot be empty.'}
            )

        self.name = self.name.strip()
        self.path = self.parent.path + '/{}'.format(self.name)

    @property
    def channel(self):
        """
        Get the channel this category belongs to
        returns: instance of channel
        """
        return Channel.objects.get(tree_id=self.tree_id)


class Channel(Node):
    objects = ChannelManager()

    class Meta:
        proxy = True

    def clean(self):
        """
        Strip trailing and leading empty spaces
        and validate empty parent
        """
        if self.parent:
            raise ValidationError(
                {'parent': 'A channel contains no parent.'}
            )

        self.name = self.name.strip()
        self.path = '/{}'.format(self.name)

    def validate_unique(self, *args, **kwargs):
        """
        A channel name should be unique
        """
        super(Channel, self).validate_unique(*args, **kwargs)
        if not self.pk:
            if self.__class__.objects.filter(name=self.name).exists():
                raise ValidationError(
                    {'name': 'Channel with this name already exists.'}
                )

    def get_category(self, name):
        """
        Get the category by the name in this channel
        name: the lookup name (exact match)
        return: a category or raise does not exist error
        """
        try:
            category = Category.objects.get(tree_id=self.tree_id, name=name)
            return category
        except Channel.DoesNotExist:
            raise

    def add_category(self, path):
        """
        Add a new category to the channel
        path: list containing the path to the category
        returns: the category added
        """
        head, *tail = path
        parent, _ = Category.objects.get_or_create(name=head,
                                                   parent=self)
        path = parent.name
        parent.path = path
        parent.save()
        for element in tail:
            parent, _ = Category.objects.get_or_create(name=element,
                                                       parent=parent)
            path = '/'.join([path, parent.name])
            parent.path = path
            parent.save()
        return parent
