from django.db import models
from accounts.models import CustomUser

class Category(models.Model):
    '''投稿する写真のカテゴリを管理するモデル
    '''
    #カテゴリ名のフィールド
    title = models.CharField(
        verbose_name='カテゴリ',  #フィールドのタイトル
        max_length=20)
    
    def __str__(self):
        '''オブジェクトを文字列に変換して返す
        
        Returns(str):カテゴリ名
        '''
        return self.title
    
class PhotoPost(models.Model):
    '''投稿されたデータを管理するモデル
    '''
    #CustomUserモデル(のuser_id)とPhotoPostモデルを
    user = models.ForeignKey(
        CustomUser,
        verbose_name='ユーザー',
        on_delete=models.CASCADE
    )   

    category = models.ForeignKey(
        Category,
        verbose_name='カテゴリ',
        on_delete=models.PROTECT
    ) 
    
    title = models.CharField(
        verbose_name='タイトル',
        max_length=200
    )

    comment = models.TextField(
        verbose_name='コメント',
    )

    image1 = models.ImageField(
        verbose_name='イメージ１',
        upload_to='photos'
    )

    image2 = models.ImageField(
        verbose_name='イメージ２',
        upload_to='photos',
        blank=True,
        null=True
    )

    posted_at = models.DateTimeField(
        verbose_name='投稿日時',
        auto_now_add=True
    )

    def __str__(self):

        return self.title

