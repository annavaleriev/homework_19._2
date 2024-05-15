from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from catalog.apps import CatalogConfig
from catalog.views import ProductDetailView, ContactsTemplateView

app_name = CatalogConfig.name

urlpatterns = [
    # path("", home, name="home"),
    # path("contacts/", ContactsTemplateView.as_view(), name="contacts_list"),
    # path("products/<int:pk>", ProductDetailView.as_view(), name="product_info"), # Добавление URL с параметром
]