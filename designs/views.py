from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    designs = request.user.rep_requests.all().order_by('design_num')
    context = {'designs': designs}
    return render(request, 'designs.html', context)