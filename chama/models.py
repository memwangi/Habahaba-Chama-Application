from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Member(AbstractUser):
    phone_number = models.CharField(
        unique=True, max_length=10)
    email = models.EmailField(max_length=254, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return self.email


class Chama(models.Model):
    """Model representing a chama
    """
    groupName = models.CharField(max_length=50)
    paybillNo = models.IntegerField(unique=True)
    contribution_amnt = models.DecimalField(max_digits=10, decimal_places=2)

    member = models.ManyToManyField(
        settings.AUTH_USER_MODEL)

    def __str__(self):
        return self.groupName

    def get_absolute_url(self):
        return reverse("chama_detail", kwargs={"pk": self.pk})


class Transaction(models.Model):
    """This model defines all the transactions that take place, e.g fines or deposits
    Also includes the user who carried out the transaction and the code.
    """
    PAYMENT_TYPE = (
        ('f', 'Fine'),
        ('d', 'Deposit'),
        ('l', 'Loan')
    )
    chama = models.ForeignKey(Chama, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_time = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=1, choices=PAYMENT_TYPE,
                                        blank=True, default='d', help_text='I am paying for? Deposit,Fine or Loan')
    phone_number = models.CharField(
        unique=True, blank=True, max_length=10)

class LoanRequest(models.Model):
    pass


class Meeting(models.Model):
    pass
