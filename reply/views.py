from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from board.models import Post
from reply.forms import ReplyForm
from reply.models import Reply

@login_required(login_url='/user/login') #로그인했을 때 동작하게 함
def create(request, bid):
    if request.method == "POST":
        replyForm = ReplyForm(request.POST)
        if replyForm.is_valid():
            reply = replyForm.save(commit=False)
            post = Post() # 몇번 게시글의 어떤 사용자가 남긴 댓글인지 확인 가능
            post.id =bid
            reply.post = post
            reply.writer = request.user # 현재 로그인한 사용자 정보 저장
            reply.save()
        return redirect('/reply/read/' + str(reply.id))


def list(request):
    replys = Reply.objects.all().order_by('-id')

    return render(request, 'reply/list.html', {'replys':replys})

def read(request, rid):
    reply = Reply.objects.get(id=rid)

    return render(request, 'reply/read.html', {'reply':reply})

@login_required(login_url='/user/login')
def delete(request, rid):
    reply = Reply.objects.get(id=rid)
    if request.user != reply.writer:
        return redirect('/reply/list')
    reply.delete()

    return redirect('/reply/list')

@login_required(login_url='/user/login')
def update(request, rid):
    reply = Reply.objects.get(id=rid)

    if request.user != reply.writer:
        return redirect('/reply/read/' + str(reply.id))

    if request.method == "GET":
        replyForm = ReplyForm(instance=reply)
        return render(request, 'reply/create.html', {'replyForm': replyForm})
    elif request.method == "POST":
        replyForm = ReplyForm(request.POST, instance=reply)
        if replyForm.is_valid():
            reply = replyForm.save(commit=False)
            reply.save()
        return redirect('/reply/read/' + str(reply.id))