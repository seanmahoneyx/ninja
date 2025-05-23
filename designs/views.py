from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Design

@login_required
def index(request):
    designs = Design.objects.all().order_by('-design_num')
    context = {'designs': designs}
    return render(request, 'designs.html', context)


@login_required
def search_designs(request):
    query = request.GET.get('search', '')

    designs = Design.objects.filter(
        Q(design_num__icontains=query) | Q(customer__cust_name__icontains=query) |
        Q(requesting_rep__username__icontains=query) | Q(designer__username__icontains=query) | 
        Q(ident__icontains=query) | Q(status__icontains=query)
    )
    return render(
        request,
        'partials/design-list.html',
        {'designs': designs}
    )