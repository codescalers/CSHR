from server.cshr.models.company_properties import CompanyProperties


def get_company_properties_by_id(id: str) -> CompanyProperties:
    """Return company properties who have the same id"""
    try:
        return CompanyProperties.objects.get(id=int(id))
    except CompanyProperties.DoesNotExist:
        return None


def get_all_comopany_properties() -> CompanyProperties:
    """Return all company properties"""
    return CompanyProperties.objects.all()
