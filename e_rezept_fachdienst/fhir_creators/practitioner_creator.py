from fhir.resources.practitioner import Practitioner
from fhir.resources.humanname import HumanName
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.meta import Meta

from e_rezept_fachdienst.fhir_creators.models.practitionerInfo import PractitionerInfo

class PractitionerCreator:
    @staticmethod
    def build_practitioner(practitioner_info: PractitionerInfo) -> Practitioner:
        practitioner = Practitioner(
            id=practitioner_info.id_value,
            meta=Meta(
                profile=["https://gematik.de/fhir/directory/StructureDefinition/PractitionerDirectory"],
                tag=[{"system": "https://gematik.de/fhir/directory/CodeSystem/Origin", "code": "ldap"}]
            ),
            identifier=[
                {"system": "https://gematik.de/fhir/sid/telematik-id", "value": practitioner_info.telematik_id},
                {"system": "https://fhir.kbv.de/NamingSystem/KBV_NS_Base_ANR", "value": practitioner_info.anr}
            ],
            active=True,
            name=[HumanName(
                text=practitioner_info.name_text,
                family=practitioner_info.family,
                given=practitioner_info.given,
                prefix=[practitioner_info.prefix]
            )],
            qualification=[
                {"code": CodeableConcept(coding=[Coding(system=q['system'], code=q['code'], display=q.get('display'))])} for q in practitioner_info.qualifications
            ]
        )

        return practitioner

    @staticmethod
    def get_example_practitioner() -> Practitioner:
        practitioner_info = PractitionerInfo(
            id_value="TIPractitionerExample001",
            telematik_id="1-1.58.00000040",
            anr="123456789",
            name_text="Dr. Max Manfred Mustermann",
            family="Mustermann",
            given=["Max", "Manfred"],
            prefix="Dr.",
            qualifications=[
                {"system": "https://gematik.de/fhir/directory/CodeSystem/PractitionerProfessionOID", "code": "1.2.276.0.76.4.31"},
                {"system": "urn:oid:1.2.276.0.76.5.514", "code": "010", "display": "FA Allgemeinmedizin"},
                {"system": "urn:oid:1.2.276.0.76.5.514", "code": "523", "display": "FA Innere Medizin und (SP) Gastroenterologie"}
            ]
        )
        return PractitionerCreator.build_practitioner(practitioner_info)

if __name__ == "__main__":
    import os
    practitioner = PractitionerCreator.get_example_practitioner()
    path = "../resources_created/fsh-generated/resources"
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + "/practitioner.json", "w") as file:
        file.write(practitioner.json(indent=4))
    print(practitioner.json(indent=4))
