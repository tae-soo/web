from django.contrib.auth.models import User
from django.db import models

from board.models import Post


class Reply(models.Model):
    contents = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # 게시글과 댓글 관계형성
    writer = models.ForeignKey(User, on_delete=models.CASCADE) # 작성자, 사용자 관계형성 / 1대 다의 관계를 가질 때 '다'에게 foreignkey를 준다. 예시> 작성자:사용자 = N : 1
