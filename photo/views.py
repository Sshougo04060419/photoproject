from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render
# django.views.genericからTemplateViewをインポート
from django.views.generic import TemplateView, ListView

# django.views.genericからCreateViewをインポート
from django.views.generic import CreateView
# django.views.genericからreverse_lazy
from django.urls import reverse_lazy
# formsモジュールからPhotoPostFormをインポート
from .forms import PhotoPostForm
# method_decoratorをインポート
from django.utils.decorators import method_decorator
# login_requiredをインポート
from django.contrib.auth.decorators import login_required
# modelsモジュールからモデルPhotoPostをインポート
from .models import PhotoPost

class IndexView(TemplateView):
    '''トップページのビュー
    '''
    # index.htmlをレンダリングする
    template_name ='index.html'
    # モデルBlogPostのオブジェクトにorder_by()を適用して
    # 投稿日時の降順で並び替える
    # queryset = PhotoPost.objects.order_by('-posted_at')

# デコレーターによりCreatePhotoViewへのアクセスはログインユーザーに限定される
# ログイン状態でなければsettings.pyのLOGIN_URLにリダイレクトされる
@method_decorator(login_required, name='dispatch')
class CreatePhotoView(CreateView):
    '''写真投稿ページへのビュー
    
    PhotoPostFormで定義されているモデルとフィールドと連携して
    投稿データをデータベースに登録する
    
    Attibutes:
       form_class:モデルとフィールドが登録されたフォームクラス
       template_name:レンダリングするテンプレート
       success_url:データベースへの登録完了後のリダイレクト先
       '''
    
    
class PostSuccessView(TemplateView):
    '''投稿完了ページのビュー
    
    Attributes:
      template_name:レンダリングするテンプレート
      '''
    # index.htmlをレンダリングする
    template_name = 'post_success.html'


    # form.pyのPhotoPostFormをフォームクラスとして登録
    from_class = PhotoPostForm
    # レンダリングするテンプレート
    template_name = "post_photo.html"
    # フォームデータ登録完了後のリダイレクト先
    success_url = reverse_lazy('photo:post_done')

    def form_valid(self, form):
        '''CreatePhotoViewクラスのform_valid()をオーバーライド
        
        フォームのバリデーションを通過したときに呼ばれる
        フォームデータの登録をここで行う
        
        parameters:
          from(django.forms.Form):
            form_classに格納されているPhotoPostFormオブジェクト
        Return:
          HttpResponseRedirectオブジェクト:
                スーパークラスのform_valid()の戻り値を返すことで
                success_urlで設定されているURLにリダイレクトされる
                '''
        # commit=FalseにしてPOSTされたデータを取得
        postdata = form.save(commit=False)
        # 投稿ユーザーのidを取得してモデルのuserフィールドに格納
        postdata.user = self.request.user
        # 投稿データをデータベースに登録
        postdata.save()
        #　戻り値はスーパークラスのform_valid()の戻り値(HttpResponseRedirect)
        return super().form_valid(form)