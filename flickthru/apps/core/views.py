import datetime
from random import randint

from django.db.models import Max, Min
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from core.forms import LoginForm
from core.models import TitledImage, Like
from core.decorators import cbv_decorator, forbidden_user


def get_random_picture():
    '''
    Return random image, get by random id, if there trying to get
    image with id that was deleted, try again
    '''
    max_id = TitledImage.objects.aggregate(Max('id'))['id__max']
    min_id = TitledImage.objects.aggregate(Min('id'))['id__min']
    if not max_id:
        return None
    try:
        image = TitledImage.objects.get(id=randint(min_id, max_id))
    except TitledImage.DoesNotExist:
        return get_random_picture()
    return image


@cbv_decorator(forbidden_user(forbidden_usertypes=[u'AnonymousUser']))
class HomePageView(TemplateView):
    '''
    Return page for random slides
    '''

    template_name = "homepage.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        image = get_random_picture()
        if not image:
            context['no_images_yet'] = False
        return context


@login_required
def get_random_picture_params(request):
    '''
    Return random image parameters
    '''
    random_image = get_random_picture()
    if not random_image:
        return JsonResponse(
            {'status': 'error',
             'result': 'There is no images in database yet...'})
    likes = random_image.likes - random_image.dislikes
    image_info = {
        'id': random_image.id, 'title': random_image.title,
        'likes': likes,
        'score': random_image.media_like_count,
        'url':random_image.media_standard_resolution_url
    }
    return JsonResponse({'status': 'success', 'result': image_info})


@csrf_exempt
@login_required
@require_http_methods(["POST"])
def like_picture(request, id):
    '''
    Return random image parameters
    '''
    is_liked = request.POST.get('is_liked', 'No info')
    if is_liked == 'No info':
        return JsonResponse(
            {'status': 'error',
             'result': 'Please provide is_liked parameter'})
    image = get_object_or_404(TitledImage, id=id)
    user = request.user
    like = Like.objects.create(image=image, user=user)
    if is_liked == 'true':
        like.liked = True
        image.likes += 1
        result = 'Like was added'
    else:
        like.liked = False
        image.dislikes += 1
        result = 'Dislike was added'
    image.save()
    like.save()
    return JsonResponse({'status': 'success', 'result': result})


def login(request):
    login_form = LoginForm()

    redirect_url = reverse('homepage', args=[])
    redirect_url = request.GET.get('next') or redirect_url

    if request.method == 'POST' and 'login_form' in request.POST:
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            return login_form.login(request, redirect_url=redirect_url)

    return render(request, "login.html", {
        "login_form": login_form,
    })
