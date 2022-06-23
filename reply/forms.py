from django import forms

from reply.models import Reply

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ('contents',)
        exclude =('writer', ) # writer는 입력을 안 받겠다