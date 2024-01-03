class OrganizationInfo:
    def __init__(
        self,
        org_id: str,
        telematik_id: str,
        org_type_code: str,
        org_type_display: str,
        name: str,
        alias: str,
        contact_name: str,
        phone: str
    ):
        self.org_id = org_id
        self.telematik_id = telematik_id
        self.org_type_code = org_type_code
        self.org_type_display = org_type_display
        self.name = name
        self.alias = alias
        self.contact_name = contact_name
        self.phone = phone