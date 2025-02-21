from django.views.generic import ListView, DeleteView, UpdateView
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.db.models import Count
from django.core.paginator import Paginator
from .models import DataEntry
from .forms import DataEntryForm

class DataEntryListView(ListView):
    
    ''' Display a paginated list with search and filter options '''
    
    model = DataEntry
    template_name = 'index.html' #Main full template
    context_object_name = 'entries' #Renaming the context object for readability
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')
        # Modifying queryset with search and filter options
        category = self.request.GET.get('category', '')
        search = self.request.GET.get('search', '')
        if category:
            queryset = queryset.filter(category=category)
        if search:
            queryset = queryset.filter(content__icontains=search)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # For Filter selector to show available category options
        context['categories'] = DataEntry.CATEGORY_CHOICES
        # To track current searched input and selected category
        context['selected_category'] = self.request.GET.get('category', '')
        context['search_input'] = self.request.GET.get('search', '')
        # For the DataEntry Create Form
        context['form'] = DataEntryForm()
        # For Reports
        context['total_entries_by_category'] = DataEntry.objects.values('category').annotate(total=Count('category'))
        return context
    
    def render_to_response(self, context, **response_kwargs):
        # If the request is an htmx request, return a partial template using including the same context
        if self.request.htmx:
            return render(self.request, 'partials/entries_list.html', context)
        return super().render_to_response(context, **response_kwargs)

class DataEntryDeleteView(DeleteView):
    
    ''' Redirecting to the delete confirm page and then to the list view if successful '''
    
    model = DataEntry
    template_name = 'confirm_delete.html'
    # Ensures data-entry-list route is resolved only after successful deletion
    success_url = reverse_lazy('data-entry-list')

class DataEntryUpdateView(UpdateView):
    
    ''' Redirecting to the edit page and then to the list view if successful '''
    
    model = DataEntry
    form_class = DataEntryForm
    template_name = 'edit_entry.html'
    # Ensures data-entry-list route is resolved only after successful deletion
    success_url = reverse_lazy('data-entry-list')
    
def create_data_entry(request) -> HttpResponse:
    
    ''' Create a new entry and perform a partial rendering of the entries list '''
    
    if request.method == "POST":
        form = DataEntryForm(request.POST)
        # Validate the form and save the entry
        if form.is_valid():
            try:
                form.save()
            except Exception as err:
                return HttpResponse(f"An error occurred: {err}", status=500)
            # Get the latest entries and paginate them
            queryset = DataEntry.objects.all().order_by('-created_at')
            # Paginate the queryset
            page_obj = paginate_queryset(request, queryset)
            # Get the total entries by category for the report
            total_entries_by_category = DataEntry.objects.values('category').annotate(total=Count('category'))
            # Preparing the context
            context = {
                'entries': page_obj,
                'page_obj': page_obj,
                'paginator': page_obj.paginator,
                'is_paginated': page_obj.paginator.num_pages > 1,
                'total_entries_by_category': total_entries_by_category,
                'include_counts': True,
            }
            return render(request, 'partials/entries_list.html', context)
        return HttpResponse("Form is invalid", status=400)
    return HttpResponse(status=204)

def toggle_review(request, pk) -> HttpResponse:
    
    ''' Toggle the review status of an entry and perform a partial rendering of the entries list '''
    
    if request.method == "POST":
        entry = get_object_or_404(DataEntry, pk=pk)
        entry.is_reviewed = not entry.is_reviewed
        entry.save()
        # Get the latest entries along with Search and Filter options
        queryset = DataEntry.objects.all().order_by('-created_at')
        category = request.POST.get('category', '')
        search = request.POST.get('search', '')
        if category:
            queryset = queryset.filter(category=category)
        if search:
            queryset = queryset.filter(content__icontains=search)
        # Paginate the queryset
        page_obj = paginate_queryset(request, queryset)
        return render(request, 'partials/entries_list.html', {
            'entries': page_obj,
            'selected_category' : category,
            'search_input' : search,
            'page_obj': page_obj,
            'paginator': page_obj.paginator,
            'is_paginated': page_obj.paginator.num_pages > 1,
            'include_counts': False,
        })
    return HttpResponse(status=204)

def paginate_queryset(request, queryset, per_page=10) -> Paginator:
    
    ''' Paginate the queryset and return the page object '''
    
    paginator = Paginator(queryset, per_page)
    page_number = request.POST.get('page', 1)
    return paginator.get_page(page_number)