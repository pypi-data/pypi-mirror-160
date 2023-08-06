# -*- coding: utf-8 -*-
"""
Profile: http://hl7.org/fhir/us/bser/StructureDefinition/BSeR-ServiceDeliveryLocation
BSeR Release: STU1
BSeR Version: 1.0.0
FHIR Version: 4.0.1
"""

from fhir.resources.location import Location
import typing
from fhir.resources import fhirtypes
from pydantic import Field, validator


class BSeR_ServiceDeliveryLocation(Location):
    profile_url = "http://hl7.org/fhir/us/bser/StructureDefinition/BSeR-ServiceDeliveryLocation"

    meta: fhirtypes.MetaType = Field(
        {"profile": [profile_url]},
        alias="meta",
        title="Metadata about the resource",
        description=(
            "The metadata about the resource. This is content that is maintained by"
            " the infrastructure. Changes to the content might not always be "
            "associated with version changes to the resource."
        ),
        element_property=True,
    )

    telecom: typing.List[fhirtypes.ContactPointType] = Field(
        None,
        alias="telecom",
        title="Contact details of the location",
        description=(
            "The contact details of communication devices available at the "
            "location. This can include phone numbers, fax numbers, mobile numbers,"
            " email addresses and web sites."
        ),
        # if property is element of this resource.
        element_property=True,
    )

    @validator('telecom')
    def check_telecom(cls, telecoms):
        '''telecom 0..*, telecom.system 1..1, telecom.value 1..1'''
        for telecom in telecoms:
            if telecom.system is None and telecom.value is None:
                raise ValueError('system and value are required')
            elif telecom.system is None:
                raise ValueError('system is required')
            elif telecom.value is None:
                raise ValueError('value is required')
        return telecoms
