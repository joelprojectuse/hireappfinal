from django.urls import path
from . import views
urlpatterns = [
    path('', views.first_page, name='first_page'),
    path('home', views.home, name="home"),
    path('register', views.register, name="register"),
    path('login', views.login_page, name="login"),
    path('signout', views.signout, name="signout"),
    path('job', views.job, name="job"),
    path('logout', views.logout_page, name="logout"),
    path('profile', views.profile, name="profile"),
    path('update_profile', views.update_profile, name="update_profile"),
    path('hirerprofile', views.hirerprofile, name="hirerprofile"),
    path('hiringform', views.hiringform, name="hiringform"),
    path('completed_view', views.completed_view, name="completed_view"),
    path('hired', views.hired, name="hired"),
    path('add/<int:job_id>/', views.add_to_job, name='add_to_job'),
    path('decline/<int:job_id_remove>/', views.decline, name='decline'),
    path('delete/<int:del_hired_id>/',
         views.delete_hired, name='delete_hired'),
]
