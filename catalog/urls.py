from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import home, contacts, product_info

app_name = CatalogConfig.name

urlpatterns = [
    path("", home, name="home"),
    path("contacts/", contacts, name="contacts_list"),
    path("products/<int:pk>", product_info, name="product_info"), # Добавление URL с параметром
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
