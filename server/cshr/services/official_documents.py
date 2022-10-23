from server.cshr.models.official_documents import OffcialDocument
from server.cshr.models.requests import STATUS_CHOICES

def filter_all_official_docs_by_pinding_status():
    return OffcialDocument.objects.filter(status=STATUS_CHOICES.PENDING)
