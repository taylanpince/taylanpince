from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

from blog.models import Category, PostType, Post


def landing(request):
    """
    Renders the landing page that aggregates all recent items
    """
    return render_to_response("blog/landing.html", {
        
    }, context_instance=RequestContext(request))


def post_detail(request, slug):
    """
    Renders the blog post detail page
    """
    post = get_object_or_404(Post.objects, slug=slug)
    
    return render_to_response("blog/post_detail.html", {
        "post": post,
    }, context_instance=RequestContext(request))


def category_detail(request, slug):
    """
    Renders the blog category detail page
    """
    category = get_object_or_404(Category, slug=slug)
    
    return render_to_response("blog/category_detail.html", {
        "category": category,
    }, context_instance=RequestContext(request))
