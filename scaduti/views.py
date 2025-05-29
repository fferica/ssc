from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ScadutoForm

@login_required
def add_scaduto(request):
    if request.method == 'POST':
        form = ScadutoForm(request.POST, request.FILES)
        if form.is_valid():
            inedito = form.save(commit=False)
            inedito.autore = request.user
            inedito.save()
            return redirect('index')
    else:
        form = ScadutoForm()
    return render(request, 'scaduti/add_scaduto.html', {'form': form})

def index_view(request):
    return render(request, 'scaduti/index.html')