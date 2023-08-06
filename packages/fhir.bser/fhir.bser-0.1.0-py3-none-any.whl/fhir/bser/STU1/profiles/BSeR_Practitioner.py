# -*- coding: utf-8 -*-
"""
Profile: http://hl7.org/fhir/us/bser/StructureDefinition/BSeR-Practitioner
BSeR Release: STU1
BSeR Version: 1.0.0
FHIR Version: 4.0.1
"""

from fhir.resources.practitioner import Practitioner
import typing
from fhir.resources import fhirtypes
from pydantic import Field, validator


class BSeR_Practitioner(Practitioner):
    profile_url = "http://hl7.org/fhir/us/bser/StructureDefinition/BSeR-Practitioner"
    # TODO: Implement - DEPENDENCY US CORE PRACTITIONER