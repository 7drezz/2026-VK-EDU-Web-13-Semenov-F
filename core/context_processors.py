from django.core.cache import cache
from questions.models import Tag
from core.models import Profile


def sidebar(request):
    popular_tags = cache.get('popular_tags')
    if popular_tags is None:
        tags = Tag.objects.popular(20)
        popular_tags = [{'name': t.name} for t in tags]
    
    best_members = cache.get('best_members')
    if best_members is None:
        best_members = Profile.objects.best_members(10)
    
    return {
        'popular_tags': popular_tags,
        'best_members': best_members,
    }