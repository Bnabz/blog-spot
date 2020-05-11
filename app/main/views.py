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