from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel

from examination_management.core.behaviours import StatusMixin


class Student(StatusMixin, TimeStampedModel):
    yes_no_choices = (('Yes', 'Yes'), ('No', 'No'))

    jee_application_no = models.CharField(_('Jee Mains Application No'), max_length=100, blank=True, null=True)
    roll_no = models.CharField(_('Roll Number'), max_length=100, primary_key=True)
    name = models.CharField(_('Name'), max_length=100, null=True, blank=True)
    fathers_name = models.CharField(_('Fathers Name'), max_length=100, null=True, blank=True)
    mothers_name = models.CharField(_('Mothers Name'), max_length=100, null=True, blank=True)
    category = models.CharField(_('Category'), max_length=50, null=True, blank=True)
    pwd = models.CharField(_('PwD'), max_length=3, choices=yes_no_choices, null=True, blank=True)

    gender_choices = (('Male', 'Male'), ('Female', 'Female'))
    gender = models.CharField(_('Gender'), max_length=7, choices=gender_choices, null=True, blank=True)

    dob = models.DateField(_('DOB'), blank=True, null=True)
    state_of_eligibility = models.CharField(_('State of Eligibility'), max_length=100, blank=True, null=True)
    address = models.TextField(_('Address'), max_length=500, blank=True, null=True)

    is_prep = models.CharField(_('Is Prep'), max_length=3, choices=yes_no_choices, null=True, blank=True)

    nationality = models.CharField(_('Nationality'), max_length=100, blank=True, null=True)
    branch = models.ForeignKey('branch.Branch', on_delete=models.SET_NULL, blank=True, null=True)
    allocated_cat = models.BooleanField(_('Allocated Category'), default=True)
    mobile = models.CharField(_('Mobile'), max_length=100, blank=True, null=True)
    email = models.EmailField(_('Email'), null=True, blank=True, unique=True)
    batch = models.ForeignKey('batch.Batch', on_delete=models.CASCADE, blank=True, null=True)
    backlogs = models.IntegerField(_('Backlogs'), default=0)

    remarks = models.TextField(_('Remarks'), blank=True, null=True)

    def save(self, *args, **kwargs):
        self.name = self.name.title()
        self.fathers_name = self.fathers_name.title()
        self.mothers_name = self.mothers_name.title()

        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.roll_no)