from abc import ABC, abstractmethod
from django.contrib import messages
# from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, resolve_url
from django.db.models import Q
from store.models import Question, QuestionForm, Answer
from member.models import Member

def store_main(request):
    return render(request, 'store/store_main.html')  # /store/

# 점주 회원관리
def member_store(request):
    members = Member.objects.all() # 모든 회원 정보 가져오기
    return render(request, 'member/member_store.html', {'members': members})

def store_home_edit(request):
    return render(request, 'store/store_home_edit.html')  # 홈 화면 수정

def about_breadscanso_edit(request):
    return render(request, 'store/about_breadscanso_edit.html')  # 브랜드 소개

def store_map(request):
    return render(request, 'store/store_map.html')  # 매장 안내

def store_map_edit(request):
    return render(request, 'store/store_map_edit.html')  # 매장 안내 수정

def store_event(request):
    return render(request, 'store/store_event.html')  # 이벤트

def store_event_edit(request):
    return render(request, 'store/store_event_edit.html')  # 이벤트 수정

def community_notice(request):
    return render(request, 'store/community_notice.html')  # 커뮤니티/공지사항

def community_notice_write(request):
    return render(request, 'store/community_notice_write.html')  # 커뮤니티/공지사항 글쓰기

def community_notice_modify(request, notice_id):
    return render(request, 'store/community_notice_modify.html', {'notice_id': notice_id})  # 커뮤니티/공지사항 글쓰기

def community_qna(request):
    return render(request, 'store/community_qna.html')  # 커뮤니티/qna

def store_account(request):
    return render(request, 'store/store_account.html')  # 매장정보


# Repository
class QuestionRepository(ABC):
    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def find_by_id(self, id):
        pass

    @abstractmethod
    def save(self, question):
        pass

    @abstractmethod
    def delete(self, id):
        pass

    @abstractmethod
    def find_by_subject(self, query):
        pass

    @abstractmethod
    def add_remove_voter(self, question, voter):
        pass


class QuestionRepositoryImpl(QuestionRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def find_all(self):
        return Question.objects.prefetch_related('author', 'answer_set').order_by('-created_at')

    def find_by_id(self, id):
        return Question.objects.get(id=id)

    def save(self, question):
        question.save()
        return question

    def delete(self, id):
        return Question.objects.filter(id=id).delete()

    def find_by_subject(self, query):
        return Question.objects.filter(Q(subject__icontains=query) | Q(content__icontains=query)).order_by('-created_at')

    def add_remove_voter(self, question, voter):
        if question.voter.filter(id=voter.id).exists():
            question.voter.remove(voter)
        else:
            question.voter.add(voter)


# Service
class QuestionService(ABC):
    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def find_by_id(self, id):
        pass

    @abstractmethod
    def create(self, question):
        pass

    @abstractmethod
    def modify(self, question):
        pass

    @abstractmethod
    def delete(self, id):
        pass

    @abstractmethod
    def find_by_subject(self, query):
        pass

    @abstractmethod
    def add_remove_voter(self, question_id, voter):
        pass


class QuestionServiceImpl(QuestionService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.__question_repository = QuestionRepositoryImpl.get_instance()

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def find_all(self):
        return self.__question_repository.find_all()

    def find_by_id(self, id):
        return self.__question_repository.find_by_id(id)

    def create(self, question):
        return self.__question_repository.save(question)

    def modify(self, question):
        return self.__question_repository.save(question)

    def delete(self, id):
        return self.__question_repository.delete(id)

    def find_by_subject(self, query):
        return self.__question_repository.find_by_subject(query)

    def add_remove_voter(self, question_id, voter):
        question = self.__question_repository.find_by_id(question_id)
        if voter == question.author:
            raise RuntimeError('본인이 작성한 글은 추천할 수 없습니다.')
        else:
            self.__question_repository.add_remove_voter(question, voter)
        return question


# Views
question_service = QuestionServiceImpl.get_instance()

def question_detail(request, question_id):
    question = question_service.find_by_id(question_id)
    return render(request, 'store/question_detail.html', {"question": question})

# @login_required(login_url='login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question = question_service.create(question)
            return redirect('store:question_detail', question_id=question.id)
        else:
            print('form.errors =', form.errors)
    else:
        form = QuestionForm()
    return render(request, 'store/question_form.html', {'form': form})

# @login_required(login_url='login')
def question_modify(request, question_id):
    question = question_service.find_by_id(question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다.')
        return redirect('store:question_detail', question_id=question_id)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            question = form.save(commit=False)
            question = question_service.modify(question)
            return redirect('store:question_detail', question_id=question_id)
    else:
        form = QuestionForm(instance=question)

    return render(request, 'store/question_form.html', {'form': form})

# @login_required(login_url='login')
def question_delete(request, question_id):
    question = question_service.find_by_id(question_id)
    if request.user != question.author:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('store:question_detail', question_id=question_id)

    question_service.delete(question_id)
    messages.success(request, '정상적으로 질문을 삭제했습니다.')
    return redirect('store:index')

def question_search(request):
    query = request.GET.get('query')
    questions = question_service.find_by_subject(query)
    results = [{'id': question.id, 'text': question.subject} for question in questions]
    return JsonResponse({"results": results})

# @login_required(login_url='login')
def question_vote(request, question_id):
    try:
        question = question_service.add_remove_voter(question_id, request.user)
        votes_count = question.voter.count() if hasattr(question, 'voter') else 0
        return JsonResponse({
            'result': 'success',
            'votes_count': votes_count
        })
    except Exception as e:
        return JsonResponse({
            'result': 'error',
            'message': str(e)
        }, status=400)

# Repository Layer
class AnswerRepository(ABC):
    @abstractmethod
    def save(self, answer):
        pass

    @abstractmethod
    def find_by_id(self, id):
        pass

    @abstractmethod
    def delete(self, answer):
        pass

    @abstractmethod
    def add_remove_voter(self, answer, voter):
        pass


class AnswerRepositoryImpl(AnswerRepository):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def save(self, answer):
        answer.save()
        return answer

    def find_by_id(self, id):
        return Answer.objects.get(id=id)

    def delete(self, answer):
        return answer.delete()

    def add_remove_voter(self, answer, voter):
        if answer.voter.filter(id=voter.id).exists():
            answer.voter.remove(voter)
        else:
            answer.voter.add(voter)


# Service Layer
class AnswerService(ABC):
    @abstractmethod
    def create(self, question_id, content, author):
        pass

    @abstractmethod
    def find_by_id(self, id):
        pass

    @abstractmethod
    def delete(self, answer):
        pass

    @abstractmethod
    def modify(self, answer):
        pass

    @abstractmethod
    def add_remove_voter(self, answer_id, voter):
        pass


class AnswerServiceImpl(AnswerService):
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.__answer_repository = AnswerRepositoryImpl.get_instance()

    @classmethod
    def get_instance(cls):
        if cls.__instance is None:
            cls.__instance = cls()
        return cls.__instance

    def create(self, question_id, content, author):
        question = Question.objects.get(id=question_id)
        answer = Answer(question=question, content=content, author=author)
        return self.__answer_repository.save(answer)

    def find_by_id(self, id):
        return self.__answer_repository.find_by_id(id)

    def delete(self, answer):
        return self.__answer_repository.delete(answer)

    def modify(self, answer):
        return self.__answer_repository.save(answer)

    def add_remove_voter(self, answer_id, voter):
        answer = self.__answer_repository.find_by_id(answer_id)
        if voter == answer.author:
            raise RuntimeError('본인이 작성한 글은 추천할수 없습니다')
        self.__answer_repository.add_remove_voter(answer, voter)
        return answer


# View Layer
answer_service = AnswerServiceImpl.get_instance()

# @login_required(login_url='login')
def answer_create(request, question_id):
    content = request.POST.get('content')
    author = request.user
    answer = answer_service.create(question_id, content, author)
    return redirect(f'{resolve_url("store:question_detail", question_id=question_id)}#answer_{answer.id}')


def answer_delete(request, answer_id):
    question_id = request.GET['question_id']
    answer = answer_service.find_by_id(answer_id)

    if answer.author != request.user:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('store:question_detail', question_id=question_id)

    answer_service.delete(answer)
    messages.success(request, '정상적으로 답변을 삭제했습니다.')
    return redirect('store:question_detail', question_id=question_id)


# @login_required(login_url='login')
def answer_modify(request, answer_id):
    question_id = request.GET['question_id']
    answer = answer_service.find_by_id(answer_id)

    if request.user != answer.author:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('store:question_detail', question_id=question_id)

    if request.method == 'POST':
        new_content = request.POST['content']
        answer.content = new_content
        answer_service.modify(answer)

    return redirect('store:question_detail', question_id=question_id)


# @login_required(login_url='login')
def answer_vote(request, answer_id):
    try:
        answer = answer_service.add_remove_voter(answer_id, request.user)
        votes_count = answer.voter.count() if hasattr(answer, 'voter') else 0
        return JsonResponse({'result': 'success', 'votes_count': votes_count})
    except Exception as e:
        return JsonResponse({'result': 'error', 'message': str(e)}, status=400)

