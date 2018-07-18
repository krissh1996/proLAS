# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
#from django.core.urlresolvers import reverse



# Create your models here.
class LASFile(models.Model):
    Filename = models.CharField(max_length=100)
    file = models.FileField()

    def __str__(self):
        return self.Filename