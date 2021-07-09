from django.shortcuts import render,redirect
from .models import Post

from django.contrib.auth.decorators import login_required
# Create post view
@login_required
def post_create_view(request):

    if request.method == "POST":
        context ={}

        title = request.POST['title']
        content = request.POST['content']

        if title and content:
            user = request.user
            post = Post.objects.create(title= title, content = content,author = user)
            return redirect('posts:detail', id = post.id)
        else:
            context['error'] = 'Your title and content cant be empty'
            return render(request,'posts/create.html', context = context)
    else:
        return render(request,'posts/create.html')

#to view  one specific blog post
def post_detail_view(request,id):
    post = Post.objects.filter(id = id).first()
    context = {'post': post}
    return render(request, 'posts/detail.html', context = context)

#this will be to view all our blog post
def post_list_view(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'posts/list.html', context = context)

#update one specific post
@login_required
def post_update_view(request,id):
    context ={}
    post = Post.objects.filter(id = id).first()
    context['post']=post
    if request.user == post.author:
        if request.method == "POST":


            title = request.POST['title']
            content = request.POST['content']

            if title and content:
                post.title = title
                post.content = content
                post.save()
                context['error'] = 'There has been no error. Your post has been updated successfully!'
                return render(request,'posts/update.html',context= context)
            else:
                context['error'] = 'Your title and content cant be empty'
                return render(request,'posts/update.html', context = context)
        else:
            return render(request,'posts/update.html', context = context)
    else:
        return redirect('posts:list')

#delete one specific post
@login_required
def post_delete_view(request,id):
    post = Post.objects.filter(id=id).first()
    if request.user == post.author:
        if request.method== "POST":
            post.delete()
            return redirect('posts:list')
        else:
            return render(request, 'posts/delete.html')
    else :
        return redirect('posts:list')
