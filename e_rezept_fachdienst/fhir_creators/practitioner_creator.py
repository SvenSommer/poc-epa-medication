from fhir.resources.practitioner import Practitioner
from fhir.resources.humanname import HumanName
from fhir.resources.codeableconcept import CodeableConcept
from fhir.resources.coding import Coding
from fhir.resources.identifier import Identifier
from fhir.resources.meta import Meta

class PractitionerCreator:
    @staticmethod
    def build_practitioner(id_value: str, telematik_id: str, anr: str, name_text: str, family: str, given: list, prefix: str, qualifications: list) -> Practitioner:
        practitioner = Practitioner(
            id=id_value,
            meta=Meta(
                profile=["https://gematik.de/fhir/directory/StructureDefinition/PractitionerDirectory"],
                tag=[{"system": "https://gematik.de/fhir/directory/CodeSystem/Origin", "code": "ldap"}]
            ),
            identifier=[
                {"system": "https://gematik.de/fhir/sid/telematik-id", "value": telematik_id},
                {"system": "https://fhir.kbv.de/NamingSystem/KBV_NS_Base_ANR", "value": anr}
            ],
            active=True,
            name=[HumanName(
                text=name_text,
                family=family,
                given=given,
                prefix=[prefix]
            )],
            qualification=[
                {"code": CodeableConcept(coding=[Coding(system=q['system'], code=q['code'], display=q.get('display'))])} for q in qualifications
            ]
        )

        return practitioner

    @staticmethod
    def get_example_practitioner() -> Practitioner:
        qualifications = [
            {"system": "https://gematik.de/fhir/directory/CodeSystem/PractitionerProfessionOID", "code": "1.2.276.0.76.4.31"},
            {"system": "urn:oid:1.2.276.0.76.5.514", "code": "010", "display": "FA Allgemeinmedizin"},
            {"system": "urn:oid:1.2.276.0.76.5.514", "code": "523", "display": "FA Innere Medizin und (SP) Gastroenterologie"}
        ]

        return PractitionerCreator.build_practitioner(
            id_value="TIPractitionerExample001",
            telematik_id="1-1.58.00000040",
            anr="123456789",
            name_text="Dr. Max Manfred Mustermann",
            family="Mustermann",
            given=["Max", "Manfred"],
            prefix="Dr.",
            qualifications=qualifications
        )

if __name__ == "__main__":
    import os
    practitioner = PractitionerCreator.get_example_practitioner()

    path = "../resources_created/fsh-generated/resources"
    if not os.path.exists(path):
        os.makedirs(path)
    with open(path + "/practitioner.json", "w") as file:
        file.write(practitioner.json(indent=4))
    print(practitioner.json(indent=4))
