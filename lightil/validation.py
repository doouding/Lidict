#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Define common use validators
"""
from django.core.validators import BaseValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class ExactLengthValidator(BaseValidator):
    message = _("Wrong string length")
    value = 0

    def compare(self, a, b):
        return a != b

    def clean(self, x):
        return len(x)
