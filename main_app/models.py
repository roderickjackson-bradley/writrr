from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

Rating = (
    ('5', '*****'),
    ('4', '****'),
    ('3', '***'),
    ('2', '**'),
    ('1', '*'),
    ('0', ''),
)

class Readrr (models.Model):
    name = models.CharField(max_length=50)
    bio = models.TextField(max_length=250)
    joined = models.DateField('Joined Date')
    email = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('readrrs_detail', kwargs={'pk': self.id})


class Writrr(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    bio = models.TextField(max_length=250)
    joined = models.DateField('Joined Date')
    readrrs = models.ManyToManyField(Readrr)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse ('detail', kwargs={'writrr_id' : self.id}) 


class Comment(models.Model):
    created = models.DateField('Comment Date')
    review = models.TextField(max_length=250)
    ratings = models.CharField(max_length=1,
    choices=Rating,
    default=Rating[0][0]
    )
    #Create a writrr_id FK
    writrr = models.ForeignKey(Writrr, on_delete=models.CASCADE)
    readrr = models.ForeignKey(Readrr, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_service_display()} on {self.date}"
    
    class Meta:
        ordering = ['-created']
    
class Opu(models.Model):
    url = models.CharField(max_length=200)
    writrr = models.ForeignKey(Writrr, on_delete=models.CASCADE)
    comments = models.ManyToManyField(Comment)

    def __str__(self):
        return f"Article for writrr_id: {self.writrr_id} @{self.url}"