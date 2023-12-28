from uuid import uuid4
from fhir.resources.organization import Organization
from fhir.resources.coding import Coding
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.identifier import Identifier
from fhir.resources.meta import Meta
from fhir.resources.contactpoint import ContactPoint
from fhir.resources.humanname import HumanName

class OrganizationCreator:
    @staticmethod
    def create_organization(
        org_id: str,
        telematik_id: str,
        org_type_code: str,
        org_type_display: str,
        name: str,
        alias: str,
        contact_name: str,
        phone: str,
    ) -> Organization:
        organization = Organization(
            id=org_id,
            meta=Meta(
                profile=[
                    "https://gematik.de/fhir/directory/StructureDefinition/OrganizationDirectory"
                ],
                tag=[{
                    "system": "https://gematik.de/fhir/directory/CodeSystem/Origin",
                    "code": "ldap"
                }]
            ),
            identifier=[
                Identifier(
                    system="https://gematik.de/fhir/sid/telematik-id",
                    value=telematik_id,
                )
            ],
            active=True,
            type=[CodeableConcept(  # Geändert zu einer Liste
                coding=[
                    Coding(
                        system="https://gematik.de/fhir/directory/CodeSystem/OrganizationProfessionOID",
                        code=org_type_code,
                        display=org_type_display
                    ),
                ]
            )],
            name=name,
            alias=[alias],
            contact=[
                {
                    "purpose": CodeableConcept(
                        coding=[
                            Coding(
                                system="http://terminology.hl7.org/CodeSystem/contactentity-type",
                                code="PATINF",
                                display="Patient"
                            )
                        ]
                    ),
                    "name": HumanName(text=contact_name),
                    "telecom": [
                        ContactPoint(system="phone", value=phone)
                    ]
                }
            ]
        )

        return organization

    @staticmethod
    def get_example_dentist():
        return OrganizationCreator.create_organization(
            org_id="OrganizationExample",
            telematik_id="2-2.58.00000040",
            org_type_code="1.2.276.0.76.4.51",
            org_type_display="Zahnarztpraxis",
            name="Zahnarztpraxis Dr. Mustermann",
            alias="Zahnarztpraxis am Bahnhof",
            contact_name="Empfang Zahnarztpraxis Dr. Mustermann",
            phone="030 1234567",
        )
    @staticmethod
    def get_example_farmacy_organization():
        return OrganizationCreator.create_organization(
            org_id="OrganizationExample",
            telematik_id="2-2.58.00000040",
            org_type_code="1.2.276.1.78.6.87",
            org_type_display="Apotheke",
            name="Apotheke am Bahnhof",
            alias="Apotheke am Bahnhof",
            contact_name="Empfang Apotheke am Bahnhof",
            phone="030 1234567",
        )
    
if __name__ == "__main__":
    import os
    organization = OrganizationCreator.get_example_dentist()

    path = "../resources_created/fsh-generated/resources"
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + "/organization_dentist.json", "w") as file:
        file.write(organization.json(indent=4))

    print(organization.json(indent=4))
