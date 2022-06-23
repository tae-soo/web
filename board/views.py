from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect

from board.forms import PostForm
from board.models import Post
from reply.forms import ReplyForm
from reply.models import Reply


def mainPage(request):
    return render(request, 'board/index.html')




@login_required(login_url='/user/login')
def like(request, bid):
    post = Post.objects.get(id=bid) # 게시글 불러오기
    user = request.user
    if post.like.filter(id=user.id).exists():
        post.like.remove(user)
        return JsonResponse({'message': 'deleted', 'like_cnt':post.like.count()})
    else :
        post.like.add(request.user) # 게시글 좋아요에 사용자 정보 추가
        return JsonResponse({'message': 'added', 'like_cnt':post.like.count()})

    return JsonResponse({'message':'ok'})




@login_required(login_url='/user/login')
def create(request):
    if request.method == "GET":
        postForm = PostForm()
        context = {'postForm': postForm}
        return render(request, 'board/create.html', context) # render 기능 context를 'board/create.html에 전달
    elif request.method == "POST":
        postForm = PostForm(request.POST)
        if postForm.is_valid():
            post = postForm.save(commit=False)
            post.writer = request.user
            post.save()

        return redirect('/board/read/' + str(post.id))


def listGet(request):
    posts = Post.objects.all().order_by('-id')

    context = {'posts': posts}

    return render(request, 'board/list.html', context)


def readGet(request, bid):

    # select_related : 해당 클래스 기준 정방향  reply 안에 게시글 존재하기 때문에 사용 join sql 실행
    # prefetch_related : 해당 클래스 역방향  Post 안에 게시글이 없기 때문에 사용  query가 2개 실행이됨됨
    post = Post.objects.prefetch_related('reply_set').get(id=bid) # 'reply_set' 표현 고정

    replyForm = ReplyForm(instance=post)
    context = {'post': post, 'replyForm':replyForm}

    return render(request, 'board/read.html', context)

@login_required(login_url='/user/login')
def deleteGet(request, bid):
    post = Post.objects.get(id=bid)
    if request.user != post.writer:
        return redirect('/board/list')

    post.delete()

    return redirect('/board/list')

@login_required(login_url='/user/login')
def update(request, bid):
    post = Post.objects.get(id=bid)

    if request.user != post.writer:
        return redirect('/board/read/' + str(post.id))

    if request.method == "GET":
        context = {
            'post': post
        }
        return render(request, 'board/update.html', context)
    elif request.method == "POST":
        postForm = PostForm(request.POST, instance=post)
        if postForm.is_valid():
            post = postForm.save(commit=False)
            post.save()
        return redirect('/board/read/' + str(post.id))
