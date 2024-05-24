from django.test import TestCase
from django.utils import timezone
import datetime
from .models import BlogPost


# Create your tests here.
class BlogPostModelTests(TestCase):

    def test_was_published_recently_with_future_date(self):
        time_to_test = timezone.now() + datetime.timedelta(days=30)
        blog_post = BlogPost(pub_date=time_to_test)
        was_published_recently = blog_post.was_published_recently()
        self.assertIs(was_published_recently, False)

    def test_was_published_recently_with_recent_date(self):
        time_to_test = timezone.now() - datetime.timedelta(days=1)
        blog_post = BlogPost(pub_date=time_to_test)
        was_published_recently = blog_post.was_published_recently()
        self.assertIs(was_published_recently, True)

    def test_was_published_recently_with_old_date(self):
        time_to_test = timezone.now() - datetime.timedelta(days=30)
        blog_post = BlogPost(pub_date=time_to_test)
        was_published_recently = blog_post.was_published_recently()
        self.assertIs(was_published_recently, False)

# class Mortgage
#     def 