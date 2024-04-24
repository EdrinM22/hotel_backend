from django.db import models
from users.models import Guest
# Create your models here.


class Feedback(models.Model):
    class Meta:
        db_table = 'feedback'

    stars = models.IntegerField()
    text = models.TextField(null=True, blank=True)
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE)
    date_time_created = models.DateTimeField(auto_now_add=True)
