from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import datetime
from .models import *


class BlogPostModelTests(TestCase):
    '''Simple test cases for behaviour of the BlogPost model.
    '''

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



# def create_question(question_text, days):
#     """
#     Create a question with the given `question_text` and published the
#     given number of `days` offset to now (negative for questions published
#     in the past, positive for questions that have yet to be published).
#     """
#     time = timezone.now() + datetime.timedelta(days=days)
#     return Question.objects.create(question_text=question_text, pub_date=time)


class BlogPostViewTests(TestCase):
    '''Test some views associated with the BlogPost model.
    '''
    def test_no_blogposts(self):
        """
        If no blog posts exist, an appropriate message is displayed.
        """
        # get response object by GET request to blog_list url
        response = self.client.get(reverse("mortgage:blog_list"))

        # assert that a response was successfully received
        self.assertEqual(response.status_code, 200)

        # assert that response contains message produced by blogpost_list.html
        self.assertContains(response, "No posts are available")

        # assert that response has an empty query set
        self.assertQuerySetEqual(response.context["object_list"], [])

    def test_one_past_blogpost(self):
        """
        BlogPost with past pub_date are displayed on the page.
        """
        # need to create a simulated user and log them in based on login an authenticated user
        client = Client()
        user = User.objects.create_user(username='john', password='johnpassword')
        client.login(username='john', password='johnpassword')

        # create a test blog post from a day in the past
        blogpost = BlogPost.objects.create(
            user=user,
            title = 'Test Post',
            text = 'Hello World',
            pub_date = timezone.now() + datetime.timedelta(days=-1)
        )

        # get response and test its contents are as expected
        response = self.client.get(reverse("mortgage:blog_list"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["object_list"], [blogpost])

    def test_two_past_blogposts(self):
        """
        The BlogPost list page can display multiple questions.
        """
        client = Client()
        user = User.objects.create_user(username='john', password='johnpassword')
        client.login(username='john', password='johnpassword')

        blogpost1 = BlogPost.objects.create(
            user=user,
            title = 'Test Post 1',
            text = 'Hello World 1',
            pub_date = timezone.now() + datetime.timedelta(days=-3)
        )
        blogpost2 = BlogPost.objects.create(
            user=user,
            title = 'Test Post 2',
            text = 'Hello World 2',
            pub_date = timezone.now() + datetime.timedelta(days=-2)
        )

        response = self.client.get(reverse("mortgage:blog_list"))
        self.assertQuerySetEqual(
            response.context["object_list"],
            [blogpost2, blogpost1],
        )

    def test_one_future_blogpost(self):
        # need to create a simulated user and log them in based on login an authenticated user
        client = Client()
        user = User.objects.create_user(username='john', password='johnpassword')
        client.login(username='john', password='johnpassword')

        # create a test blog post from two days in the future
        blogpost = BlogPost.objects.create(
            user=user,
            title = 'Test Post',
            text = 'Hello World',
            pub_date = timezone.now() + datetime.timedelta(days=2)
        )

        # get response and test its contents are as expected
        # we expect empty response, since future blog posts not in queryset.
        response = self.client.get(reverse("mortgage:blog_list"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["object_list"], [])

    def test_one_future_and_one_past_blogpost(self):
        client = Client()
        user = User.objects.create_user(username='john', password='johnpassword')
        client.login(username='john', password='johnpassword')
        blogpost1 = BlogPost.objects.create(
            user=user,
            title = 'Test Post 1',
            text = 'Hello World 1',
            pub_date = timezone.now() + datetime.timedelta(days=2)
        )
        blogpost2 = BlogPost.objects.create(
            user=user,
            title = 'Test Post 2',
            text = 'Hello World 2',
            pub_date = timezone.now() + datetime.timedelta(days=-2)
        )
        response = self.client.get(reverse("mortgage:blog_list"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerySetEqual(response.context["object_list"], [blogpost2])
