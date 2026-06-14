import time
import jwt
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from .models import Question, Answer, Tag
from .forms import AskForm, AnswerForm
from .tasks import send_new_answer_notification, publish_new_answer


def paginate(objects_list, request, per_page=20):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)

    try:
        page = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page = paginator.page(1)

    return page


def index(request):
    questions = Question.objects.new()
    page = paginate(questions, request, per_page=20)
    for q in page.object_list:
        q.user_vote = q.get_user_vote(request.user)
    return render(request, 'questions/index.html', {
        'page': page,
        'questions': page.object_list
    })


def hot(request):
    questions = Question.objects.hot()
    page = paginate(questions, request, per_page=20)
    for q in page.object_list:
        q.user_vote = q.get_user_vote(request.user)
    return render(request, 'questions/hot.html', {
        'page': page,
        'questions': page.object_list
    })


def tag(request, tag_name):
    get_object_or_404(Tag, name=tag_name)
    questions = Question.objects.by_tag(tag_name)
    page = paginate(questions, request, per_page=20)
    for q in page.object_list:
        q.user_vote = q.get_user_vote(request.user)
    return render(request, 'questions/tag.html', {
        'page': page,
        'questions': page.object_list,
        'tag_name': tag_name
    })


def question(request, question_id):
    question_obj = get_object_or_404(
        Question.objects.select_related('author__profile'),
        id=question_id,
        is_active=True
    )

    question_obj.user_vote = question_obj.get_user_vote(request.user)
    answers = question_obj.answers.select_related('author__profile').all()
    page = paginate(answers, request, per_page=30)
    for a in page.object_list:
        a.user_vote = a.get_user_vote(request.user)

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(f"{reverse('core:login')}?next={request.get_full_path()}")

        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(user=request.user, question=question_obj)
            
            if question_obj.author != request.user and question_obj.author.email:
                send_new_answer_notification.delay(
                    question_obj.author.email,
                    question_obj.title,
                    answer.text[:200],
                    question_obj.id
                )

            from django.utils import timezone
            answer_data = {
                'id': answer.id,
                'text': answer.text,
                'author_username': answer.author.username,
                'rating': answer.rating,
                'created_at': timezone.now().isoformat(),
            }
            publish_new_answer.delay(question_obj.id, answer_data)
            
            paginator = Paginator(answers, 30)
            last_page = paginator.num_pages if paginator.num_pages > 0 else 1
            return redirect(f"{reverse('questions:question', args=[question_id])}?page={last_page}#answer-{answer.id}")
    else:
        form = AnswerForm()
    
    return render(request, 'questions/question.html', {
        'question': question_obj,
        'page': page,
        'answers': page.object_list,
        'answer_form': form,
    })


@login_required
def ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            question = form.save(user=request.user)
            return redirect('questions:question', question_id=question.id)
    else:
        form = AskForm()

    return render(request, 'questions/ask.html', {'form': form})


@require_POST
@login_required
def question_like(request, question_id):
    question = get_object_or_404(Question, id=question_id, is_active=True)
    value = int(request.POST.get('value', 0))
    if value not in [1, -1]:
        return JsonResponse({'error': 'Invalid value'}, status=400)
    
    new_value = question.vote(request.user, value)
    return JsonResponse({
        'success': True,
        'rating': question.rating,
        'user_vote': new_value
    })


@require_POST
@login_required
def answer_like(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id, is_active=True)
    value = int(request.POST.get('value', 0))
    if value not in [1, -1]:
        return JsonResponse({'error': 'Invalid value'}, status=400)
    
    new_value = answer.vote(request.user, value)
    return JsonResponse({
        'success': True,
        'rating': answer.rating,
        'user_vote': new_value
    })


@require_POST
@login_required
def answer_correct(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id, is_active=True)
    
    if request.user != answer.question.author:
        return JsonResponse({'error': 'Only question author can mark correct answer'}, status=403)
    
    success = answer.mark_as_correct(request.user)
    if success:
        return JsonResponse({
            'success': True,
            'answer_id': answer.id,
            'is_correct': True
        })
    return JsonResponse({'error': 'Failed to mark as correct'}, status=400)


@require_POST
@login_required
def answer_unmark(request, answer_id):
    answer = get_object_or_404(Answer, id=answer_id, is_active=True)
    
    if request.user != answer.question.author:
        return JsonResponse({'error': 'Only question author can unmark answer'}, status=403)
    
    success = answer.unmark_as_correct(request.user)
    if success:
        return JsonResponse({
            'success': True,
            'answer_id': answer.id,
            'is_correct': False
        })
    return JsonResponse({'error': 'Answer was not marked as correct'}, status=400)


@require_GET
def search_suggestions(request):
    query = request.GET.get('q', '').strip()
    
    if len(query) < 2:
        return JsonResponse({'suggestions': []})
    
    questions = Question.objects.filter(is_active=True).extra(
        where=["to_tsvector('simple', title || ' ' || text) @@ plainto_tsquery('simple', %s)"],
        params=[query]
    )[:10]
    
    suggestions = [
        {
            'id': q.id,
            'title': q.title,
            'url': reverse('questions:question', args=[q.id])
        }
        for q in questions
    ]
    
    return JsonResponse({'suggestions': suggestions})


@login_required
def centrifugo_token(request):
    payload = {
        'sub': str(request.user.id),
        'exp': int(time.time()) + 3600,
    }
    token = jwt.encode(payload, settings.CENTRIFUGO_TOKEN_SECRET, algorithm='HS256')
    return JsonResponse({'token': token})