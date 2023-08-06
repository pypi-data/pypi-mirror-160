# -*- coding: utf-8 -*-
"""
Profile: http://hl7.org/fhir/us/bser/StructureDefinition/BSeR-ReferralRecipientPractitionerRole
BSeR Release: STU1
BSeR Version: 1.0.0
FHIR Version: 4.0.1
"""

from fhir.resources.practitionerrole import PractitionerRole
import typing
from fhir.resources import fhirtypes
from pydantic import Field


class BSeR_ReferralRecipientPractitionerRole(PractitionerRole):
    profile_url = "http://hl7.org/fhir/us/bser/StructureDefinition/BSeR-ReferralRecipientPractitionerRole"

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
        None,
        alias="practitioner",
        title="Practitioner that is able to provide the defined services for the organization",
        description="Practitioner that is able to provide the defined services for the organization.",
        element_property=True,
        enum_reference_types=["BSeR_Practitioner"],
    )

    organization: fhirtypes.ReferenceType = Field(
        None,
        alias="organization",
        title="Organization where the roles are available",
        description="The organization where the Practitioner performs the roles associated.",
        element_property=True,
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
