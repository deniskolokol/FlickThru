from django_webtest import WebTest
from django.core.urlresolvers import reverse
from model_mommy import mommy
from django.utils.encoding import force_text
from core.models import User


class AuthTestMixin(object):

    def init_users(self):
        # Create User object
        self.user = User.objects.create(email='user@mail.com', username="user")
        self.user.set_password('test')
        self.user.save()

    def login(self, login, password):
        resp = self.app.get(reverse('account_login'))
        form = resp.forms[0]
        form['login'] = login
        form['password'] = password
        form.submit()


class TitledImageTest(WebTest, AuthTestMixin):
    def setUp(self):
        self.init_users()
        self.login(self.user.email, 'test')
        self.image = mommy.make('core.TitledImage',
                           _fill_optional=True)

    def test_get_random_picture_params(self):
        """Create Image
        test that get_random_picture_params return us all what we need
        """
        url = reverse('random-picture')
        resp = self.app.get(url)
        likes = self.image.likes - self.image.dislikes
        image_info = {
            'id': self.image.id, 'title': self.image.title,
            'likes': likes,
            'score': self.image.media_like_count,
            'url': self.image.media_standard_resolution_url
        }
        self.assertJSONEqual(force_text(resp.content),
                             {'status': 'success', 'result': image_info})

    def test_like_picture(self):
        """Like Image
        test that like_picture likes and dislikes self.images in correct way
        """
        url = reverse('like-picture', args=(self.image.id,))
        resp = self.app.post(url, {'id': self.image.id, 'is_liked': 'true'})
        self.assertJSONEqual(force_text(resp.content),
                             {'status': 'success',
                              'result': 'Like was added'})
        resp = self.app.post(url, {'id': self.image.id, 'is_liked': 'false'})
        self.assertJSONEqual(force_text(resp.content),
                             {'status': 'success',
                              'result': 'Dislike was added'})
