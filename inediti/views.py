from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import IneditoForm

@login_required
def add_inedito(request):
    if request.method == 'POST':
        form = IneditoForm(request.POST, request.FILES)
        if form.is_valid():
            inedito = form.save(commit=False)
            inedito.autore = request.user
            inedito.save()
            return redirect('index')
    else:
        form = IneditoForm()
    return render(request, 'inediti/add_inedito.html', {'form': form})

def index_view(request):
    return render(request, 'inediti/index.html')