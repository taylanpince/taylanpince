from django.utils import simplejson
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.views.decorators.http import require_POST
from django.views.generic.list_detail import object_list
from django.shortcuts import render_to_response, get_object_or_404

from tagging.views import tagged_object_list
from core.utils.pagination import make_url_pattern
from core.utils.encoders import LazyEncoder, convert_object_to_json

from blog.forms import CommentForm
from blog.models import Category, PostType, Post, Comment


def landing(request):
    """
    Renders the landing page that aggregates all recent items
    """
    return object_list(
        request,
        queryset=Post.objects.all(),
        paginate_by=5,
        page=request.GET.get("page", 1),
        template_name="blog/landing.html",
        allow_empty=True,
        template_object_name="posts",
        extra_context={
            "pager_url": make_url_pattern(reverse("blog_landing"), request.GET),
        }
    )


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
    
    return object_list(
        request,
        queryset=category.posts,
        paginate_by=5,
        page=request.GET.get("page", 1),
        template_name="blog/category_detail.html",
        allow_empty=True,
        template_object_name="posts",
        extra_context={
            "category": category,
            "pager_url": make_url_pattern(category.get_absolute_url(), request.GET),
        }
    )


def tag_detail(request, tag):
    """
    Renders the tag detail page
    """
    return tagged_object_list(
        request,
        Post.objects,
        tag,
        paginate_by=5,
        page=request.GET.get("page", 1),
        allow_empty=True,
        template_name="blog/tag_detail.html",
        template_object_name="posts",
        extra_context={
            "pager_url": make_url_pattern(reverse("blog_tag_detail", kwargs={"tag": tag}), request.GET),
        }
    )


def post_type_styles(request):
    """
    Renders a CSS file with PostType icons
    """
    return render_to_response("blog/post_types.css", {
        "types": PostType.objects.all(),
    }, context_instance=RequestContext(request), mimetype="text/css")


def comment_detail(request, id):
    """
    Renders a single comment
    """
    comment = get_object_or_404(Comment.objects, pk=id)
    
    return render_to_response("blog/comment_detail.html", {
        "comment": comment,
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
        template = "blog/comment_submit.json"
        mimetype = "application/json"
        
        if form.errors:
            errors = simplejson.dumps(form.errors, cls=LazyEncoder, ensure_ascii=False)
        else:
            errors = None
    else:
        template = "blog/comment_submit.html"
        mimetype = "text/html; charset=utf-8"
        errors = form.errors
    
    return render_to_response(template, {
        "errors": errors,
        "comment": comment,
        "post": post,
        "form": form,
    }, context_instance=RequestContext(request), mimetype=mimetype)
