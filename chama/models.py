from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from djmoney.models.fields import MoneyField
import uuid
from django.core.exceptions import ObjectDoesNotExist
from datetime import timedelta
import datetime
import math


class Member(AbstractUser):
    phone_number = models.CharField(
        unique=True, max_length=10)
    email = models.EmailField(max_length=254, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def __str__(self):
        return self.email

    def get_chamas(self):
        """Get all the chamas where the user is either an admin or a member"""
        ismember = self.chama.all().count()
        isadmin = self.admin.all().count()
        total = isadmin + ismember
        return total

    def get_my_savings(self):
        """Get all the user's savings"""
        transactions = self.transactions.all()
        savings = 0
        for transaction in transactions:
            if transaction.transaction_type == 'd':
                i = transaction.amount
                savings += i

        return savings

    def get_my_loans(self):
        loans = self.my_loan_requests.filter(
            is_approved=True).filter(is_paid=False)
        total = 0
        for loan in loans:
            i = loan.amount
            total += i
        return total

    def my_chama_shares(self):
        pass


class Chama(models.Model):
    """Model representing a chama
    """
    chama_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
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

    class Meta:
        ordering = ['groupName']

    def __str__(self):
        return self.groupName

    def get_absolute_url(self):
        return reverse("chama_detail", kwargs={"pk": self.pk})

    def get_members(self):
        """Get number of members"""
        members = self.members.all().count() + 1
        return members

    def get_admin(self):
        """Get admin"""
        return self.created_by

    def get_arrears(self):
        # get all payments that have been approved
        # get all
        pass

    def member_shares(self, member):
        """Get members equity in percentage"""
        member = self.members.get(member)
        member_transactions = self.transactions.filter(
            member=member).filter(transaction_type='d')

        # get total deposits for a single user
        total = 0
        for i in member_transactions:
            amount = i.amount
            total += amount
        return total

        # get percentage
        balance = self.get_total_balance

        shares = (total / balance) * 100
        member_shares = math.trunc(2, shares)
        return member_shares

    def get_total_balance(self):
        """Get account balance"""
        loans = self.loan_requests.filter(is_approved=True)
        total_loans = 0
        for loan in loans:
            amount = loan.amount
            total_loans += amount

        # Get total income
        payments = self.transactions.all()
        total_income = 0
        for payment in payments:
            amount = payment.amount
            total_income += amount

        balance = total_income - total_loans
        return balance

    def get_next_meeting(self):
        """Get meeting coming up in four weeks days."""
        months_time = datetime.date.today() + datetime.timedelta(weeks=4)
        meeting = self.meetings.get(meeting_date__lt=months_time)
        return meeting

    def total_approved_loans(self):
        """get all loans that have been approved in this chama"""
        loans = self.loan_requests.filter(is_approved=True)
        total_loans = 0
        for i in loans:
            amount = i.amount
            total_loans += amount
        return total_loans


class Transaction(models.Model):
    """This model defines all the transactions that take place, e.g fines or deposits
    Also includes the user who carried out the transaction and the code.
    """
    chama = models.ForeignKey(
        Chama, on_delete=models.DO_NOTHING, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_time = models.DateTimeField(auto_now_add=False)

    phone_number = models.CharField(blank=True, max_length=10)
    member = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, on_delete=models.DO_NOTHING, related_name='transactions')
    PAYMENT_TYPE = (
        ('f', 'Fine'),
        ('d', 'Deposit'),
        ('l', 'Loan')
    )
    transaction_type = models.CharField(max_length=1, choices=PAYMENT_TYPE,
                                        blank=True, default='d', help_text='I am paying for? Deposit,Fine or Loan')

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.phone_number

    def get_loans_total(self):
        pass

    def get_fines_total(self):
        pass


class LoanRequests(models.Model):
    """This model stores all the user requests for a loan in a particular chama"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, related_name='my_loan_requests')
    is_approved = models.BooleanField(default=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    chama = models.ForeignKey(
        Chama, on_delete=models.DO_NOTHING, related_name='loan_requests')
    is_confirmed = models.BooleanField(default=False)
    is_paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.chama} {self.amount} {self.user.phone_number}'

    def get_absolute_url(self):
        return reverse("request-loan", kwargs={"pk": self.chama.pk})


class ChamaMeetings(models.Model):
    """Meetings with venues"""
    chama = models.ForeignKey(
        Chama, on_delete=models.DO_NOTHING, related_name='meetings')
    meeting_date = models.DateTimeField(blank=False, auto_now_add=False)
    location = models.TextField(blank=True, max_length=300)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'On {self.meeting_date}, at {self.location}'

    def get_date(self):
        return 'foo'

    def get_absolute_url(self):
        return reverse("chama-detail", kwargs={"pk": self.chama.pk})
