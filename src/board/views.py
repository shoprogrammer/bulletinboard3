from django.shortcuts import render,redirect,get_object_or_404
from .form import BoardForm,SignUpForm,CommentForm,FavoriteForm,ReactionForm,ContactForm,LikeForm
from .models import BoardModel,CommentModel,FavoriteModel,ReactionModel,SortModel,LikeModel
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db import models
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib import messages








#一覧表示
def listboard(request):
    template_name = 'board/boardlist.html'
    user = request.user

    if user.is_authenticated:
    
        boards_query = BoardModel.objects.annotate(is_favorite=Count('favoritemodel',filter=models.Q(favoritemodel__user=user)),
                                                   is_like=Count('likemodel',filter=models.Q(likemodel__user=user)),
                                                   like_count=Count('likemodel')
                                                   ).order_by('-updated_at')
        paginator = Paginator(boards_query,10)
        page_number = request.GET.get('page')
        boards = paginator.get_page(page_number)
        boards_query = user.favorites.count()




    else:
        boards_query = BoardModel.objects.all()
        paginator = Paginator(boards_query,10)
        page_number = request.GET.get('page')
        boards = paginator.get_page(page_number)
    

    for board in boards:
        board.comment_count = board.comments.count()

    return render(request,template_name,{"boards":boards,"boards_query":boards_query})


#board作成のフォーム

def newboard(request):
    template_name = "board/boardnew.html"
    form = BoardForm()
    return render(request,template_name,{"form":form})


#post時のboard作成
@login_required
def createboard(request):
    template_name = "board/boardlist.html"
   
    if request.POST:
        form = BoardForm(request.POST,request.FILES)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            messages.success(request,"成功しました")   
            return redirect('board-list')
        else:
            messages.error(request,'失敗しました')
    else:
        form = BoardForm()

    return render(request,template_name,{'form':form})

#boardの詳細--------------------------------------------------
@login_required
def deteilboard(request,pk):
    template_name = "board/boarddetail.html"
    board = BoardModel.objects.get(pk=pk)
    comments_query = CommentModel.objects.filter(board=pk).order_by('-created_at')
    comment_form = CommentForm()
    #ページネーター 
    paginator = Paginator(comments_query,5)
    page_number = request.GET.get('page')
    comments = paginator.get_page(page_number)
    comments_query = comments_query.count()

    
    return render(request,template_name,{"board":board,"comments":comments,"comment_form":comment_form,"comments_query":comments_query})
    
def editboard(request,pk):
    template_name = "board/boardedit.html"
    board = BoardModel.objects.get(pk=pk)
    form = BoardForm(instance=board)
    return render(request,template_name,{"board":board,"form":form})




def updateboard(request,pk):
    template_name = "board/boardedit.html"
    board = BoardModel.objects.get(pk=pk)
    if request.POST:
        form = BoardForm(request.POST,request.FILES,instance=board)
        if form.is_valid():
            form.save()
            return redirect('detail-board',pk=pk)
    else:
        form = BoardForm(instance=board)

    return render(request,template_name,{"form":form,"board":board})

def deleteboard(request,pk):
    board = BoardModel.objects.get(pk=pk)
    if request.POST:
        board.delete()
        return redirect("board-list")
    return redirect("board-list")

#自分のボードです
def myboard(request):
    template_name = 'board/myboard.html'
    user = request.user
    boards = user.boards.all()
    return render(request,template_name,{'boards':boards})


def createcomment(request,pk):
    if request.POST:
        comment_form = CommentForm(request.POST,request.FILES)
        if comment_form.is_valid():
            comment_form.instance.user = request.user
            comment_form.instance.board_id = pk
            comment_form.save()
    return redirect('detail-board',pk=pk)

def deletecomment(request,board_pk,comment_pk):
    comment = get_object_or_404(CommentModel,pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('detail-board',pk=board_pk)


def editcomment(request,board_pk,comment_pk):
    template_name = "comment/commentedit.html"
    comment = get_object_or_404(CommentModel,pk=comment_pk,)
    board = get_object_or_404(BoardModel,pk=board_pk)
    form = CommentForm(instance=comment)
    return render(request,template_name,{"board":board,"form":form,"comment":comment})




def updatecomment(request,board_pk,comment_pk):
    template_name = "comment/commentedit.html"
    comment = get_object_or_404(CommentModel,pk=comment_pk)
    board = get_object_or_404(BoardModel,pk=board_pk)

    if request.POST:
        form = CommentForm(request.POST,request.FILES,instance=comment)
        if form.is_valid():
         form.save()
         return redirect('detail-board',pk=board_pk)
    else:
        form = CommentForm(instance=comment)

    return render(request,template_name,{"form":form,"comment":comment,"board":board})




#reaction機能----------------------------------------------------------------

def detailreaction(request,board_pk,comment_pk):
    template_name = 'reaction/reactiondetail.html'
    comment = get_object_or_404(CommentModel,pk=comment_pk)
    board = get_object_or_404(BoardModel,pk=board_pk)
    reactions = ReactionModel.objects.filter(board=board_pk,comment=comment_pk)
    return render(request,template_name,{"comment":comment,"board":board,"reactions":reactions})



def editreaction(request,board_pk,comment_pk,reaction_pk):
    template_name = 'reaction/reactionedit.html'
    comment = get_object_or_404(CommentModel,pk=comment_pk)
    board = get_object_or_404(BoardModel,pk=board_pk)
    reaction = get_object_or_404(ReactionModel,pk=reaction_pk)
    reaction_form = ReactionForm(instance=reaction)
    return render(request,template_name,{"comment":comment,"board":board,"reaction":reaction,"reaction_form":reaction_form})






def createreaction(request,board_pk,comment_pk):
    template_name = "reaction/reactioncreate.html"
    board = get_object_or_404(BoardModel,pk=board_pk)
    comment = get_object_or_404(CommentModel,pk=comment_pk)
    if request.POST:
        reaction_form = ReactionForm(request.POST,request.FILES)
        if reaction_form.is_valid():
            reaction_form.instance.user = request.user
            reaction_form.instance.board_id = board_pk
            reaction_form.instance.comment_id = comment_pk
            reaction_form.save()
            return redirect('detail-reaction',board_pk=board_pk,comment_pk=comment_pk)
    else:
        reaction_form = ReactionForm()

    return render(request,template_name,{'reaction_form':reaction_form,'board':board,'comment':comment})

    
def deletereaction(request,board_pk,comment_pk,reaction_pk):
    template_name = "reaction/reactiondetail.html"
    board = BoardModel.objects.get(pk=board_pk)
    comment = CommentModel.objects.get(board=board_pk,pk=comment_pk)
    reaction = ReactionModel.objects.get(board=board_pk,comment=comment_pk,pk=reaction_pk)
    if request.POST:
        reaction.delete()
        return redirect('detail-reaction',board_pk=board_pk,comment_pk=comment_pk)
    return render(request,template_name,{'board':board,'comment':comment,'reaction':reaction})



def updatereaction(request,board_pk,comment_pk,reaction_pk):
    template_name = "reaction/reactionedit.html"

    board = BoardModel.objects.get(pk=board_pk)
    comment = CommentModel.objects.get(board=board_pk,pk=comment_pk)
    reaction = get_object_or_404(ReactionModel,pk=reaction_pk)
    if request.POST:
        reaction_form = ReactionForm(request.POST,request.FILES,instance=reaction)
        if reaction_form.is_valid():
            reaction_form.save()
            return redirect('detail-reaction',board.pk,comment.pk)

    else:
        reaction_form = ReactionForm(instance=reaction)

    return render(request,template_name,{"board":board,"comment":comment,"reaction":reaction})







@login_required
def board_search(request):
    query = request.GET.get('query')
    template_name = "board/boardlist.html"
    search_type = request.GET.get('search_type')
    boards = BoardModel.objects.all()

    if search_type == 'partial':
        boards = boards.filter(title__icontains=query)
        boards_count = boards.count()
    elif search_type == 'prefix':
        boards = boards.filter(title__startswith=query)
        boards_count = boards.count()
    elif search_type == 'suffix':
        boards = boards.filter(title__endswith=query)
        boards_count = boards.count()


    return render(request,template_name,{"boards":boards,"boards_count":boards_count})

#ボードをコメント数でソートする
@login_required
def board_commentsort(request):
    sort_by = request.GET.get('sort')
    ddirection = request.GET.get('ddirection')
    boards = BoardModel.objects.annotate(comment_count=Count('comments'))

    #sortのデータを受け取りうまくif文に組み込む
    # 一番最初のデータ取得
    sorts = SortModel.objects.filter(user=request.user).first()
    print(sorts)




    if ddirection == 'aasc':
        next_ddirection = 'ddesc'
    else:
        next_ddirection = 'aasc'

    if sort_by:
        if ddirection == 'ddesc':
            boards = boards.order_by(f'-{sort_by}')
        else:
            boards = boards.order_by(sort_by)
    else:
        boards = boards
    
    template_name = "board/boardlist.html"
    context = {

        'boards':boards,
        'next_ddirection':next_ddirection,
        'sort_by':sort_by,
        'ddirection':ddirection,

    }

    return render(request,template_name,context)






@login_required
def board_sort(request):
  
    

    result = False

     #GPT post True or False
    sort_instance = SortModel.objects.filter(user=request.user).first()
    
    if sort_instance is None:
        sort_instance = SortModel.objects.create(user=request.user)

    if request.POST:
        
        sort_instance.whichsort = not sort_instance.whichsort
        
        sort_instance.save()
        result = sort_instance
        
    
    
        if sort_instance.whichsort == True:
            boards = BoardModel.objects.all().order_by('-created_at')
            result = False
        elif sort_instance.whichsort == False:
            boards = BoardModel.objects.all().order_by('created_at')
            result = True
    else:
        boards = BoardModel.objects.all() 
        
       

   



 

    for board in boards:
        board.comment_count = board.comments.count()

    template_name = "board/boardlist.html"
   

    context = {

        'boards':boards,
         'result':result,
        'sort_instance':sort_instance,
        'board':board,
    }
    return render(request,template_name,context)


@login_required
def myboard_sort(request):
    sort_by = request.GET.get('sort')
    direction = request.GET.get('direction')
    # boards = BoardModel.objects.all()

    user = request.user
    if direction == 'asc':
        next_direction = 'desc'
    else:
        next_direction = 'asc'

    if sort_by:
        if direction == 'desc':
            boards = user.boards.all().order_by(f'-{sort_by}')
        else:
            boards = user.boards.all().order_by(sort_by)
    else:
        boards = user.boards.all()

    template_name = "board/myboard.html"

    context = {

        'boards':boards,
        'sort_by':sort_by,
        'direction':direction,
        'next_direction':next_direction,


    }
    return render(request,template_name,context)
@login_required
def favorite_sort(request):
    template_name = "favorite/favoritedisplay.html"
    sort_by = request.GET.get('sort')
    direction = request.GET.get('direction')

    user = request.user
    if direction == 'asc':
        next_direction = 'desc'
    else:
        next_direction = 'asc'

    if sort_by:
        if direction == 'desc':
            boards = user.favorites.all().order_by(f'-{sort_by}')
        else:
            boards = user.favorites.all().order_by(sort_by)
    else:
        boards = user.favorites.all()

    context = {

        'boards':boards,
        'sort_by':sort_by,
        'direction':direction,
        'next_direction':next_direction,


    }
    return render(request,template_name,context)












#作成時間によってコメントの順番を変更する
@login_required
def comment_sort(request,pk):
    sort_by = request.GET.get('sort')
    direction = request.GET.get('direction')
    template_name = "board/boarddetail.html"
    board = BoardModel.objects.get(pk=pk)
    comment_form = CommentForm()

    if direction == 'asc':
        next_direction = 'desc'
    else:
        next_direction = 'asc'
    
    if sort_by == 'created_at':
        if direction == 'desc':
            # comments = CommentModel.objects.get(pk=pk).order_by('-created_at')
            comments = CommentModel.objects.filter(board=pk).order_by('-created_at')
        else:
           
            comments = CommentModel.objects.filter(board=pk).order_by('created_at')
            # comments = CommentModel.objects.get(pk=pk).order_by('created_at')
        
    else:
        # comments = CommentModel.objects.get(pk=pk)
        comments = CommentModel.objects.filter(board=pk)

    ctx = {
        "comments":comments,
        "sort_by":sort_by,
        "next_direction":next_direction,
        "direction":direction,
        "board":board,
        "comment_form":comment_form }


    


    return render(request,template_name,ctx)

@login_required
def new_sort(request):
    template_name = "board/boardlist.html"
    sort_by = request.GET.get('sort')
    direction = request.GET.get('direction')
    # boards = BoardModel.objects.all()
    boards = BoardModel.objects.annotate(comment_count=Count('comments'))
    for board in boards:
        board.comment_count = board.comments.count()

    if direction == 'asc':
        next_direction = 'desc'
    else:
        next_direction = 'asc'

    if sort_by:
        if direction == 'desc':
            boards = boards.order_by('-updated_at')
        else:
            boards = boards.order_by('updated_at')
    else:
        boards = boards

    context = {
        'boards':boards,
        'next_direction':next_direction,
        'sort_by':sort_by,
        'direction':direction,
        'board':board,


    }
    return render(request,template_name,context)



#いいね機能
def add_like(request):
    if request.POST:
        form = LikeForm(request.POST)
        if form.is_valid():
            user=request.user
            board = form.cleaned_data['board']

            like_exists = LikeModel.objects.filter(user=user,board=board).exists()
            if not like_exists:
                form.instance.user =user
                form.save()

       
            return redirect('board-list')
    return redirect('board-list')

def remove_like(request):
    if request.POST:
        like = LikeModel.objects.get(user=request.user,board=request.POST.get('board'))
        like.delete()
        return redirect('board-list')
    return redirect('board-list')








#お気に入り
def display_favorite(request):
    template_name="favorite/favoritedisplay.html"
    user = request.user
    # boards = FavoriteModel.objects.filter(user=user)
    boards = user.favorites.all()
    boards_query = user.favorites.count()
    print(boards_query)
    return render(request,template_name,{'boards':boards,'boards_query':boards_query})




def add_favorite(request):
    if request.POST:
        form = FavoriteForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('board-list')
    return redirect('board-list')

def remove_favorite(request):
    if request.POST:
        favorite = FavoriteModel.objects.get(user=request.user,board=request.POST.get('board'))
        favorite.delete()
        return redirect('board-list')
    return redirect('board-list')

#myfavorite用のremove
def remove_myfavorite(request):
    # template_name="favorite/favoritedisplay.html"
    if request.POST:
        favorite = FavoriteModel.objects.get(user=request.user,board=request.POST.get('board'))
        favorite.delete()
    return redirect('display_favorite')



#お問合せフォーム
def contact(request):
    template_name ='contact/contact.html'
    form = ContactForm(request.POST)
    if form.is_valid():
        contact=form.save()

        #ユーザーへのメール
        user_subject = 'お問い合わせを受け付けました'
        user_message = 'お問い合わせ内容:¥n¥n{}'.format(contact.message)
        send_mail(user_subject,user_message,settings.EMAIL_HOST_USER,[contact.email])

        #運営者へのメール
        admin_subject = 'お問合せがありました'
        admin_message = 'お問合せ内容:¥n¥n{}'.format(contact.message)
        send_mail(admin_subject,admin_message,settings.EMAIL_HOST_USER,[settings.EMIAL_HOST_USER])
        return redirect('contact_success')

    else:
        form = ContactForm()



    return render(request,template_name,{'form':form})


def contact_success(request):
    template_name = "contact/contact_success.html"
    return render(request,template_name)




def comment_search(request,pk):
    query = request.GET.get('query')
    template_name = "board/boarddetail.html"
    search_type = request.GET.get('search_type')
    board = BoardModel.objects.get(pk=pk)
    comments = CommentModel.objects.filter(board=board)
    print(comments)
    if search_type == 'partial':
        comments = comments.filter(content__icontains=query)
    elif search_type == 'prefix':
        comments = comments.filter(content__startswith=query)
    elif search_type == 'suffix':
        comments = comments.filter(content__endswith=query)

    return render(request,template_name,{"comments":comments,"board":board})

    


    # if query:
    #     comments = CommentModel.objects.filter(board=pk,content__icontains=query)
    # else:
    #     comments = CommentModel.objects.filter(board=pk).order_by('-update_at')

    return render(request,template_name,{"comments":comments,"board":board})

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


def logout_view(request):
    logout(request)
    return redirect('board-list')

def signup(request):
    if request.POST:
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    
    else:
        form = SignUpForm()
    
    return render(request,'registration/signup.html',{'form':form})

def profile(request):
    user = request.user
    return render(request,'accounts/profile.html',{'user':user})