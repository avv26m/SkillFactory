from datetime import datetime
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect

from .models import Post, Subscription, Category
from .filters import PostFilter
from .forms import PostForm



class PostsList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 3


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context

class PostsSearch(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'post_search.html'
    context_object_name = 'news'
    paginate_by = 3

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

class PostCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('newapp.add_post',)
   # raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_create.html'
    context_object_name = 'create'
    # success_url = reverse_lazy('posts')

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/articles/create/':
            post.categoryType = 'AR'
        elif self.request.path == '/news/create/':
            post.categoryType = 'NW'
        return super().form_valid(form)

class PostDelete(DeleteView):
    permission_required = ('newapp.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    context_object_name = 'delete'
    success_url = reverse_lazy('posts')

class PostUpdate(UpdateView):
    permission_required = ('newapp.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    context_object_name = 'post'
    success_url = reverse_lazy('posts')

@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )