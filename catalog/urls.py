from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('authors/', views.AuthorDetails.as_view(), name='authors'),
    path('book/<int:primary_key>', views.book_detail_view, name='book-detail')
]

urlpatterns += [
    path('book/<uuid:pk>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
]