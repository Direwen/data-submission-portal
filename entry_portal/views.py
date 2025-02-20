from django.views.generic import ListView, DeleteView, UpdateView
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.db.models import Count
from django.core.paginator import Paginator
from .models import DataEntry
from .forms import DataEntryForm

class DataEntryListView(ListView):
    model = DataEntry
    template_name = 'index.html'
    context_object_name = 'entries'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by('-created_at')
        category = self.request.GET.get('category', '')
        search = self.request.GET.get('search', '')
        if category:
            queryset = queryset.filter(category=category)
        if search:
            queryset = queryset.filter(content__icontains=search)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = DataEntry.CATEGORY_CHOICES
        context['selected_category'] = self.request.GET.get('category', '')
        context['search_input'] = self.request.GET.get('search', '')
        context['form'] = DataEntryForm()
        context['total_entries_by_category'] = DataEntry.objects.values('category').annotate(total=Count('category'))
        print(context)
        return context
    
    def render_to_response(self, context, **response_kwargs):
        if self.request.htmx:
            return render(self.request, 'partials/entries_list.html', context)
        return super().render_to_response(context, **response_kwargs)

class DataEntryDeleteView(DeleteView):
    model = DataEntry
    template_name = 'confirm_delete.html'
    success_url = reverse_lazy('data-entry-list')

class DataEntryUpdateView(UpdateView):
    model = DataEntry
    form_class = DataEntryForm
    template_name = 'edit_entry.html'
    success_url = reverse_lazy('data-entry-list')
    
def create_data_entry(request):
    if request.method == "POST":
        form = DataEntryForm(request.POST)
        if form.is_valid():
            form.save()
            entries = DataEntry.objects.all().order_by('-created_at')
            paginator = Paginator(entries, 10)
            page_number = request.POST.get('page', 1)  # Get from hx-vals
            page_obj = paginator.get_page(page_number)
            total_entries_by_category = DataEntry.objects.values('category').annotate(total=Count('category'))
            return render(request, 'partials/entries_list.html', {
                'entries': page_obj,
                'page_obj': page_obj,
                'paginator': paginator,
                'is_paginated': paginator.num_pages > 1,
                'total_entries_by_category': total_entries_by_category,
                'include_counts': True,
            })
        return HttpResponse("Form is invalid", status=400)
    return HttpResponse(status=204)

def toggle_review(request, pk):
    if request.method == "POST":
        entry = DataEntry.objects.get(pk=pk)
        entry.is_reviewed = not entry.is_reviewed
        entry.save()
        queryset = DataEntry.objects.all().order_by('-created_at')
        paginator = Paginator(queryset, 10)
        page_number = request.POST.get('page', 1)
        page_obj = paginator.get_page(page_number)
        return render(request, 'partials/entries_list.html', {
            'entries': page_obj,
            'page_obj': page_obj,
            'paginator': paginator,
            'is_paginated': paginator.num_pages > 1,
            'include_counts': False,
        })
    return HttpResponse(status=204)
    