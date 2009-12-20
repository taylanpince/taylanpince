from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic.simple import direct_to_template

from portfolio.models import Category, Piece


def landing(request):
    """
    Renders the landing page for all portfolio items
    """
    categories = Category.objects.order_by("pk")
    pieces = Piece.objects.all()
    active_category = None
    
    if request.GET.get("category", None):
        try:
            active_category = Category.objects.get(slug=request.GET.get("category"))
        except Category.DoesNotExist:
            pass
    
    if active_category:
        pieces = pieces.filter(categories=active_category)
    
    return direct_to_template(request, "home.html", extra_context={
        "categories": categories,
        "active_category": active_category,
        "pieces": pieces
    })


def detail(request, slug):
    """
    Renders the portfolio piece detail page
    """
    piece = get_object_or_404(Piece.objects, slug=slug)
    
    return direct_to_template(request, "portfolio/detail.html", {
        "piece": piece,
    })
