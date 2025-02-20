from django.urls import path
from .views import DataEntryListView, DataEntryDeleteView, DataEntryUpdateView, create_data_entry, toggle_review

urlpatterns = [
    path('', DataEntryListView.as_view(), name='data-entry-list'),
    path('create/', create_data_entry, name='create-entry'),
    path('toggle-review/<int:pk>', toggle_review, name='toggle-review'),
    path('delete/<int:pk>/', DataEntryDeleteView.as_view(), name='delete-entry'),
    path('edit/<int:pk>/', DataEntryUpdateView.as_view(), name='edit-entry'),
]