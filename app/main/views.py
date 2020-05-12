from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import UpdateProfile,PostForm,CommentForm
from ..models import User,Post,Comment
from flask_login import login_required, current_user
from .. import db,photos
from datetime import datetime
from ..requests import getQuotes


@main.route('/')
def index():
    quotes = getQuotes()
    posts = Post.query.all()
    return render_template('index.html', quotes=quotes, posts=posts, current_user=current_user)



@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()
    user_id = current_user._get_current_object().id
    profile_posts = Post.query.filter_by(user_id = user_id).all()
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user,profile_posts=profile_posts)



@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))


@main.route("/new_post", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        date_posted = datetime.today()
        author = current_user._get_current_object().username 
        user_id = current_user._get_current_object().id
        post = Post(title=form.title.data, content=form.content.data, author=author,date_posted = date_posted,user_id = user_id)
        post.save()
        return redirect(url_for('main.index'))
    return render_template('new_post.html', title='New Post',
                           form=form, legend='New Post')




@main.route('/comments/<int:post_id>', methods = ['POST','GET'])
@login_required
def comment(post_id):
    form = CommentForm()
    post = Post.query.get(post_id)
    post_comments = Comment.query.filter_by(post_id = post_id).all()
    idb = post.user_id
    ida = current_user._get_current_object().id 
    if ida == idb:
        can_delete = True
    
    if form.validate_on_submit():
        comment = form.comment.data 
        post_id = post_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(comment = comment,user_id = user_id,post_id = post_id)
        new_comment.save_comment()
        return redirect(url_for('.comment', post_id = post_id))
    
    print(ida)
    print(idb)
    return render_template('comments.html', form =form, post = post,post_comments=post_comments,ida = ida, idb = idb,)


@main.route('/delete_comment/<int:id>')
@login_required
def delete_comment(id):
    
    comment = Comment.query.filter_by(id = id).first()
    post_id = comment.post_id
    comment.delete()

    return redirect(url_for('main.comment', post_id = post_id))

