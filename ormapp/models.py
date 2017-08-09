#coding:utf-8
from django.db import models
from django.contrib.auth.models import AbstractUser,Group
from django.core import validators

# class MyUser(AbstractUser):
#     uname = models.CharField(
#         max_length=30,
#         unique=True,
#         help_text=('Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.'),
#         # validators=[
#         #     validators.RegexValidator(
#         #         r'^[\w.@+-]+$',
#         #         _('Enter a valid username. This value may contain only '
#         #           'letters, numbers ' 'and @/./+/-/_ characters.')
#         #     ),
#         # ],
#         error_messages={
#             'unique': ("A user with that username already exists."),
#         },
#     )
#     class Meta:
#         verbose_name=u'用户'
#         verbose_name_plural=verbose_name
