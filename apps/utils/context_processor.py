from apps.models import Category
from apps.models.shop import Like, Basket


def context_categories(request):
    return {
        'categories': Category.objects.all()
    }


def context_counts(request):
    if request.user.is_authenticated:
        likes = Like.objects.filter(user=request.user).values('products').count()
        if Basket.objects.filter(user=request.user).first():
            if Basket.objects.filter(user=request.user).first().basketproduct_set.all():
                basket = sum(Basket.objects.filter(user=request.user).values_list('basketproduct__quantity', flat=True))
            else:
                basket = 0
        else:
            basket = 0
    else:
        likes = 0
        basket = 0
    return {
        'counts': {
            'likes': likes,
            'basket': basket,
        }
    }


def get_custom_url(request):
    _url = '/'.join(request.path.split('/')[2:])
    return {
        'get_url': _url
    }
