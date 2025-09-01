# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Employees(models.Model):
    employee_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    age = models.IntegerField(blank=True, null=True)
    mobile_number = models.CharField(unique=True, max_length=15)
    date_of_birth = models.DateField()
    date_of_joining = models.DateField()
    taken_leave = models.IntegerField(blank=True, null=True)
    available_leave = models.IntegerField(blank=True, null=True)
    sick_leave = models.IntegerField(blank=True, null=True)
    casual_leave = models.IntegerField(blank=True, null=True)
    aadhar_number = models.CharField(unique=True, max_length=12)
    pan_card_number = models.CharField(unique=True, max_length=10)

    class Meta:
        managed = False
        db_table = 'employees'
