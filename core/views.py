from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomProfileForm
from scaduti.models import Scaduto
from inediti.models import Inedito
from django.db.models import Q
from django.contrib.auth.models import User
from .models import UserProfile
from django.http import HttpResponseForbidden, HttpResponseNotFound

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
            scaduti_qs = Scaduto.objects.filter(
                Q(titolo__icontains=query) |
                Q(trama__icontains=query) |
                Q(autore__username__icontains=query)
            )
            if anno:
                scaduti_qs = scaduti_qs.filter(anno_pubblicazione=anno)
            if editore:
                scaduti_qs = scaduti_qs.filter(editore__icontains=editore)
            if genere:
                scaduti_qs = scaduti_qs.filter(genere__icontains=genere)
            for s in scaduti_qs:
                s.book_type = 'scaduto'
            results = list(scaduti_qs)
        else:  # inediti
            inediti_qs = Inedito.objects.filter(
                Q(titolo__icontains=query) |
                Q(trama__icontains=query) |
                Q(autore__username__icontains=query)
            )
            if genere:
                inediti_qs = inediti_qs.filter(genere__icontains=genere)
            for i in inediti_qs:
                i.book_type = 'inedito'
            results = list(inediti_qs)

    return render(request, 'core/index.html', {
        'results': results,
        'search_type': search_type,
        'query': query,
        'genere': genere,
        'anno': anno,
        'editore': editore,
        'genre_choices': GENRE_CHOICES,
    })

def privacy_policy(request):
    return render(request, 'core/privacy_policy.html')

def get_singular_type(search_type):
    mapping = {
        'scaduti': 'scaduto',
        'inediti': 'inedito'
    }
    return mapping.get(search_type, search_type)

def scheda_libro(request, type, pk):
    if type in ['inedito', 'inediti']:
        book = get_object_or_404(Inedito, id=pk)
    elif type in ['scaduto', 'scaduti']:
        book = get_object_or_404(Scaduto, id=pk)
    else:
        return HttpResponseNotFound('Tipo non valido')
    return render(request, 'core/scheda_libro.html', {'book': book, 'type': type})

def scheda_autore(request, pk):
    author = get_object_or_404(User, pk=pk)
    return render(request, 'core/scheda_autore.html', {'author': author})

@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    
    # Handle Profile Edit
    if request.method == 'POST' and 'edit_profile' in request.POST:
        form = CustomProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profilo')
    else:
        form = CustomProfileForm(instance=profile)
    
    # Handle Account Deletion
    if request.method == 'POST' and 'delete_account' in request.POST:
        request.user.delete()
        return redirect('index')
    
    return render(request, 'core/profilo.html', {  
        'form': form,
        'profile': profile,
})


def sign_in(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            gender = form.cleaned_data['gender']
            already_published = form.cleaned_data['already_published']
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.gender = gender
            profile.already_published = already_published
            profile.save()

            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/sign_in.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profilo')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'core/user_login.html')

def user_logout(request):
    logout(request)
    return redirect('index')

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
    return render(request, 'core/index.html', {
        'results': results,
        'search_type': search_type,
        'query': query,
    })

@login_required
def delete_book(request, type, pk):
    if type == 'inedito':
        book = get_object_or_404(Inedito, id=pk)
    elif type == 'scaduto':
        book = get_object_or_404(Scaduto, id=pk)
    else:
        return HttpResponseNotFound('Tipo non valido')
    if book.autore != request.user:
        return HttpResponseForbidden('Non puoi eliminare questo libro.')
    if request.method == 'POST':
        book.delete()
        messages.success(request, f'Libro "{book.titolo}" eliminato con successo.')
        return redirect('profilo')
    return render(request, 'core/confirm_delete.html', {'book': book, 'type': type})

