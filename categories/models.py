from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=250, blank=False, unique=True)
    parent = models.ForeignKey('self', models.CASCADE, blank=True, null=True,
                               related_name='children')

    class Meta:
        ordering = ('id', )

    def __repr__(self):
        return self.name
