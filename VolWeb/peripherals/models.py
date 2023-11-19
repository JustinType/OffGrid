from django.db import models

# Create your models here.
# OS CHOICE
CHOICES = (
    ('Windows', 'Windows'),
    ('Linux', 'Linux'),
    #        ('MacOs', 'MacOs'), <- not implemented yet
)


class Peripheral(models.Model):

    name = models.TextField(max_length=512)
    description = models.TextField()
    os_version = models.CharField(max_length=50, choices=CHOICES)
    source_system = models.TextField(max_length=1024)

    bash_bunny_device = models.TextField(max_length=256)
    storage_device = models.TextField(max_length=256)

    def __str__(self):
        return self.name
