# -*- coding: utf-8 -*-
"""
Profile: http://hl7.org/fhir/us/bser/StructureDefinition/BSeR-ArthritisReferralSupportingInformation
BSeR Release: STU1
BSeR Version: 1.0.0
FHIR Version: 4.0.1
"""

from fhir.resources.bundle import Bundle
from fhir.resources import fhirtypes
from pydantic import Field, MissingError, validator


class BSeR_ArthritisReferralSupportingInformation(Bundle):
    profile_url = "http://hl7.org/fhir/us/bser/StructureDefinition/BSeR-ArthritisReferralSupportingInformation"

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

    type: fhirtypes.Code = Field(
        "collection",
        alias="type",
        title=(
            "document | message | transaction | transaction-response | batch | "
            "batch-response | history | searchset | collection"
        ),
        description="Indicates the purpose of this bundle - how it is intended to be used.",
        # if property is element of this resource.
        element_property=True,
        element_required=True,
        # note: Enum values can be used in validation,
        # but use in your own responsibilities, read official FHIR documentation.
        enum_values=["collection"],
    )

    # TODO: Implement entry requirements once clarified.

    @validator('meta')
    def check_meta(cls, meta):
        '''profile url set properly'''
        profile_url = "http://hl7.org/fhir/us/bser/StructureDefinition/BSeR-ArthritisReferralSupportingInformation"
        meta_dict = meta.dict()
        print(meta)
        if meta is None:
            raise MissingError('meta.profile must exist')
        else:
            if meta_dict["profile"] is None:
                raise MissingError('meta.profile must exist')
            elif not isinstance(meta_dict["profile"], list):
                raise TypeError('meta.profile must be list')
            else:
                for profile in meta_dict["profile"]:
                    if not isinstance(profile, str):
                        raise TypeError("profile.meta elements must be str")
                if profile_url not in meta_dict["profile"]:
                    raise ValueError("missing profile url from meta.profile")
        return meta

    @validator('type')
    def check_type(cls, type):
        '''type equals collection'''
        if type is None:
            raise ValueError('type must be collection')
        elif type != "collection":
            raise ValueError('type must be collection')
        return type
