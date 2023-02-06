from db.models.template import Template
from services.base_postgres_service import BaseService


class TemplateService(BaseService):
    _model = Template


template_service: TemplateService = TemplateService()


def get_template_service() -> TemplateService:
    """Function for dependency injection"""

    return template_service
