from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from random import sample
from .models import Figure, Album, UserFigure, FigurePackage
from .forms import (FigureForm, AlbumVisibilityForm, FigureSaleForm, 
                   FigureTransferForm, FigurePackageForm)
from events.models import Event

@login_required
def create_figure(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.creator != request.user:
        return redirect('event_detail', event.id)
    
    if request.method == 'POST':
        form = FigureForm(request.POST, request.FILES)
        if form.is_valid():
            figure = form.save(commit=False)
            figure.event = event
            figure.save()
            return redirect('event_detail', event.id)
    else:
        form = FigureForm(initial={'event': event})
    
    return render(request, 'figures/create_figure.html', {
        'form': form,
        'event': event,
    })

@login_required
def album_detail(request, album_id):
    album = get_object_or_404(Album, id=album_id)
    if album.owner != request.user and not album.is_public:
        return redirect('home')
    
    figures = album.figures.select_related('figure')
    
    # Count figures by rarity for stats
    rarity_stats = figures.values('figure__rarity').annotate(count=Count('figure__rarity'))
    
    if request.method == 'POST' and album.owner == request.user:
        form = AlbumVisibilityForm(request.POST, instance=album)
        if form.is_valid():
            form.save()
            return redirect('album_detail', album.id)
    else:
        form = AlbumVisibilityForm(instance=album)
    
    return render(request, 'figures/album_detail.html', {
        'album': album,
        'figures': figures,
        'form': form,
        'rarity_stats': rarity_stats,
    })

@login_required
def buy_package(request, package_id):
    package = get_object_or_404(FigurePackage, id=package_id)
    event = package.event
    
    # Check if user has an album for this event
    album = Album.objects.filter(event=event, owner=request.user).first()
    if not album:
        return redirect('event_detail', event.id)
    
    # In a real app, process payment here
    # For now, just generate the figures
    
    # Get all figures for this event
    all_figures = Figure.objects.filter(event=event)
    
    # For simplicity, we'll just randomly select 10 figures
    # In a real app, you'd implement proper rarity distribution
    selected_figures = sample(list(all_figures), min(10, all_figures.count()))
    
    # Create UserFigure instances
    for figure in selected_figures:
        UserFigure.objects.create(
            figure=figure,
            owner=request.user,
            album=album
        )
    
    return redirect('album_detail', album.id)

@login_required
def set_figure_for_sale(request, user_figure_id):
    user_figure = get_object_or_404(UserFigure, id=user_figure_id, owner=request.user)
    
    if request.method == 'POST':
        form = FigureSaleForm(request.POST, instance=user_figure)
        if form.is_valid():
            form.save()
            return redirect('album_detail', user_figure.album.id)
    else:
        form = FigureSaleForm(instance=user_figure)
    
    return render(request, 'figures/set_figure_for_sale.html', {
        'form': form,
        'user_figure': user_figure,
    })

@login_required
def transfer_figure(request, user_figure_id):
    user_figure = get_object_or_404(UserFigure, id=user_figure_id, owner=request.user)
    
    if request.method == 'POST':
        form = FigureTransferForm(request.POST)
        if form.is_valid():
            new_owner = form.cleaned_data['username']
            
            # Check if new owner has an album for this event
            album = Album.objects.filter(
                event=user_figure.figure.event,
                owner=new_owner
            ).first()
            
            if not album:
                form.add_error('username', 'Recipient does not have an album for this event')
            else:
                user_figure.owner = new_owner
                user_figure.album = album
                user_figure.is_for_sale = False
                user_figure.price = None
                user_figure.save()
                return redirect('album_detail', album.id)
    else:
        form = FigureTransferForm()
    
    return render(request, 'figures/transfer_figure.html', {
        'form': form,
        'user_figure': user_figure,
    })

@login_required
def create_package(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if event.creator != request.user:
        return redirect('event_detail', event.id)
    
    if request.method == 'POST':
        form = FigurePackageForm(request.POST)
        if form.is_valid():
            package = form.save(commit=False)
            package.event = event
            package.save()
            return redirect('event_detail', event.id)
    else:
        form = FigurePackageForm(initial={'event': event})
    
    return render(request, 'figures/create_package.html', {
        'form': form,
        'event': event,
    })

@login_required
def marketplace(request):
    figures_for_sale = UserFigure.objects.filter(is_for_sale=True).select_related('figure', 'owner')
    return render(request, 'figures/marketplace.html', {
        'figures_for_sale': figures_for_sale,
    })

@login_required
def buy_figure(request, user_figure_id):
    user_figure = get_object_or_404(UserFigure, id=user_figure_id, is_for_sale=True)
    
    if user_figure.owner == request.user:
        return redirect('marketplace')
    
    # Check if buyer has an album for this event
    album = Album.objects.filter(
        event=user_figure.figure.event,
        owner=request.user
    ).first()
    
    if not album:
        return redirect('event_detail', user_figure.figure.event.id)
    
    # In a real app, process payment here
    # For now, just transfer ownership
    
    # Update seller's balance (not implemented in this basic version)
    
    user_figure.owner = request.user
    user_figure.album = album
    user_figure.is_for_sale = False
    user_figure.price = None
    user_figure.save()
    
    return redirect('album_detail', album.id)
