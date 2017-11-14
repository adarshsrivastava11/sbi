# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Account(models.Model):
    acc_no = models.CharField(max_length=11)
    created = models.BooleanField()
