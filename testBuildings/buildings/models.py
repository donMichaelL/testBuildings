from __future__ import unicode_literals
from django.db import models
from django.conf import settings


COUNTRIES_CHOICES = (
    ('gr', 'Greece'),
    ('rm', 'Romania'),
    ('bg', 'Bulgaria'),
    ('it', 'Italy'),
)

class Building(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=80)
    country = models.CharField(max_length=2, choices=COUNTRIES_CHOICES)
    address = models.CharField(max_length=30, null=True, blank=True)
    tk = models.PositiveIntegerField(verbose_name="Postcode", null=True, blank=True)
    max_evacuation_time = models.PositiveIntegerField(verbose_name="Maximum Evacuation Time", help_text="in seconds",null=True, blank=True, default=0)
    photo = models.ImageField(upload_to='building_images/', null=True, blank=True, help_text="Supported Formats: png, jpg, jpeg, bmp")
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ['-updated']

    def __unicode__(self):
        return self.name


class Floor(models.Model):
    building = models.ForeignKey(Building)
    name = models.CharField(max_length=60)
    number = models.SmallIntegerField(verbose_name="Floor Level")
    blueprint = models.ImageField(upload_to='blueprints/', null=True, blank=True)
    max_evacuation_time = models.PositiveIntegerField(verbose_name="Maximum Evacuation Time", help_text="in seconds",null=True, blank=True, default=0)
    stud_number = models.PositiveIntegerField(verbose_name="Number of students", null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        ordering = ['number']

    def __unicode__(self):
        return self.name
