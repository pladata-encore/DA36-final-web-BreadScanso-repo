from django.db import models
from django.contrib.auth.models import User
from django import forms


### Models ###
# class Question(models.Model):
#     # Question -> User 참조가 author, voter 두개이므로, 역참조명 related_name을 반드시 설정해서 구분해야 한다.
#     author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='questions')
#     subject = models.CharField(max_length=200)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     modified_at = models.DateTimeField(auto_now=True)
#     voter = models.ManyToManyField(User, blank=True, related_name='question_votes') # 추천인 추가
#
#
# class Answer(models.Model):
#     author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='answers')
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     modified_at = models.DateTimeField(auto_now=True)
#     voter = models.ManyToManyField(User, blank=True, related_name='answer_votes') # 추천인 추가
#
#
# ### Forms ###
# class QuestionForm(forms.ModelForm):
#
#     class Meta:
#         model = Question
#         fields = ['subject', 'content'] # Form클래스에서 사용할 Model클래스 속성
#         # template에서 사용자에게 노출할 필드명
#         labels = {
#             'subject': '제목',
#             'content': '내용',
#         }