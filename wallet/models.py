from django.db import models

# Create your models here.
class Wallet(models.Model):
    """
    User's wallet
    """
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    deposit = models.FloatField()
    name = models.CharField(max_length=10)
    icon = models.CharField(max_length=10)
    credit_card = models.BooleanField()

class Transfer(models.Model):
    """
    Represent the transfer between one person's wallets
    """
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='source_wallet')
    destination = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='dest_wallet')
    amount = models.FloatField()
    description = models.CharField(max_length=50)
    title = models.CharField(max_length=20)
    transfer_time = models.DateTimeField(auto_now=True)

class Consum(models.Model):
    """
    Represent the consuming money
    """
    source = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.FloatField()
    description = models.CharField(max_length=50)
    title = models.CharField(max_length=20)
    consum_type = models.CharField(max_length=10)
    consum_time = models.DateTimeField(auto_now=True)

class ConsumType(models.Model):
    """
    User custom consuming type
    """
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
