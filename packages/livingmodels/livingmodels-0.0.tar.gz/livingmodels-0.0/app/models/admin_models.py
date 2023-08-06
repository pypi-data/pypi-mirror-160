
from sqladmin import ModelAdmin

from app.database import _get_engine
from app.models.services_guide_models import ServicesGuide, Services
from app.settings import db_settings


class ServicesGuideAdmin(ModelAdmin, model=ServicesGuide, async_engine=_get_engine(db_settings)):
    name = "Справочник"
    column_list = [ServicesGuide.id, ServicesGuide.name, ServicesGuide.description]
    column_searchable_list = [ServicesGuide.name]
    column_sortable_list = [ServicesGuide.name]


class ServicesAdmin(ModelAdmin, model=Services, async_engine=_get_engine(db_settings)):
    name = "Услуги"
    column_list = [Services.id, Services.name, Services.description]
    column_searchable_list = [Services.name]
    column_sortable_list = [Services.name]
