# -*- coding: utf-8 -*-
"""
Profile: http://hl7.org/fhir/us/bser/StructureDefinition/BSeR-ReferralInitiatorPractitionerRole
BSeR Release: STU1
BSeR Version: 1.0.0
FHIR Version: 4.0.1
"""

from fhir.resources.practitionerrole import PractitionerRole
import typing
from fhir.resources import fhirtypes
from pydantic import Field, validator


class BSeR_ReferralInitiatorPractitionerRole(PractitionerRole):
    profile_url = "http://hl7.org/fhir/us/bser/StructureDefinition/BSeR-ReferralInitiatorPractitionerRole"

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

    practitioner: fhirtypes.ReferenceType = Field(
        ...,
        alias="practitioner",
        title="Practitioner that is able to provide the defined services for the organization",
        description="Practitioner that is able to provide the defined services for the organization.",
        element_property=True,
        element_required=True,
        enum_reference_types=["BSeR_Practitioner"],
    )

    organization: fhirtypes.ReferenceType = Field(
        ...,
        alias="organization",
        title="Organization where the roles are available",
        description="The organization where the Practitioner performs the roles associated.",
        element_property=True,
        element_required=True,
        enum_reference_types=["BSeR_Organization"],
    )

    location: typing.List[fhirtypes.ReferenceType] = Field(
        None,
        alias="location",
        title="The location(s) at which this practitioner provides care",
        description=None,
        # if property is element of this resource.
        element_property=True,
        # note: Listed Resource Type(s) should be allowed as Reference.
        enum_reference_types=["BSeR_ServiceDeliveryLocation"],
    )

    @validator('organization')
    def check_organization(cls, organization):
        '''organization 1..1'''
        if organization is None:
            raise ValueError('organization is required')
        return organization

    @validator('practitioner')
    def check_practitioner(cls, practitioner):
        '''practitioner 1..1'''
        if practitioner is None:
            raise ValueError('practitioner is required')
        return practitioner
