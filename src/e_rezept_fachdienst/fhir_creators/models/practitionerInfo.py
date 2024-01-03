class PractitionerInfo:
    def __init__(
        self,
        id_value: str,
        telematik_id: str,
        anr: str,
        name_text: str,
        family: str,
        given: list,
        prefix: str,
        qualifications: list
    ):
        self.id_value = id_value
        self.telematik_id = telematik_id
        self.anr = anr
        self.name_text = name_text
        self.family = family
        self.given = given
        self.prefix = prefix
        self.qualifications = qualifications