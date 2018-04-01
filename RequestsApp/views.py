from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import RequestForm


def get_full_name(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)

        if form.is_valid():
            return HttpResponseRedirect('/thanks/')

    else:
        form = RequestForm()

    return render(request, 'requestForm.html', {'form': form})
