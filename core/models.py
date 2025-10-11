from django.contrib.auth.models import  AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=11,
        validators=[RegexValidator(r'^09\d{9}$')],
        blank= True,
        default=''
    )
    birth_date = models.DateField(blank=True, null=True)