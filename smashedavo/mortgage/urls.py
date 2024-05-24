from django.urls import path
from . import views
from .views import BlogPostListView, BlogPostDetailView, LoanListView

app_name = "mortgage"
urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('blog/', BlogPostListView.as_view(), name='blog_list'),
    path('blog/create', views.blog_create, name='blog_create'),
    path('blog/<int:blogpost_id>/delete', views.blog_delete, name='blog_delete'),
    path('blog/<int:blogpost_id>/edit', views.blog_edit, name='blog_edit'),
    path('blog/<int:pk>/', BlogPostDetailView.as_view(), name='blog_detail'),
    path('loans/', LoanListView.as_view(), name='loan_list'),
    path('loans/create/', views.loan_create, name='loan_create'),
    path('loans/<int:loan_id>/delete', views.loan_delete, name='loan_delete'),
    path('loans/<int:loan_id>/edit', views.loan_edit, name='loan_edit'),
]