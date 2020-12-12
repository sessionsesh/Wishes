from django.db import models
from django.contrib.auth.models import User

class Relationship(models.Model):
    # Objects of relationship
    user1 = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user1')  # sender
    user2 = models.ForeignKey(User,on_delete=models.CASCADE, related_name='user2')  # receiver

    # Indicates, that first user or second user accept friendship
    # TODO: think about one field(is_accepted) instead of accept1 and accept
    accept1 = models.BooleanField(default=False)
    accept2 = models.BooleanField(default=False)

    # Relationship beginning date
    relation_start = models.DateTimeField(auto_now_add=True)
