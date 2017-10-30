from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255 ,null=False, blank=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    left = models.PositiveIntegerField(null=True, blank=True)
    rigth = models.PositiveIntegerField(null=True, blank=True)
    channel = models.ForeignKey('Channel', null=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Channel(models.Model):
    name = models.CharField(max_length=255 ,null=False, blank=False)

    def __str__(self):
        return self.name

