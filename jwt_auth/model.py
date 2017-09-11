from django.db import models

class TokenBlackList(models.Model):
    """
    Provide deleting token action. Token in the black list is invalid
    """
    token = models.CharField(max_length=200)
    expire = models.DateTimeField()
