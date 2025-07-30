from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, View
from .models import Post
from .forms import CommentForm

# Create your views here.

# enabling class based views
class StartingPageView(ListView):
    template_name = 'blog/index.html'
    model = Post
    context_object_name = 'posts'
    def get_queryset(self):
        # return Post.objects.all().order_by('-date')[:3]  done by django automatically when model is set
        queryset = super().get_queryset()
        data= queryset.order_by('-date')[:3]
        return data

class AllPostsView(ListView):
    template_name = 'blog/all-posts.html'
    model = Post
    context_object_name = 'all_posts'
    ordering = ['-date']  # orders by date in descending order
    # def get_queryset(self):       no need to override this method as ordering is set
    #     queryset = super().get_queryset()
    #     return queryset.order_by('-date')
    

class SinglePostView(View):
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get('stored_posts')
        if stored_posts is not None:
            is_saved_for_later = str(post_id) in stored_posts            
        else:
            is_saved_for_later = False  # If no stored posts, set to False
        return is_saved_for_later


    def get(self, request, slug):
        post= Post.objects.get(slug=slug)
        context= {
            'post': post,
            'form': CommentForm(),  # Initialize the form to be used in the template
            'comments': post.comments.all().order_by('-id'),  # Fetch all comments related to the post            
            'is_saved_for_later': self.is_stored_post(request, post.id),  # Check if the post is saved for later
        }
        return render(request, 'blog/post-detail.html', context)
    
    def post(self, request, slug):
        post= Post.objects.get(slug=slug)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            form = comment_form.save(commit=False)  # Create a Comment instance without saving to the database
            form.post = post  # Set the post field to the current post            
            comment_form.save()  # Save the comment
            return HttpResponseRedirect(reverse('post-detail-page', args=[slug]))  # Redirect to the same post detail page
        
        context= {
            'post': post,
            'form': comment_form,
            'comments': post.comments.all().order_by('-id'),  # Fetch all comments related to the post
            'is_saved_for_later': self.is_stored_post(request, post.id),  # Check if the post is saved for later
        }
        return render(request, 'blog/post-detail.html', context)
    
class ReadLaterView(View):
    def get(self, request):
        stored_posts= request.session.get('stored_posts')
        print("\n\nStored posts:", stored_posts)  # Debugging line to check stored posts

        context = {}
        if stored_posts is None or len(stored_posts) == 0:
            context['posts'] =[]
            context['has_posts'] = False
        else:
            posts= Post.objects.filter(id__in=stored_posts)
            context['has_posts'] = True
            context['posts'] = posts
     
        return render(request, 'blog/stored-posts.html', context)


    def post(self, request):
        post_id= request.POST.get('post_id')
        stored_posts = request.session.get('stored_posts')

        if stored_posts is None:
            stored_posts = []
        
        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)  # Remove the post if it already exists
        request.session['stored_posts'] = stored_posts  # Update the session with the modified list
        
        return HttpResponseRedirect('/blog')



'''
def get_date(post):
    return post['date']

def starting_page(request):    
    # sorted_posts= sorted(all_posts, key=get_date)
    # latest_posts= sorted_posts[-3:]

    latest_posts= Post.objects.all().order_by('-date')[:3]
    return render (request, 'blog/index.html', {
        'posts': latest_posts
    })

def posts(request):
    all_posts= Post.objects.all()
    return render(request, 'blog/all-posts.html', {
        'all_posts': all_posts
    })

def post_detail(request, slug):    
    # identified_post = next(post for post in all_posts if post['slug'] == slug)

    identified_post= Post.objects.get(slug= slug)
    return render(request, 'blog/post-detail.html', {
        'post': identified_post 
    })

# class PostDetailView(DetailView, FormView):
#     template_name = 'blog/post-detail.html'    
#     model = Post  
#     form_class = CommentForm  
#     success_url = '/blog/posts'  # redirect to the same page after form submission
    
    # def get_context_data(self, **kwargs):
    #     context= super().get_context_data(**kwargs)
        # slug= self.kwargs.get('slug')
        # context['post'] = Post.objects.get(slug=slug)     # no need of slug DetailView does it automatically
    #     return context


'''