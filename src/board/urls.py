from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    



    #ボード
    path("boardlist/",views.listboard,name='board-list'),
    path("boardnew/",views.newboard,name="new-board"),
    path("boardcreate/",views.createboard,name="create-board"),
    path("boarddetail/<int:pk>/",views.deteilboard,name="detail-board"),
    path("boardedit/<int:pk>/",views.editboard,name="edit-board"),
    path("boardupdate/<int:pk>/",views.updateboard,name="update-board"),
    path("boarddelete/<int:pk>/",views.deleteboard,name="delete-board"),
    path("myboards/",views.myboard,name="my-board"),

    #コメント
    path("commentcreate/<int:pk>/",views.createcomment,name="create-comment"),
    path("commentcreate/<int:board_pk>/delete/<int:comment_pk>/",views.deletecomment,name="delete-comment"),
    path("commentedit/<int:board_pk>/edit/<int:comment_pk>/",views.editcomment,name="edit-comment"),
    path("commentupdate/<int:board_pk>/update/<int:comment_pk>/",views.updatecomment,name="update-comment"),

    #リアクション
    path("reaction/<int:board_pk>/detail/<int:comment_pk>/",views.detailreaction,name="detail-reaction"),
    path('reaction/<int:board_pk>/create/<int:comment_pk>/',views.createreaction,name="create-reaction"),
    path("reaction/<int:board_pk>/edit/<int:comment_pk>/edit/<int:reaction_pk>",views.editreaction,name="edit-reaction"),
    path('reaction/<int:board_pk>/delete/<int:comment_pk>/delete/<int:reaction_pk>/',views.deletereaction,name="delete-reaction"),
    path('reaction/<int:board_pk>/update/<int:comment_pk>/update/<int:reaction_pk>/',views.updatereaction,name="update-reaction"),

    #検索機能
    path('boardsearch/',views.board_search,name="search-board"),
    path('commentsearch/<int:pk>/',views.comment_search,name="search-comment"),

    #並び替え機能
    path('sort/',views.board_sort,name='sort'),
    path('mysort/',views.myboard_sort,name='my-sort'),
    path('commentsort/<int:pk>/',views.comment_sort,name='sort-comment'),
    path('favoritesort/',views.favorite_sort,name='favorite-sort'),
    path('boardcommentsort/',views.board_commentsort,name='board-commentsort'),
    path('newsort/',views.new_sort,name='new-sort'),

    #お気に入り機能
    path('add_favorite/',views.add_favorite,name='add_favorite'),
    path('remove_favorite/',views.remove_favorite,name='remove_favorite'),
    path('display_favorite/',views.display_favorite,name='display_favorite'),
    path('remove_myfavorite/',views.remove_myfavorite,name='remove_myfavorite'),

    #いいね機能
    path('add_like/',views.add_like,name='add_like'),
    path('remove_like/',views.remove_like,name='remove_like'),


    #お問合せフォーム
    path('contact/',views.contact,name='contact'),
    # path('contact/success/',views.contact_success,name='contact_success'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
