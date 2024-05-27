from datetime import datetime

from django.http import HttpResponse
from django.views import View
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

from .tasks import send_email_task, weekly_send_email_task
from django.utils.translation import gettext as _ # импортируем функцию для перевода
from django.utils import timezone
from django.shortcuts import redirect
import pytz #  импортируем стандартный модуль для работы с часовыми поясами



class PostsList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect(self.request.path)

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
            post.save()
            send_email_task.delay(post.pk)
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


# Create your views here.

# class Index(View):
#     def get(self, request):
#         models = Post.objects.all()
#         context = {
#             'models': models,
#             'current_time': timezone.localtime(timezone.now()),
#             'timezones': pytz.common_timezones
#         }
#         return HttpResponse(render(request, 'news.html', context))
#
#         #  по пост-запросу будем добавлять в сессию часовой пояс, который и будет обрабатываться написанным нами ранее middleware
#     def post(self, request):
#         request.session['django_timezone'] = request.POST['timezone']
#         return redirect('/')