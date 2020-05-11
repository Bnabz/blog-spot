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