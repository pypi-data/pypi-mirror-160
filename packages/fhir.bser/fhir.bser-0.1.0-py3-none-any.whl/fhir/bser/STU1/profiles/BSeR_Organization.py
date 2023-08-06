# -*- coding: utf-8 -*-
"""
Profile: http://hl7.org/fhir/us/bser/StructureDefinition/BSeR-Organization
BSeR Release: STU1
BSeR Version: 1.0.0
FHIR Version: 4.0.1
"""

from fhir.resources.organization import Organization
import typing
from fhir.resources import fhirtypes
from pydantic import Field, validator


class BSeR_Organization(Organization):
    profile_url = "http://hl7.org/fhir/us/bser/StructureDefinition/BSeR-Organization"
    # TODO: Implement - DEPENDENCY US CORE ORGANIZATION