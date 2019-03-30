from django.db import models


class Chama(models.Model):
    """Model representing a chama
    """
    groupName = models.CharField(_(""), max_length=50)

class Receipt(models.Model):
    pass

class Transaction(models.Model):
    pass

class LoanRequest(models.Model):
    pass

class Meeting(models.Model):
    pass
