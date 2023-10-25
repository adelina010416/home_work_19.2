from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from pytils.translit import slugify

from blog.models import Post


# Create
class PostCreateView(CreateView):
    model = Post
    fields = ('title', 'content', 'image',)
    success_url = reverse_lazy('blog:posts')

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.title)
            new_post.save()
        return super().form_valid(form)


# Read
class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.view_count += 1
        self.object.save()
        return self.object


class PostListView(ListView):
    model = Post

    def get_query_set(self, *args, **kwargs):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset


# Update
class PostUpdateView(UpdateView):
    model = Post
    fields = ('title', 'content', 'image',)

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.title)
            new_post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post', args=[self.kwargs.get('pk')])


# Delete
class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:posts')
