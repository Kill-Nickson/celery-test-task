from django.db import models
from django.urls import reverse


class Schema(models.Model):
    title = models.CharField(max_length=255, null=False)

    separators = (
        (',', ','),
        (';', ';'),
    )

    column_separator = models.CharField(max_length=10, choices=separators, null=False)

    columns = models.CharField(max_length=1000, null=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('schema_detail', args=[str(self.pk)])


class Dataset(models.Model):
    schema = models.ForeignKey(
        Schema,
        on_delete=models.CASCADE,
        related_name='dataset',
    )
    date = models.DateTimeField(auto_now_add=True)

    statuses = (
        ('Processing', 'Processing'),
        ('Ready', 'Ready'),
    )

    status = models.CharField(max_length=30, choices=statuses, null=False)
    csv_file = models.FileField(upload_to='documents', blank=True, null=True)

    def __str__(self):
        return str(self.pk)
