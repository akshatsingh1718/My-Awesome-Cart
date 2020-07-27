from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from .models import Blogpost, Contact, BlogpostComment
from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import F
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# custom tag
from blog.templatetags import extras
# forms
from .forms import LoginForm, ContactForm, BlogPostForm
# Create your views here.


@login_required(login_url='/blog/login')
def myCreations(request):
    user = request.user
    blogs = Blogpost.objects.filter(author=user.username)
    context = {'myposts': blogs}
    return render(request, 'blog/mycreations.html', context)


def index(request):
    myposts = Blogpost.objects.all()
    params = {'myposts':  myposts}
    return render(request, "blog/index.html", params)


def blogPost(request, blogId):
    # blog = get_object_or_404(Blogpost, pk=blogId)
    try:
        blog = Blogpost.objects.get(post_id=blogId)
        blog.views = blog.views + 1
        blog.save()
        # comment or parent comment fetching by timestamp
        comments = BlogpostComment.objects.filter(
            post=blog,
            parent=None
        ).order_by('-timestamp')
        # fetching replies where parent should be None because
        # if the parent is None the they will be comment not replies
        replies = BlogpostComment.objects.filter(
            post=blog).exclude(parent=None)
        replyDict = {}
        for reply in replies:
            if reply.parent.sno not in replyDict.keys():
                replyDict[reply.parent.sno] = [reply]
            else:
                replyDict[reply.parent.sno].append(reply)

        print(replyDict, "   ", comments)
    except ObjectDoesNotExist:
        return redirect('/blog/')
    params = {'blog': blog, 'comments': comments, 'replies': replyDict}
    return render(request, "blog/blogPost.html", params)


def blogpostComment(request):
    if request.method == 'POST':
        comment = request.POST.get('comment')
        user = request.user
        post_id = request.POST.get("post_id")
        post = Blogpost.objects.get(post_id=post_id)

        comment_or_id = request.POST.get("comment_or_parentId")

        if comment_or_id == 'comment':
            comment = BlogpostComment(
                comment=comment,
                user=user,
                post=post
            )
            comment.save()
        else:
            try:
                comment_or_id = comment_or_id.replace('reply', '')
                parent = BlogpostComment.objects.get(sno=comment_or_id)
                comment = BlogpostComment(
                    comment=comment,
                    user=user,
                    post=post,
                    parent=parent
                )
                comment.save()
            except ObjectDoesNotExist:
                return HttpResponse("<h1>Server Error</h1>")
        return redirect(f'/blog/blogpost/{post_id}')


def searchMatch(query, item):
    for word in query:
        if word in item.title.lower() or word in item.description.lower():
            return True
    return False


def search(request):
    query = request.GET.get('search')
    query_words = query.lower().split()
    mathced_blogs = []
    try:
        blogs = Blogpost.objects.all()
        mathced_blogs = [
            item for item in blogs if searchMatch(query_words, item)]
        if len(mathced_blogs) == 0:
            raise ObjectDoesNotExist
        else:
            params = {'blogs': mathced_blogs}
            return render(request, 'blog/search.html', params)
    except ObjectDoesNotExist:
        params = {'search': query}
        return render(request, 'blog/search.html', params)


def about(request):
    return render(request, 'blog/about.html')


def contactUs(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank You for your feedback')
    form = ContactForm()
    return render(request, 'blog/contact.html', {'forms': form})

# login and logout API's


def loginUser(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # cleaning data to get username and password
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # authenticating user
            user = authenticate(password=password, username=username)
            if user is not None:
                messages.success(request, 'Successfully Logged In')
                login(request, user)
                return redirect('/blog')
            else:
                messages.error(request, 'Invalid Username or Password!')
    # if the request is get or if the user is not authenticated
    # redirect user to Login Page
    form = LoginForm()
    return render(request, 'blog/login.html', {'form': form})


def logoutUser(request):
    if not request.user.is_anonymous:
        logout(request)
    return redirect('/blog')

# Api to create a Blog
@login_required(login_url='/blog/login')
def createBlog(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        print(form)
        print(form.is_valid())
        if form.is_valid():
            print(form)
            form.save()
            return redirect('/blog')
    form = BlogPostForm()
    return render(request, 'blog/createblog.html', {'forms': form})
