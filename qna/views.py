from abc import ABC, abstractmethod
from enum import member
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, resolve_url
from django.db.models import Q
from member.models import QnA, QnAReply, QuestionForm
from member.models import Member
import json
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

def qna_main(request):
    qnas = QnA.objects.all().order_by('-created_at')

    # 페이지당 항목 수 (고정)
    qnas_per_page = 10

    # 페이지네이션 처리
    paginator = Paginator(qnas, qnas_per_page)

    # 페이지 번호 가져오기
    page_number = request.GET.get("page", 1)
    try:
        page_number = int(page_number)
        if page_number < 1:
            page_number = 1
    except ValueError:
        page_number = 1

    # 페이지 객체 가져오기
    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # 페이지 범위 계산
    max_pages = 5
    current_page = page_obj.number
    total_pages = paginator.num_pages

    start_page = max(1, current_page - 2)
    end_page = min(total_pages, start_page + max_pages - 1)

    if end_page - start_page + 1 < max_pages and start_page > 1:
        start_page = max(1, end_page - max_pages + 1)

    page_range = range(start_page, end_page + 1)

    # member = request.user.member

    context = {
        'qnas': qnas,
        'page_obj': page_obj,
        'page_range': page_range,
        'total_qnas': qnas.count(),  # 총 공지사항 수
        # 'member': member,
    }
    return render(request, 'qna/qna_main.html', context)  # qna/qna_main


# Repository
class QuestionRepository(ABC):
    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def find_by_id(self, qna_id):
        pass

    @abstractmethod
    def save(self, qna):
        pass

    @abstractmethod
    def delete(self, qna_id):
        pass

    @abstractmethod
    def find_by_title(self, query):
        pass

    # @abstractmethod
    # def add_remove_voter(self, question, voter):
    #     pass


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
        return QnA.objects.prefetch_related('author', 'answer_set').order_by('-created_at')

    def find_by_id(self, qna_id):
        return QnA.objects.get(qna_id=qna_id)

    def save(self, qna):
        qna.save()
        return qna

    def delete(self, qna_id):
        return QnA.objects.filter(qna_id=qna_id).delete()

    def find_by_title(self, query):
        return QnA.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).order_by('-created_at')

    # def add_remove_voter(self, question, voter):
    #     if question.voter.filter(id=voter.id).exists():
    #         question.voter.remove(voter)
    #     else:
    #         question.voter.add(voter)


# Service
class QuestionService(ABC):
    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def find_by_id(self, qna_id):
        pass

    @abstractmethod
    def create(self, qna):
        pass

    @abstractmethod
    def modify(self, qna):
        pass

    @abstractmethod
    def delete(self, qna_id):
        pass

    @abstractmethod
    def find_by_title(self, query):
        pass

    # @abstractmethod
    # def add_remove_voter(self, qna_id, voter):
    #     pass


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

    def find_by_id(self, qna_id):
        return self.__question_repository.find_by_id(qna_id)

    def create(self, qna):
        return self.__question_repository.save(qna)

    def modify(self, qna):
        return self.__question_repository.save(qna)

    def delete(self, qna_id):
        return self.__question_repository.delete(qna_id)

    def find_by_title(self, query):
        return self.__question_repository.find_by_title(query)

    # def add_remove_voter(self, qna_id, voter):
    #     question = self.__question_repository.find_by_id(qna_id)
    #     if voter == question.author:
    #         raise RuntimeError('본인이 작성한 글은 추천할 수 없습니다.')
    #     else:
    #         self.__question_repository.add_remove_voter(question, voter)
    #     return question


# Views
question_service = QuestionServiceImpl.get_instance()

# def qna_main(request):
#     qnas = QnA.objects.all().order_by('-created_at')
#
#     # 페이지당 항목 수 (고정)
#     qnas_per_page = 10
#
#     # 페이지네이션 처리
#     paginator = Paginator(qnas, qnas_per_page)
#
#     # 페이지 번호 가져오기
#     page_number = request.GET.get("page", 1)
#     try:
#         page_number = int(page_number)
#         if page_number < 1:
#             page_number = 1
#     except ValueError:
#         page_number = 1
#
#     # 페이지 객체 가져오기
#     try:
#         page_obj = paginator.page(page_number)
#     except EmptyPage:
#         page_obj = paginator.page(paginator.num_pages)
#
#     # 페이지 범위 계산
#     max_pages = 5
#     current_page = page_obj.number
#     total_pages = paginator.num_pages
#
#     start_page = max(1, current_page - 2)
#     end_page = min(total_pages, start_page + max_pages - 1)
#
#     if end_page - start_page + 1 < max_pages and start_page > 1:
#         start_page = max(1, end_page - max_pages + 1)
#
#     page_range = range(start_page, end_page + 1)
#
#     context = {
#         'qnas': qnas,
#         'page_obj': page_obj,
#         'page_range': page_range,
#         'total_qnas': qnas.count(),  # 총 공지사항 수
#     }
#
#     return render(request, 'store/qna_main.html', context)  # 템플릿 파일 경로 지정


# def question_detail(request, qna_id):
#     question = question_service.find_by_id(qna_id)
#     return render(request, 'store/question_detail.html', {"question": question})
def qna_detail(request, qna_id):
    qna = question_service.find_by_id(qna_id)
    # 질문에 달린 답변들을 가져옴
    answers = QnAReply.objects.filter(qna_id=qna_id)

    # member = request.user.member

    context = {
        'qna': qna,
        'answers': answers,
        # 'member': member,
    }
    return render(request, 'qna/qna_detail.html', context)



# @login_required(login_url='login')
def qna_create(request):
    # stores = [
    #     {"id": "A", "name": "Store A"},
    #     {"id": "B", "name": "Store B"}
    # ]  # 매장 목록을 리스트 형태로 제공

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            # store = request.POST.get('store', '전체')  # 선택된 매장
            qna = form.save(commit=False)
            qna.member_id = request.user
            # qna.store = store
            qna = question_service.create(qna)
            return redirect('qna:qna_detail', qna_id=qna.qna_id)
        else:
            print('form.errors =', form.errors)
    else:
        form = QuestionForm()

    member = request.user.member
    context = {
        'form': form,
        'member': member,
        # 'stores': stores,  # 🔥 stores 추가
    }

    return render(request, 'qna/qna_form.html', context)



# @login_required(login_url='uauth:login')
def qna_modify(request, qna_id):
    qna = question_service.find_by_id(qna_id)

    # 인가 확인(작성자 본인 여부)
    if request.user != qna.member_id:
        from django.contrib import messages
        messages.error(request, '수정 권한이 없습니다.') # 논필드오류
        return redirect('qna:qna_detail', qna_id=qna_id)

    # GET/POST 요청 분기
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=qna)  # 기존 qna에 사용자입력값 덮어쓰기
        if form.is_valid():
            qna = form.save(commit=False)  # form -> model 변환만
            qna = question_service.modify(qna)
            return redirect('qna:qna_detail', qna_id=qna_id)
    else:
        form = QuestionForm(instance=qna)

    form = QuestionForm(instance=qna)
    return render(request, 'qna/qna_form.html', {'form': form})

# @login_required(login_url='login')
def qna_delete(request, qna_id):
    qna = question_service.find_by_id(qna_id)
    if request.user != qna.member_id:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('qna:qna_detail', qna_id=qna_id)

    question_service.delete(qna_id)
    messages.success(request, '정상적으로 질문을 삭제했습니다.')
    return redirect('qna:qna_main')

def qna_search(request):
    query = request.GET.get('query')
    qna = question_service.find_by_title(query)
    results = [{'qna_id': qna.qna_id, 'text': qna.title} for qna in qna]
    return JsonResponse({"results": results})

# @login_required(login_url='login')
# def question_vote(request, qna_id):
#     try:
#         qna = question_service.add_remove_voter(qna_id, request.user)
#         votes_count = qna.voter.count() if hasattr(qna, 'voter') else 0
#         return JsonResponse({
#             'result': 'success',
#             'votes_count': votes_count
#         })
#     except Exception as e:
#         return JsonResponse({
#             'result': 'error',
#             'message': str(e)
#         }, status=400)

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

    # @abstractmethod
    # def add_remove_voter(self, answer, voter):
    #     pass


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
        return QnAReply.objects.get(id=id)

    def delete(self, answer):
        return answer.delete()

    # def add_remove_voter(self, answer, voter):
    #     if answer.voter.filter(id=voter.id).exists():
    #         answer.voter.remove(voter)
    #     else:
    #         answer.voter.add(voter)


# Service Layer
class AnswerService(ABC):
    @abstractmethod
    def create(self, qna_id, content, author_id):
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

    # @abstractmethod
    # def add_remove_voter(self, answer_id, voter):
    #     pass


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

    def create(self, qna_id, content, author_id):
        question = QnA.objects.get(qna_id=qna_id)
        answer = QnAReply(qna_id=question.qna_id, content=content, author_id=author_id)
        return self.__answer_repository.save(answer)

    def find_by_id(self, id):
        return self.__answer_repository.find_by_id(id)

    def delete(self, answer):
        return self.__answer_repository.delete(answer)

    def modify(self, answer):
        return self.__answer_repository.save(answer)

    # def add_remove_voter(self, answer_id, voter):
    #     answer = self.__answer_repository.find_by_id(answer_id)
    #     if voter == answer.author:
    #         raise RuntimeError('본인이 작성한 글은 추천할수 없습니다')
    #     self.__answer_repository.add_remove_voter(answer, voter)
    #     return answer


# View Layer
answer_service = AnswerServiceImpl.get_instance()

# @login_required(login_url='login')
def answer_create(request, qna_id):
    content = request.POST.get('content')
    author_id = request.user.member.member_id
    answer = answer_service.create(qna_id, content, author_id)

    return redirect(f'{resolve_url("qna:qna_detail", qna_id=qna_id)}#answer_{answer.id}')


def answer_delete(request, answer_id):
    qna_id = request.GET['qna_id']
    answer = answer_service.find_by_id(answer_id)

    if answer.author_id != request.user:
        messages.error(request, '삭제권한이 없습니다.')
        return redirect('qna:qna_detail', qna_id=qna_id)

    answer_service.delete(answer)
    messages.success(request, '정상적으로 답변을 삭제했습니다.')
    return redirect('qna:qna_detail', qna_id=qna_id)


# @login_required(login_url='login')
def answer_modify(request, answer_id):
    qna_id = request.GET['qna_id']
    answer = answer_service.find_by_id(answer_id)

    if request.user != answer.author_id:
        messages.error(request, '수정 권한이 없습니다.')
        return redirect('qna:qna_detail', qna_id=qna_id)

    if request.method == 'POST':
        new_content = request.POST['content']
        answer.content = new_content
        answer_service.modify(answer)

    return redirect('qna:qna_detail', qna_id=qna_id)


# @login_required(login_url='login')
# def answer_vote(request, answer_id):
#     try:
#         answer = answer_service.add_remove_voter(answer_id, request.user)
#         votes_count = answer.voter.count() if hasattr(answer, 'voter') else 0
#         return JsonResponse({'result': 'success', 'votes_count': votes_count})
#     except Exception as e:
#         return JsonResponse({'result': 'error', 'message': str(e)}, status=400)

