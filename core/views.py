from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from scaduti.models import Scaduto
from inediti.models import Inedito
from django.db.models import Q
from django.contrib.auth.models import User


def index_view(request):
    search_type = request.GET.get('search_type', 'inediti')
    query = request.GET.get('query', '')
    genere = request.GET.get('genere', '')
    anno = request.GET.get('anno', '')
    editore = request.GET.get('editore', '')

    results = []

    GENRE_CHOICES = [
        ('fantasy', 'Fantasy'),
        ('thriller', 'Thriller'),
        ('romance', 'Romance'),
    ]

    if query or genere or anno or editore:
        if search_type == 'scaduti':
            results = Scaduto.objects.filter(
                Q(titolo__icontains=query) |
                Q(trama__icontains=query) |
                Q(autore__username__icontains=query)
            )
            if anno:
                results = results.filter(anno_pubblicazione=anno)
            if editore:
                results = results.filter(editore__icontains=editore)
            if genere:
                results = results.filter(genere__icontains=genere)
        else:  # inediti
            results = Inedito.objects.filter(
                Q(titolo__icontains=query) |
                Q(trama__icontains=query) |
                Q(autore__username__icontains=query)
            )
            if genere:
                results = results.filter(genere__icontains=genere)

    return render(request, 'core/index.html', {
        'results': results,
        'search_type': search_type,
        'query': query,
        'genere': genere,
        'anno': anno,
        'editore': editore,
        'genre_choices': GENRE_CHOICES,
    })



def scheda_libro(request, type, pk):
    if type == 'inedito':
        book = get_object_or_404(Inedito, id=pk)
    elif type == 'scaduto':
        book = get_object_or_404(Scaduto, id=pk)
    else:
        return HttpResponseNotFound('Tipo non valido')
    return render(request, 'core/scheda_libro.html', {'book': book})

def scheda_autore(request, pk):
    author = get_object_or_404(User, pk=pk)
    return render(request, 'core/scheda_autore.html', {'author': author})



# User profile
@login_required
def profile_view(request):
    return render(request, 'core/profilo.html')


def sign_in(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Effettua il login automatico
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'core/sign_in.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')  # Reindirizza alla pagina profilo
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'core/user_login.html')


def user_logout(request):
    logout(request)
    return redirect('index')  # Redirect to home page


def search_books(request):
    search_type = request.GET.get('search_type', 'inediti')
    query = request.GET.get('query', '')
    results = []

    if search_type == 'scaduti':
        anno = request.GET.get('anno')
        editore = request.GET.get('editore')
        results = Scaduto.objects.filter(
            Q(trama__icontains=query) |
            Q(autore__username__icontains=query)
        )
        if anno:
            results = results.filter(anno_pubblicazione=anno)
        if editore:
            results = results.filter(editore__icontains=editore)
    elif search_type == 'inediti':
        results = Inedito.objects.filter(
            Q(titolo__icontains=query) |
            Q(autore__username__icontains=query)
        )

    return render(request, 'core/index.html', {  # fixed template path here
        'results': results,
        'search_type': search_type,
        'query': query,
    })
