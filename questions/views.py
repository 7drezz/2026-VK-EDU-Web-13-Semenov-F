from django.shortcuts import render
from core.utils import paginate

def index(request):
    questions_list = []
    for i in range(1, 101):
        questions_list.append({
            'id': i,
            'title': f'Question title {i}',
            'text': f'This is the text of question {i}.',
            'answers_count': i % 5,
            'tags': ['python', 'django'] if i % 2 == 0 else ['javascript', 'react'],
            'created_at': '2 hours ago' if i < 10 else 'yesterday',
            'author': f'user_{i}',
            'rating': 50 - i
        })
    
    page = paginate(questions_list, request, per_page=20)
    return render(request, 'questions/index.html', {'page': page, 'questions': page.object_list})

def hot(request):
    questions_list = []
    for i in range(1, 101):
        questions_list.append({
            'id': i,
            'title': f'Hot question title {i}',
            'text': f'This is the text of popular question.',
            'answers_count': (5 - i) % 5,
            'tags': ['python', 'django'] if i % 2 == 0 else ['javascript', 'react'],
            'created_at': '2 hours ago' if i < 10 else 'yesterday',
            'author': f'popular_{i}',
            'rating': 100 - i
        })
    
    page = paginate(questions_list, request, per_page=20)
    return render(request, 'questions/hot.html', {'page': page, 'questions': page.object_list})

def tag(request, tag_name):
    questions_list = []
    for i in range(1, 101):
        if tag_name.lower() == 'sql':
            second_tag = 'postgresql'
        else:
            second_tag = 'sql'
        
        questions_list.append({
            'id': i,
            'title': f'Questions about {tag_name} #{i}',
            'text': f'This question is about {tag_name}.',
            'answers_count': i % 6,
            'tags': [tag_name, second_tag],
            'created_at': '2 hours ago' if i < 10 else 'yesterday',
            'author': f'{tag_name}_user_{i}',
            'rating': 50 - i
        })
    
    page = paginate(questions_list, request, per_page=20)
    return render(request, 'questions/tag.html', {'page': page, 'questions': page.object_list, 'tag_name': tag_name})

def question(request, question_id):
    question_data = {
        'id': question_id,
        'title': f'Question {question_id}: How to fix unzip error in Ubuntu 18.04?',
        'text': 'I have an archive. When unpacking it manually, I get the error message "an error occurred while extracting files." I tried using different archive managers, but nothing helps.',
        'answers_count': 2,
        'tags': ['linux', 'ubuntu', 'zip'],
        'created_at': '2 hours ago',
        'author': 'gwoix',
        'rating': 2
    }
    
    answers_list = []
    for i in range(1, 101):
        answers_list.append({
            'id': i,
            'text': f'Answer #{i}. Try installing p7zip-full instead, then use 7z to extract.' if i % 2 == 0 else f'Answer #{i}: The issue is likely a corrupted central directory. Fix the archive first.',
            'author': f'answer_user_{i}',
            'created_at': ['1 hour ago', '2 hours ago', '3 hours ago', 'yesterday'][min(i - 1, 3)],
            'rating': 20 - i,
            'is_correct': i == 2
        })
    
    page = paginate(answers_list, request, per_page=30)
    return render(request, 'questions/question.html', {
        'question': question_data,
        'page': page,
        'answers': page.object_list
    })

def ask(request):
    return render(request, 'questions/ask.html')