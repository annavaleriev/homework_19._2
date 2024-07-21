from django.urls import path

from catalog import views
from catalog.apps import CatalogConfig
from catalog.views import category_list

app_name = CatalogConfig.name

urlpatterns = [
    path("", views.ProductListView.as_view(), name="home"),
    path("contacts/", views.ContactsTemplateView.as_view(), name="contacts_list"),
    path("products/<int:pk>/", views.ProductDetailView.as_view(), name="product_info"),
    path("create/", views.ProductCreateView.as_view(), name="create"),  # это CreateView
    path("edit/<int:pk>/", views.ProductUpdateView.as_view(), name="edit"),  # это UpdateView
    path('categories/', category_list, name='category_list')
]
