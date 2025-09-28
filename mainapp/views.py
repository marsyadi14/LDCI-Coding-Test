from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.generic import TemplateView, DetailView
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.forms.models import model_to_dict

from .forms import UserForm, PostForm, LoginForm
from .models import Post, Status, User

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("dashboard")
            else:
                form.add_error("username", "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        posts = Post.objects.all().order_by("-post_id")
        page_number = self.request.GET.get("page", 1)
        
        paginator = Paginator(posts, 5)
        page_obj = paginator.get_page(page_number)

        context["posts"] = page_obj.object_list
        context["page_obj"] = page_obj
        
        context["form"] = PostForm(initial={"repost_val": ""})
        
        return context
    
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.instance.post_status = Status.ACTIVE
            form.instance.poster_id = self.request.user
            repost_val = form.cleaned_data.get("repost_val")
            if repost_val:
                form.instance.repost_id = Post.objects.get(post_id=repost_val)
            lat_val = form.cleaned_data.get("lat_val")
            lon_val = form.cleaned_data.get("lon_val")
            if lat_val != None and lon_val != None:
                form.instance.loc_lat = lat_val
                form.instance.loc_lon = lon_val
            form.save()
            return redirect("/")
        
        context = self.get_context_data()
        context["form"] = form
        context["detailed_post"] = False
        return self.render_to_response(context)
    
class DetailedPostView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = "post_detail.html"
    context_object_name = "post"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["form"] = PostForm(initial={"repost_val": ""})
        context["detailed_post"] = True
        
        return context
    
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            form.instance.post_status = Status.ACTIVE
            form.instance.poster_id = self.request.user
            repost_val = form.cleaned_data.get("repost_val")
            if repost_val:
                form.instance.repost_id = Post.objects.get(post_id=repost_val)
            lat_val = form.cleaned_data.get("lat_val")
            lon_val = form.cleaned_data.get("lon_val")
            if lat_val != None and lon_val != None:
                form.instance.loc_lat = lat_val
                form.instance.loc_lon = lon_val
            form.save()
            return redirect("/")
        
        context = self.get_context_data()
        context["form"] = form
        context["detailed_post"] = False
        return self.render_to_response(context)
    
@login_required
def toggle_like(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user in post.liker_id.all():
        post.liker_id.remove(request.user)
        liked = False
    else:
        post.liker_id.add(request.user)
        liked = True

    return JsonResponse({
        "liked": liked,
        "total_likes": post.liker_id.count(),
    })

class UserFormView(FormView):
    form_class = UserForm
    template_name = "signup.html"
    success_url = "/"
    
    def form_valid(self, form):
        print("FORM VALID CALLED")
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.activate()
        user.save()
        return redirect(self.get_success_url())
    
    def form_invalid(self, form):
        print("ERRORS:", form.errors)
        return super().form_invalid(form)

class PostFormView(FormView):
    form_class = PostForm
    template_name = "posts.html"
    success_url = "/"
    
    def form_valid(self, form):
        form.instance.post_status = Status.ACTIVE
        form.instance.poster_id = self.request.user
        form.save()
        print(form.cleaned_data)
        return super().form_valid(form)

def get_post_json(request, post_id):
    try:
        post_obj = Post.objects.get(post_id=post_id)
        post_dict = {
            "post_id": post_obj.post_id,
            "post_content": post_obj.post_content,
            "loc_lon": post_obj.loc_lon,
            "loc_lat": post_obj.loc_lat,
            "created_at": post_obj.created_at,
            "post_status": post_obj.post_status,
            "liker_id": list(post_obj.liker_id.values_list("user_id", flat=True)),
            "poster_id": post_obj.poster_id.user_id,
        }
        
        if post_obj.repost_id:
            post_dict["repost_id"] = post_obj.repost_id.post_id
        
        return JsonResponse(post_dict)
    except Post.DoesNotExist:
        return JsonResponse({'error': 'Post not found'}, status=404)

def get_all_post_json(request):
    post_count = Post.objects.count()
    
    max_post = request.GET.get('max_post', "5")
    if not max_post.isdecimal():
        max_post = 5
    elif int(max_post) > 5:
        max_post = 5
    else:
        max_post = int(max_post)
        
    page = request.GET.get('page', "0")
    if not page.isdecimal():
        page = 0
    elif int(page) < 0:
        page = 0
    else:
        page = int(page)
    
    return JsonResponse({
        "total_post": post_count,
        "posts": [entry for entry in Post.objects.values()[page*max_post:(page+1)*max_post]]
    })