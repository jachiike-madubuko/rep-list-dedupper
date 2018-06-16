"""
Change your models (in models.py).
Run python django423/mysite/manage.py makemigrations dedupper to create migrations for those changes
Run python manage.py migrate dedupper to apply those changes to the database.
"""

from __future__ import unicode_literals

from django.db import models

def strip(string):
    newstring = string.replace(" ","")
    return  newstring


class Simple(models.Model):
    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128)
    category = models.CharField(max_length=128)
    average = models.IntegerField(null=True, blank=True)
    TYPES_OF_RECORD = (  ('Undecided', 'Undecided'),
        ('Duplicate', 'Duplicate'),
        ('New Record', 'New Record')  )
    type = models.CharField(max_length=128, choices=TYPES_OF_RECORD, default='Undecided')

    closest1 = models.ForeignKey('Simple', on_delete=models.CASCADE, related_name='the_closest', null=True, blank=True)
    closest2 = models.ForeignKey('Simple', on_delete=models.CASCADE, related_name='second_closest', null=True, blank=True)
    closest3 = models.ForeignKey('Simple', on_delete=models.CASCADE, related_name='third_closest', null=True, blank=True)

    def __str__(self):
        return '{} by {} \n\t has Record type: {}'.format(self.title, self.author, self.type, self.average)

    def key(self, key_parts):
        key=''

        key_builder = {
            'title': strip(self.title),
            'author': strip(self.author),
            'category': strip(self.category)
        }

        for part in key_parts:
            key += key_builder[part]
        return key


#TODO
#create contact model
#create rep_contact and sf_contact that inherit from contact
#set up model for SF contact
#for rep_contact make a match_contactID and make it unique

class Contact(models.Model):
    CRD = models.CharField( max_length=128, unique=True,  db_column="CRD")
    firstName = models.CharField(max_length=128, blank=True)
    lastName = models.CharField(max_length=128, blank=True)
    suffix = models.CharField(max_length=128, blank=True)
    canSellDate = models.CharField(max_length=128, blank=True)
    levelGroup = models.CharField(max_length=128, blank=True)
    mailingStreet = models.CharField(max_length=128, blank=True)
    mailingCity = models.CharField(max_length=128, blank=True)
    mailingStateProvince = models.CharField(max_length=128, blank=True)
    mailingZipPostalCode = models.CharField(max_length=128, blank=True)
    territory = models.CharField(max_length=128, blank=True)
    workPhone = models.CharField(max_length=128, blank=True)
    homePhone = models.CharField(max_length=128, blank=True)
    mobilePhone = models.CharField(max_length=128, blank=True)
    workEmail = models.CharField(max_length=128, blank=True)
    personalEmail = models.CharField(max_length=128, blank=True)
    otherEmail = models.CharField(max_length=128, blank=True)
    area = models.CharField(max_length=128, blank=True)
    region = models.CharField(max_length=128, blank=True)
    regionalLeader = models.CharField(max_length=128, blank=True)
    levelLeader = models.CharField(max_length=128, blank=True)
    fieldTrainerLeader = models.CharField(max_length=128, blank=True)
    performanceLeader = models.CharField(max_length=128, blank=True)
    boaName = models.CharField(max_length=128, blank=True)


    def __str__(self):
        return '{} {}'.format(self.firstName, self.lastName,)
    def key(self, key_parts):
        key = ''

        key_builder = {
            'CRD': strip(self.CRD),
            'firstName': strip(self.firstName),
            'lastName': strip(self.lastName),
            'suffix': strip(self.suffix),
            'canSellDate': strip(self.canSellDate),
            'levelGroup': strip(self.levelGroup),
            'mailingStreet': strip(self.mailingStreet),
            'mailingCity': strip(self.mailingCity),
            'mailingStateProvince': strip(self.mailingStateProvince),
            'mailingZipPostalCode': strip(self.mailingZipPostalCode),
            'territory': strip(self.territory),
            'ID': strip(self.ID),
            'workPhone': strip(self.workPhone),
            'homePhone': strip(self.homePhone),
            'mobilePhone': strip(self.mobilePhone),
            'workEmail': strip(self.workEmail),
            'personalEmail': strip(self.personalEmail),
            'otherEmail': strip(self.otherEmail),
            'area': strip(self.area),
            'region': strip(self.region),
            'regionalLeader': strip(self.regionalLeader),
            'levelLeader': strip(self.levelLeader),
            'fieldTrainerLeader': strip(self.fieldTrainerLeader),
            'performanceLeader': strip(self.performanceLeader),
            'boaName': strip(self.boaName),
        }

        for part in key_parts:
            key += key_builder[part]
        return key


class RepContact(models.Model):
    CRD = models.CharField(max_length=128, db_column="CRD")
    firstName = models.CharField(max_length=128, blank=True)
    lastName = models.CharField(max_length=128, blank=True)
    suffix = models.CharField(max_length=128, blank=True)
    canSellDate = models.CharField(max_length=128, blank=True)
    levelGroup = models.CharField(max_length=128, blank=True)
    mailingStreet = models.CharField(max_length=128, blank=True)
    mailingCity = models.CharField(max_length=128, blank=True)
    mailingStateProvince = models.CharField(max_length=128, blank=True)
    mailingZipPostalCode = models.CharField(max_length=128, blank=True)
    territory = models.CharField(max_length=128, blank=True)
    workPhone = models.CharField(max_length=128, blank=True)
    homePhone = models.CharField(max_length=128, blank=True)
    mobilePhone = models.CharField(max_length=128, blank=True)
    workEmail = models.CharField(max_length=128, blank=True)
    personalEmail = models.CharField(max_length=128, blank=True)
    otherEmail = models.CharField(max_length=128, blank=True)
    area = models.CharField(max_length=128, blank=True)
    region = models.CharField(max_length=128, blank=True)
    regionalLeader = models.CharField(max_length=128, blank=True)
    levelLeader = models.CharField(max_length=128, blank=True)
    fieldTrainerLeader = models.CharField(max_length=128, blank=True)
    performanceLeader = models.CharField(max_length=128, blank=True)
    boaName = models.CharField(max_length=128, blank=True)
    average = models.IntegerField(null=True, blank=True)
    TYPES_OF_RECORD = (('Undecided', 'Undecided'),
                       ('Duplicate', 'Duplicate'),
                       ('New Record', 'New Record'))
    type = models.CharField(max_length=128, choices=TYPES_OF_RECORD, default='Undecided')

    closest1 = models.ForeignKey('SFContact', on_delete=models.CASCADE, related_name="first_%(app_label)s_%("
                                                                                     "class)s_related",
        related_query_name="%(app_label)s_%(class)s", null=True,
                                 blank=True)
    closest2 = models.ForeignKey('SFContact', on_delete=models.CASCADE, related_name="second_%(app_label)s_%("
                                                                                     "class)s_related",
        related_query_name="%(app_label)s_%(class)ss", null=True,
                                 blank=True)
    closest3 = models.ForeignKey('SFContact', on_delete=models.CASCADE, related_name="third_%(app_label)s_%("
                                                                                     "class)s_related",
        related_query_name="%(app_label)s_%(class)sss", null=True,
                                 blank=True)
    dupFlag = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return '{} {}'.format(self.firstName, self.lastName,)
    def key(self, key_parts):
        key = ''

        key_builder = {
            'CRD': strip(self.CRD),
            'firstName': strip(self.firstName),
            'lastName': strip(self.lastName),
            'suffix': strip(self.suffix),
            'canSellDate': strip(self.canSellDate),
            'levelGroup': strip(self.levelGroup),
            'mailingStreet': strip(self.mailingStreet),
            'mailingCity': strip(self.mailingCity),
            'mailingStateProvince': strip(self.mailingStateProvince),
            'mailingZipPostalCode': strip(self.mailingZipPostalCode),
            'territory': strip(self.territory),
            'workPhone': strip(self.workPhone),
            'homePhone': strip(self.homePhone),
            'mobilePhone': strip(self.mobilePhone),
            'workEmail': strip(self.workEmail),
            'personalEmail': strip(self.personalEmail),
            'otherEmail': strip(self.otherEmail),
            'area': strip(self.area),
            'region': strip(self.region),
            'regionalLeader': strip(self.regionalLeader),
            'levelLeader': strip(self.levelLeader),
            'fieldTrainerLeader': strip(self.fieldTrainerLeader),
            'performanceLeader': strip(self.performanceLeader),
            'boaName': strip(self.boaName),
        }

        for part in key_parts:
            key += key_builder[part]
        return key


class SFContact(models.Model):
    CRD = models.CharField(max_length=128, unique=True, db_column="CRD")
    firstName = models.CharField(max_length=128, blank=True)
    lastName = models.CharField(max_length=128, blank=True)
    suffix = models.CharField(max_length=128, blank=True)
    canSellDate = models.CharField(max_length=128, blank=True)
    levelGroup = models.CharField(max_length=128, blank=True)
    mailingStreet = models.CharField(max_length=128, blank=True)
    mailingCity = models.CharField(max_length=128, blank=True)
    mailingStateProvince = models.CharField(max_length=128, blank=True)
    mailingZipPostalCode = models.CharField(max_length=128, blank=True)
    territory = models.CharField(max_length=128, blank=True)
    workPhone = models.CharField(max_length=128, blank=True)
    homePhone = models.CharField(max_length=128, blank=True)
    mobilePhone = models.CharField(max_length=128, blank=True)
    workEmail = models.CharField(max_length=128, blank=True)
    personalEmail = models.CharField(max_length=128, blank=True)
    otherEmail = models.CharField(max_length=128, blank=True)
    area = models.CharField(max_length=128, blank=True)
    region = models.CharField(max_length=128, blank=True)
    regionalLeader = models.CharField(max_length=128, blank=True)
    levelLeader = models.CharField(max_length=128, blank=True)
    fieldTrainerLeader = models.CharField(max_length=128, blank=True)
    performanceLeader = models.CharField(max_length=128, blank=True)
    boaName = models.CharField(max_length=128, blank=True)
    closest_rep = models.ForeignKey('RepContact', on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(class)s", null=True,
                                 blank=True)
    dupFlag = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return '{} {}'.format(self.firstName, self.lastName,)
    def key(self, key_parts):
        key = ''

        key_builder = {
            'CRD': strip(self.CRD),
            'firstName': strip(self.firstName),
            'lastName': strip(self.lastName),
            'suffix': strip(self.suffix),
            'canSellDate': strip(self.canSellDate),
            'levelGroup': strip(self.levelGroup),
            'mailingStreet': strip(self.mailingStreet),
            'mailingCity': strip(self.mailingCity),
            'mailingStateProvince': strip(self.mailingStateProvince),
            'mailingZipPostalCode': strip(self.mailingZipPostalCode),
            'territory': strip(self.territory),
            'workPhone': strip(self.workPhone),
            'homePhone': strip(self.homePhone),
            'mobilePhone': strip(self.mobilePhone),
            'workEmail': strip(self.workEmail),
            'personalEmail': strip(self.personalEmail),
            'otherEmail': strip(self.otherEmail),
            'area': strip(self.area),
            'region': strip(self.region),
            'regionalLeader': strip(self.regionalLeader),
            'levelLeader': strip(self.levelLeader),
            'fieldTrainerLeader': strip(self.fieldTrainerLeader),
            'performanceLeader': strip(self.performanceLeader),
            'boaName': strip(self.boaName),
        }

        for part in key_parts:
            key += key_builder[part]
        return key
