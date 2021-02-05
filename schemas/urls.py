from django.urls import path

from .views import (
    SchemaListView,
    SchemaDetailView,
    SchemaDeleteView,
    SchemaCreateView
)


urlpatterns = [
    path('<int:pk>/', SchemaDetailView.as_view(), name='schema_detail'),
    path('<int:pk>/delete/', SchemaDeleteView.as_view(), name='schema_delete'),
    path('new/', SchemaCreateView.as_view(), name='schema_new'),
    path('', SchemaListView.as_view(), name='schema_list'),
]
