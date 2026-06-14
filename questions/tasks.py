from celery import shared_task
from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from cent import Client


@shared_task
def update_popular_tags_cache():
    from questions.models import Tag
    tags = Tag.objects.popular(20)
    # Преобразуем в список словарей для сериализации
    tags_data = [{'name': t.name, 'count': t.question_count} for t in tags]
    cache.set('popular_tags', tags_data, timeout=3600)


@shared_task
def update_best_members_cache():
    from core.models import Profile
    members = Profile.objects.best_members(10)
    cache.set('best_members', members, timeout=3600)


@shared_task
def send_new_answer_notification(question_author_email, question_title, answer_preview, question_id):
    send_mail(
        subject=f'New answer: {question_title[:50]}',
        message=f'Someone answered:\n\n{answer_preview[:200]}\n\nView: http://localhost:8000/question/{question_id}/',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[question_author_email],
        fail_silently=False,
    )


@shared_task
def publish_new_answer(question_id, answer_data):
    try:
        client = Client(settings.CENTRIFUGO_API_URL, api_key=settings.CENTRIFUGO_API_KEY, timeout=2)
        client.publish(f'questions:{question_id}', answer_data)
    except Exception:
        pass