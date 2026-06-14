import jwt
import time
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

def paginate(objects_list, request, per_page=10):
    paginator = Paginator(objects_list, per_page)
    page_number = request.GET.get('page', 1)
    
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    
    return page

def generate_centrifugo_token(user_id):
    payload = {
        'sub': str(user_id),
        'exp': int(time.time()) + 3600,
    }
    return jwt.encode(payload, settings.CENTRIFUGO_SECRET, algorithm='HS256')