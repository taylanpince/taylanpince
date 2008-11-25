from django.utils import simplejson
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST
from django.shortcuts import render_to_response, get_object_or_404

from core.utils.encoders import LazyEncoder, convert_object_to_json

from blog.forms import CommentForm
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
        "form": CommentForm(auto_id="%s", prefix="CommentForm")
    }, context_instance=RequestContext(request))


def category_detail(request, slug):
    """
    Renders the blog category detail page
    """
    category = get_object_or_404(Category, slug=slug)
    
    return render_to_response("blog/category_detail.html", {
        "category": category,
    }, context_instance=RequestContext(request))


@require_POST
def submit_comment(request, slug):
    """
    Process the comment form
    """
    post = get_object_or_404(Post.objects, slug=slug)
    form = CommentForm(request.POST, auto_id="%s", prefix="CommentForm")
    
    if form.is_valid():
        comment = form.save(commit=False)
        
        comment.ip_address = request.META.get("REMOTE_ADDR", None)
        comment.post = post
        
        comment.save()
        
        if comment.published:
            request.notifications.create(_("Your comment has been posted!"), "success")
        else:
            request.notifications.create(_("Your comment was posted, but it won't be published until approved."), "warning")
        
        if not request.is_ajax():
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        request.notifications.create(_("There were some errors with your comment submission."), "error")
        
        comment = None
    
    if request.is_ajax():
        template = "blog/comment.json"
        mimetype = "application/json"
        
        if form.errors:
            errors = simplejson.dumps(form.errors, cls=LazyEncoder, ensure_ascii=False)
        else:
            errors = None
        
        comment = convert_object_to_json(comment, fields=["url", "body_html", "author", "email", "creation_date", "published"])
    else:
        template = "blog/comment.html"
        mimetype = "text/html; charset=utf-8"
        errors = form.errors
    
    return render_to_response(template, {
        "errors": errors,
        "comment": comment,
        "post": post,
        "form": form,
    }, context_instance=RequestContext(request), mimetype=mimetype)
