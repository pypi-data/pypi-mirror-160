# -*- coding: utf-8 -*-
"""
Profile: http://hl7.org/fhir/us/bser/StructureDefinition/BSeR-ReferralServiceRequest
BSeR Release: STU1
BSeR Version: 1.0.0
FHIR Version: 4.0.1
"""

from fhir.resources.servicerequest import ServiceRequest
import typing
from fhir.resources import fhirtypes
from pydantic import Field, validator


class BSeR_ReferralServiceRequest(ServiceRequest):
    profile_url = "http://hl7.org/fhir/us/bser/StructureDefinition/BSeR-ReferralServiceRequest"
    # TODO: Implement