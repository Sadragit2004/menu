from . import views


from django.urls import path

app_name = 'main'

urlpatterns = [


    path('',views.main,name='index'),
    path('content/', views.main_content_view, name='block'),
    path('section1/', views.section1_view, name='section1'),
    path('restaurants/latest/', views.LatestRestaurantsView.as_view(), name='latest_restaurants'),
    path('restaurants/all/', views.AllRestaurantsView.as_view(), name='all_restaurants'),
    path('api/restaurants/load-more/', views.load_more_restaurants, name='load_more_restaurants'),
    path('faq/',views.faq,name='faq'),
    path('course/',views.active_courses,name='course')


]