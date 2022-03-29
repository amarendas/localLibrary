from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render,get_object_or_404 
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.decorators import login_required
import datetime
from django.urls import reverse

from catalog.forms import RenewBookForm

# Create your views here.
@login_required 
def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default. 
    num_authors = Author.objects.count()
    
    # The total no of genre
    num_genre=Genre.objects.all().count()    
    num_visits=request.session.get('num_visits_cookie',0)
    request.session['num_visits_cookie']=num_visits+1
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_genre': num_genre,
        'num_visits':num_visits,
    }
        # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
class BookListView(LoginRequiredMixin,generic.ListView):
    model = Book
    # The querry is automaticllly made and the result stored in 
    # book_list or object_list
    # views.BookListView.as_view() is used to render the page in the url.py
    # It is rendered using template located at /locallibrary/catalog/templates/catalog/book_list.html 
    # Context is transfered as variable "book_list" for use in html.
class AuthorDetails(LoginRequiredMixin,generic.ListView):
    model=Author #this  call querries the data_set and renders the page /templates/catalog/author_list.html
    # querry list is strored in author_list
    # context variable is "author_list"
    

    
def book_detail_view(request, primary_key):
    try:
        book = Book.objects.get(pk=primary_key)
    except Book.DoesNotExist:
        raise Http404('Book does not exist')

    return render(request, 'catalog/book_detail.html', context={'book': book})

def renew_book_librarian(request,pk):
    book_instance = get_object_or_404(BookInstance, pk=pk) # Data is retrived from the model/Database table :"Bookinstance"
    
    # Now checheck if the form use post or getmethod
    if request.method=='POST':
        form = RenewBookForm(request.POST) # create a form object with data from the rewuest
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed') )
        else:
                proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)