from django.urls import path
from catalog.apps import CatalogConfig
from catalog import views

app_name = CatalogConfig.name

urlpatterns = [
    path("", views.ProductListView.as_view(), name="home"),
    path("contacts/", views.ContactsTemplateView.as_view(), name="contacts_list"),
    path("products/<int:pk>/", views.ProductDetailView.as_view(), name="product_info"),
    path("create/", views.ProductCreateView.as_view(), name="create"),  # это CreateView
    path("edit/<int:pk>/", views.ProductUpdateView.as_view(), name="edit"),   # это UpdateView
    path("version/create/", views.VersionCreateView.as_view(), name="create_version"),
    path("version/list/", views.VersionListView.as_view(), name="list_version"),
    path("version/edit/", views.VersionUpdateView.as_view(), name="update_version")   # это UpdateView#
]