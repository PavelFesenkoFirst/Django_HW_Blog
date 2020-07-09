from django.db.models import Count, Sum
from django.db.models import F
from django.shortcuts import render, get_object_or_404
from .models import Comments, Authors, Posts, Rubrics

from django.db.models import Count


# Create your views here.
def index(request):
    context = {}
    rubric_qs = Posts.objects.filter(show_rubric=True).order_by('-date_publication')[:6]
    context['rubric_list'] = rubric_qs
    return render(request, 'contents/index.html', context)


def rubric_list(request):
    context = {}
    # добавляем поиск
    oder = request.GET.get('order', '-rubric_name')
    search = request.GET.get('search', '')
    s_rubrics = Rubrics.objects.filter(
        rubric_name__contains=search
    ).order_by(oder)
    context['rubric_list'] = s_rubrics
    return render(request, 'contents/rubric_list.html', context)


def rubric_detail(request, slug):
    context = {}
    rubrics = get_object_or_404(Rubrics, slug=slug)
    posts_qs = Posts.objects.filter(show_rubric=True)
    com = Comments.objects.all()
    post_qq = Posts.objects.all()
    context['rubric'] = rubrics
    context['post_in'] = posts_qs
    context['posts'] = post_qq
    context['com'] = com
    return render(request, 'contents/rubric.html', context)


def post_list(request):
    context = {}
    posts_qs = Posts.objects.filter(show_rubric=True)
    context['posts_list'] = posts_qs
    return render(request, 'contents/post_list.html', context)


#
def post_detail(request, pk, slug_category):
    context = {}
    post = Posts.objects.filter(
        pk=pk, rubrics_id__slug=slug_category
    ).first()
    coment_qs = Comments.objects.filter(post_id=pk)
    author_qs = Authors.objects.filter(pk=pk)
    post.view_rubric += 1
    post.save()
    count_view = Posts.objects.get(pk=pk)
    context['cometns'] = coment_qs
    context['posts'] = post
    context['count_view'] = count_view
    context['author_qs'] = author_qs
    return render(request, 'contents/post.html', context)


def author_list(request):
    context = {}
    author = Authors.objects.all()
    context['author_list'] = author
    return render(request, 'contents/author_list.html', context)


def author_detail(request, pk):
    context = {}
    author_qs = Authors.objects.filter(pk=pk)
    count_post = Posts.objects.filter(author_id=pk).aggregate(Count('pk'))['pk__count']
    count_comment = Comments.objects.filter(author=pk).aggregate(Count('pk'))['pk__count']
    last_pub = Posts.objects.filter(author_id=pk).order_by('-date_publication')[0]
    post_qq = Posts.objects.filter(author_id=pk).aggregate(Sum('view_rubric'))['view_rubric__sum']
    context['comment_author'] = count_comment
    context['author_info'] = author_qs
    context['post_author'] = count_post
    context['total_post'] = post_qq
    context['last'] = last_pub
    return render(request, 'contents/author.html', context)
