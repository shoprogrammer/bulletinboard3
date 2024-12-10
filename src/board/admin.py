from django.contrib import admin
from .models import BoardModel,CommentModel,ReactionModel,FavoriteModel,SortModel,LikeModel

admin.site.register(BoardModel)
admin.site.register(CommentModel)
admin.site.register(ReactionModel)
admin.site.register(FavoriteModel)
admin.site.register(SortModel)
admin.site.register(LikeModel)