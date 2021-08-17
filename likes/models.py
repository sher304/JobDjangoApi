from django.db import models

from account.models import CustomUser
from main.models import Ads


# class Like(models.Model):
#     author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
#                                related_name='likes')
#     ads = models.ForeignKey(Ads, on_delete=models.CASCADE,
#                             related_name='likes')
#     object_id = model
