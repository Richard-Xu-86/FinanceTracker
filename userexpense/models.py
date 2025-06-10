from django.db import models #Gives access to Django’s ORM for defining DB tables.
from django.contrib.auth.models import User #Links each expense to a registered user.
from django.utils.timezone import now

class Expense(models.Model): #new database table
    amount = models.FloatField()
    date = models.DateField(default=now)
    decription = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)#Foreign key to the user who owns this expense. If the user is deleted, the expense will be too.
    category = models.CharField(max_length=255)

    def __str__(self):
        return self.category

    class Meta:
        ordering = ['-date']

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural='Categroies'

    def __str__(self):
        return self.name
    
class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)
    amount = models.FloatField()
    month = models.DateField()  # represents the month the budget applies to

    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.month.strftime('%B %Y')}"


            