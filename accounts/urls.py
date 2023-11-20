from django.urls import path
# viewsモジュールをインポート
from . import views

# URLパターンを登録するための変数
app_name = 'accounts'
urlpatterns = [
    path('signup/',
         views.SignUpView.as_view(),
         name='signup'),

    path('signup_success/',
         views.SignUpSuccessView.as_view(),
         name='signup\success'),     
]