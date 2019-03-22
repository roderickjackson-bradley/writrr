
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
  follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)

  User.profile = property(lambda u: Profile.objects.get_or_create(user=u)[0])