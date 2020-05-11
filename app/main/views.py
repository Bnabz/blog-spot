from flask import render_template,request,redirect,url_for,abort
from . import main
from .forms import UpdateProfile,PostForm,CommentForm
from ..models import User,Post,Comment,Quotes
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
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        post.save()
        return redirect(url_for('main.index'))
    return render_template('new_post.html', title='New Post',
                           form=form, legend='New Post')