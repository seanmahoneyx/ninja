from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Design, DesignAttachment
from django.views.decorators.http import require_http_methods

from designs.forms import DesignForm

@login_required
def index(request):
    designs = Design.objects.all().order_by('-design_num')
    context = {'designs': designs,
               'form': DesignForm()
               }
    return render(request, 'designs.html', context)


@login_required
def search_designs(request):
    # for testing spinner and opacity changes on searches
    # import time
    # time.sleep(1)
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

@login_required
@require_http_methods(['POST'])
def create_design(request):
    form = DesignForm(request.POST)
    if form.is_valid():
        design = form.save(commit=False)
        design.requesting_rep = request.user
        design.save()

        for f in request.FILES.getlist('attachments'):
            DesignAttachment.objects.create(design=design, file=f)

        context = {'design': design}
        response = render(request, 'partials/design-row.html', context)
        response['HX-Trigger'] = 'design-success'
        return response
    
    return render(request, 'partials/design-form.html', {'form': form})