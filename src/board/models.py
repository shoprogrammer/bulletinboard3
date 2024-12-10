from django.db import models
from django.contrib.auth.models import User

class BoardModel(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='media/',null=True,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='boards',null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class CommentModel(models.Model):
    board = models.ForeignKey(BoardModel,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')
    image = models.ImageField(upload_to='media/',null=True,blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content
    

class ReactionModel(models.Model):
    board = models.ForeignKey(BoardModel,on_delete=models.CASCADE,related_name='reactions')
    comment = models.ForeignKey(CommentModel,on_delete=models.CASCADE,related_name='reactions')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='reactions')
    content = models.TextField(default='未設定')
    image = models.ImageField(upload_to='media/',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content


#いいね機能
class LikeModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='likes')
    board = models.ForeignKey(BoardModel,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user','board'],name='unique_user_board_like')
        ]
    def __str__(self):
        return f"{self.user.username} liked {self.board}"

class FavoriteModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='favorites')
    board = models.ForeignKey(BoardModel,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        unique_together = ('user','board')

    def __str__(self):
        return self.board.title


# sortしたかしてないか
class SortModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='sorts')
    whichsort = models.BooleanField(default=False)

    def __str__(self):
        return str(self.whichsort)





class Contact(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

