from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from djmoney.models.fields import MoneyField
import uuid
from django.core.exceptions import ObjectDoesNotExist


class Member(AbstractUser):
    phone_number = models.CharField(
        unique=True, max_length=10)
    email = models.EmailField(max_length=254, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return self.email


class ChamaManager(models.Manager):
    def add_member(self, member):
        if member not in self.members.all():
            self.members_set.add(member)
        return

    def get_all_members(self):
        members = self.members.all()
        return members


class Chama(models.Model):
    """Model representing a chama
    """
    chama_id = models.UUIDField(default=uuid.uuid4,
                                help_text='Unique ID for this particular chama across whole app')
    groupName = models.CharField(max_length=255, unique=True)
    paybillNo = models.PositiveIntegerField(unique=True)
    contribution_amnt = models.DecimalField(
        max_digits=10, decimal_places=2)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='chama', blank=True)
    contribution_interval = models.PositiveIntegerField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='admin')

    objects = ChamaManager()

    class Meta:
        ordering = ['groupName']

    def __str__(self):
        return self.groupName

    def get_absolute_url(self):
        return reverse("chama_detail", kwargs={"pk": self.pk})

    def add_member(self, member):
        pass


class Transaction(models.Model):
    """This model defines all the transactions that take place, e.g fines or deposits
    Also includes the user who carried out the transaction and the code.
    """
    chama = models.ForeignKey(
        Chama, on_delete=models.DO_NOTHING, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_time = models.DateTimeField(auto_now_add=False)

    phone_number = models.CharField(
        unique=True, blank=True, max_length=10)
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, on_delete=models.DO_NOTHING, related_name='user')
    PAYMENT_TYPE = (
        ('f', 'Fine'),
        ('d', 'Deposit'),
        ('l', 'Loan')
    )
    transaction_type = models.CharField(max_length=1, choices=PAYMENT_TYPE,
                                        blank=True, default='d', help_text='I am paying for? Deposit,Fine or Loan')

    class Meta:
        ordering = ['chama']

    def __str__(self):
        return self.phone_number
