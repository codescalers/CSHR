from cshr.models.official_documents import OffcialDocument
from cshr.models.requests import STATUS_CHOICES


def filter_all_official_docs_by_pending_status():
    """Method helper to filter all official documents by pending status"""
    return OffcialDocument.objects.filter(status=STATUS_CHOICES.PENDING)


def get_official_document_by_id(id: int) -> OffcialDocument:
    """Method helper to get an official document object by its id"""
    try:
        return OffcialDocument.objects.get(id=id)
    except OffcialDocument.DoesNotExist:
        return None
