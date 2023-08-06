# -*- coding: utf-8 -*-
"""
Profile: http://hl7.org/fhir/us/bser/StructureDefinition/BSeR-ReferralTask
BSeR Release: STU1
BSeR Version: 1.0.0
FHIR Version: 4.0.1
"""

from fhir.resources.task import Task
import typing
from fhir.resources import fhirtypes
from pydantic import Field, validator


class BSeR_ReferralTask(Task):
    profile_url = "http://hl7.org/fhir/us/bser/StructureDefinition/BSeR-ReferralTask"
    # TODO: Implement