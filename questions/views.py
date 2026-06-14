from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Question, Answer, Tag

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
    return render(request, 'questions/index.html', {
        'page': page,
        'questions': page.object_list
    })

def hot(request):
    questions = Question.objects.hot()
    page = paginate(questions, request, per_page=20)
    return render(request, 'questions/hot.html', {
        'page': page,
        'questions': page.object_list
    })

def tag(request, tag_name):
    get_object_or_404(Tag, name=tag_name)
    questions = Question.objects.by_tag(tag_name)
    page = paginate(questions, request, per_page=20)
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
    
    answers = question_obj.answers.select_related('author__profile').all()
    page = paginate(answers, request, per_page=30)
    
    return render(request, 'questions/question.html', {
        'question': question_obj,
        'page': page,
        'answers': page.object_list
    })

def ask(request):
    return render(request, 'questions/ask.html')