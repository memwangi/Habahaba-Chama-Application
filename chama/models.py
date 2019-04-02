from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Chama(models.Model):
    """Model representing a chama
    """
    groupName = models.CharField(max_length=50)
    paybillNo = models.IntegerField(unique=True)
    contribution_amnt = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.groupName

    def get_absolute_url(self):
        return reverse("chama_detail", kwargs={"pk": self.pk})


class userProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    user_chama = models.ManyToManyField(
        Chama, related_name='member_of', symmetrical=False)


class Receipt(models.Model):
    pass


class Transaction(models.Model):
    """This model defines all the transactions that take place, e.g fines or deposits
    Also includes the user who carried out the transaction and the code.
    """
    TRANSACTION_TYPE = (
        ('f', 'Fine'),
        ('d', 'Deposit'),
    )
    chama = models.ForeignKey('Chama', on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_time = models.DateTimeField(auto_now_add=True)



class LoanRequest(models.Model):
    pass


class Meeting(models.Model):
    pass
