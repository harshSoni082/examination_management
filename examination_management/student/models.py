from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from examination_management.core.behaviours import StatusMixin


class Student(StatusMixin, TimeStampedModel):
    application_no = models.CharField(_('Jee Mains Application No'), max_length=100, blank=True, null=True)
    roll_no = models.CharField(_('Roll Number'), max_length=100, primary_key=True)
    name = models.CharField(_('Name'), max_length=100, null=True, blank=True)
    fathers_name = models.CharField(_('Fathers Name'), max_length=100, null=True, blank=True)
    mothers_name = models.CharField(_('Mothers Name'), max_length=100, null=True, blank=True)
    category = models.CharField(_('Category'), max_length=50, null=True, blank=True)
    pwd = models.BooleanField(_('PwD'), default=False)

    gender_choices = (('M', 'Male'), ('F', 'Female'))
    gender = models.CharField(_('Gender'), max_length=1, choices=gender_choices, null=True, blank=True)

    dob = models.DateField(_('DOB'), blank=True, null=True)
    soe = models.CharField(_('State of Eligibility'), max_length=100, blank=True, null=True)
    address = models.CharField(_('Address'), max_length=500, blank=True, null=True)
    is_prep = models.BooleanField(_('Is Prep'), default=False)
    nationality = models.CharField(_('Nationality'), max_length=100, blank=True, null=True)
    branch = models.ForeignKey('branch.Branch', on_delete=models.SET_NULL, blank=True, null=True)
    allocated = models.BooleanField(_('Allocated'), default=True)
    mobile = models.CharField(_('Mobile'), max_length=14, blank=True, null=True)
    email = models.EmailField(_('Email'), null=True, blank=True, unique=True)
    batch = models.ForeignKey('batch.Batch', on_delete=models.CASCADE, blank=True, null=True)
    backlogs = models.IntegerField(_('Backlogs'), default=0)

    def __str__(self):
        return str(self.roll_no)