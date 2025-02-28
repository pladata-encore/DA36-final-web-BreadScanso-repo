from abc import ABC, abstractmethod
from django.contrib import messages
# from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, resolve_url
from django.db.models import Q
from store.models import Question, QuestionForm, Answer
from member.models import Member
import json
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator, EmptyPage
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required


def store_main(request):
    return render(request, 'store/store_main_map.html' )

# 매장페이지 - 회원관리
def member_store(request):
    # 검색 기능 처리
    search_query = request.POST.get('search_input', '')

    if search_query:
        # 검색어가 있을 경우 회원명 기준으로 필터링
        members = Member.objects.filter(name__icontains=search_query)
    else:
        # 검색어가 없을 경우 모든 회원 정보 가져오기
        members = Member.objects.all()

    # 페이지네이션 처리 (10개씩)
    paginator = Paginator(members, 10)
    # 페이지 번호 가져오기, 유효하지 않으면 1 페이지로 설정
    page_number = request.GET.get('page', 1)
    try:
        page_number = int(page_number)
        if page_number < 1:
            page_number = 1
    except ValueError:
        page_number = 1
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        # 페이지 번호가 범위를 벗어난 경우 마지막 페이지로 설정
        page_obj = paginator.get_page(paginator.num_pages)

    # GET 요청 처리 (member 데이터 가져오기)
    member = request.user.member

    # 하나의 딕셔너리로 합쳐서 전달
    context = {
        'page_obj': page_obj,
        'member': member
    }

    return render(request, 'member/member_store.html', context)


# 회원 정보 업데이트
def update_member_store(request):
    if request.method == 'POST':
        try:
            # POST로 넘어오는 데이터
            data = json.loads(request.body)
            member_id = data.get('member_id')  # 회원 ID
            new_name = data.get('new_name')  # 새로운 회원명
            new_phone_num = data.get('new_phone_num')  # 새로운 휴대폰 번호
            new_email = data.get('new_email')  # 새로운 이메일

            # 유효성 검사
            if not member_id or not new_name or not new_phone_num or not new_email:
                return JsonResponse({'success': False, 'error': 'Invalid data provided'})

            # 회원 존재 여부 확인
            try:
                member = Member.objects.get(member_id=member_id)
            except Member.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Member not found'})

            # 회원 정보 업데이트
            member.name = new_name
            member.phone_num = new_phone_num
            member.email = new_email
            member.save()

            return JsonResponse({'success': True})
        except Exception as e:
            print(f"Error updating member: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)})

    return JsonResponse({'success': False, 'error': '잘못된 요청입니다.'})

def member_store_edit(request):
    return render(request, 'store/member_store_edit.html')  # 회원 정보 수정

from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db import connection
import json
import traceback

@require_http_methods(["POST"])
def delete_member_store(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # JSON 데이터 파싱
            member_ids = data.get("member_ids", [])

            if not member_ids:
                return JsonResponse({
                    "success": False,
                    "message": "삭제할 회원을 선택해주세요."
                })

            with connection.cursor() as cursor:
                # 먼저 member_member 테이블에서 삭제
                sql_member = "DELETE FROM member_member WHERE member_id IN (%s)" % ','.join(['%s'] * len(member_ids))
                cursor.execute(sql_member, member_ids)
                deleted_from_member = cursor.rowcount

                # auth_user 테이블에서도 삭제
                sql_user = "DELETE FROM auth_user WHERE username IN (%s)" % ','.join(['%s'] * len(member_ids))
                cursor.execute(sql_user, member_ids)
                deleted_from_user = cursor.rowcount

            return JsonResponse({
                "success": True,
                "message": f"{deleted_from_member}명의 회원 정보 및 {deleted_from_user}명의 사용자 계정이 삭제되었습니다."
            })

        except Exception as e:
            error_details = traceback.format_exc()
            return JsonResponse({
                "success": False,
                "message": f"삭제 실패: {str(e)}",
                "details": error_details
            })

    return JsonResponse({"success": False, "message": "잘못된 요청입니다."})


# @require_http_methods(["POST"])
# def delete_member_store(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)  # JSON 데이터 파싱
#             member_ids = data.get("member_ids", [])
#
#             if not member_ids:
#                 return JsonResponse({
#                     "success": False,
#                     "message": "삭제할 회원을 선택해주세요."
#                 })
#
#             # 직접 SQL 쿼리 실행하여 member_member 테이블에서만 삭제
#             from django.db import connection
#
#             with connection.cursor() as cursor:
#                 # 테이블 이름과 필드 이름을 정확하게 사용
#                 # 여러 회원을 삭제할 때는 IN 절 사용
#                 sql = "DELETE FROM member_member WHERE member_id IN (%s)" % ','.join(['%s'] * len(member_ids))
#                 cursor.execute(sql, member_ids)
#                 row_count = cursor.rowcount
#
#             return JsonResponse({"success": True, "message": f"{row_count}명의 회원이 삭제되었습니다."})
#         except Exception as e:
#             import traceback
#             error_details = traceback.format_exc()
#             return JsonResponse({
#                 "success": False,
#                 "message": f"삭제 실패: {str(e)}",
#                 "details": error_details
#             })
#
#     return JsonResponse({"success": False, "message": "잘못된 요청입니다."})
# # 회원 삭제
# @require_http_methods(["POST"])
# def delete_member_store(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)  # JSON 데이터 파싱
#             member_ids = data.get("member_ids", [])
#
#             if not member_ids:
#                 return JsonResponse({
#                     "success": False,
#                     "message": "삭제할 회원을 선택해주세요."
#                 })
#
#             deleted_count, _ = Member.objects.filter(member_id__in=member_ids).delete()
#
#             return JsonResponse({"success": True, "message": f"선택한 회원이 삭제되었습니다."})
#         except Exception as e:
#             return JsonResponse({"success": False, "message": f"삭제 실패: {str(e)}"})
#
#     return JsonResponse({"success": False, "message": "잘못된 요청입니다."})

def store_home_edit(request):
    # GET 요청 처리 (member 데이터 가져오기)
    member = request.user.member
    return render(request, 'store/store_home_edit.html', {"member": member})  # 홈 화면 수정

def about_breadscanso_edit(request):
    # GET 요청 처리 (member 데이터 가져오기)
    member = request.user.member
    return render(request, 'store/about_breadscanso_edit.html', {"member": member})  # 브랜드 소개

def store_map(request):
    member = request.user.member

    store = member.store,
    store_name = dict(member._meta.get_field('store').choices).get(store[0], '')
    store_address = member.store_address
    store_time = member.store_time
    store_notes = member.store_notes

    context = {
        'member': member,
        'store_address': store_address,
        'store_time': store_time,
        'store_notes': store_notes,
        'store' : store,
        'store_name' : store_name,
    }
    return render(request, 'store/store_map.html', context)  # 매장 안내

@csrf_exempt  # CSRF 검사를 비활성화
@login_required  # 로그인한 사용자만 접근 가능
def store_map_edit(request):
    # POST 요청 처리 (AJAX로 받은 데이터를 저장)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            store_address = data.get('store_address')
            store_time = data.get('store_time')
            store_notes = data.get('store_notes')

            member = request.user.member
            member.store_address = store_address
            member.store_time = store_time
            member.store_notes = store_notes
            member.save()

            return JsonResponse({'status': 'success', 'message': '변경사항이 저장되었습니다.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    # GET 요청 시 기존 매장의 정보 제공!
    member = request.user.member
    store_address = member.store_address
    store_time = member.store_time
    store_notes = member.store_notes

    context = {
        'member': member,
        'store_address': store_address,
        'store_time': store_time,
        'store_notes': store_notes,
    }
    return render(request, 'store/store_map_edit.html', context)

def store_event(request):
    member = request.user.member
    return render(request, 'store/store_event.html', {"member": member})  # 이벤트

def store_event_edit(request):
    member = request.user.member
    return render(request, 'store/store_event_edit.html', {"member": member})  # 이벤트 수정

def community_notice(request):
    member = request.user.member
    return render(request, 'store/community_notice.html', {"member": member})  # 커뮤니티/공지사항

def community_notice_write(request):
    member = request.user.member
    return render(request, 'store/community_notice_write.html', {"member": member})  # 커뮤니티/공지사항 글쓰기

def community_notice_modify(request, notice_id):
    member = request.user.member
    return render(request, 'store/community_notice_modify.html', {'notice_id': notice_id, "member": member})  # 커뮤니티/공지사항 글쓰기

def community_qna(request):
    member = request.user.member
    return render(request, 'store/community_qna.html', {"member": member})  # 커뮤니티/qna

def store_account(request):
    member = request.user.member
    return render(request, 'store/store_account.html', {"member": member})  # 매장정보


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

    member = request.user.member
    context = {
        'form': form,
        'member': member
    }

    return render(request, 'store/question_form.html', context)

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

