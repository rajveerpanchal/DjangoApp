from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Post, Like


@csrf_exempt
@login_required
def create_post(request):
    if request.method == 'POST':
        owner = request.user
        title = request.POST.get('title')
        content = request.POST.get('content')
        is_public = request.POST.get('is_public', False)

        post = Post.objects.create(owner=owner, title=title, content=content, is_public=is_public)
        return JsonResponse({'message': 'Post created successfully', 'post_id': post.id})
    else:
        return JsonResponse({'message': 'Invalid request method'})


@csrf_exempt
@login_required
def edit_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id, owner=request.user)
    except Post.DoesNotExist:
        return JsonResponse({'message': 'Post not found or you do not have permission to edit it'})

    if request.method == 'PUT':
        post.title = request.POST.get('title', post.title)
        post.content = request.POST.get('content', post.content)
        post.is_public = request.POST.get('is_public', post.is_public)
        post.save()
        return JsonResponse({'message': 'Post edited successfully'})
    elif request.method == 'DELETE':
        post.delete()
        return JsonResponse({'message': 'Post deleted successfully'})
    else:
        return JsonResponse({'message': 'Invalid request method'})


def get_all_posts(request):
    posts = Post.objects.all()
    post_data = []
    for post in posts:
        likes_count = Like.objects.filter(post=post).count()
        post_data.append({
            'id': post.id,
            'owner': post.owner.username,
            'title': post.title,
            'content': post.content,
            'is_public': post.is_public,
            'likes_count': likes_count
        })
    return JsonResponse(post_data, safe=False)
