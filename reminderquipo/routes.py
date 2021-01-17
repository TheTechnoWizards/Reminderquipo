from flask import render_template, url_for, flash, redirect, request, abort
from reminderquipo import app, db, bcrypt
from reminderquipo.models import User, Post
from reminderquipo.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flask_login import login_user, current_user, logout_user, login_required
from reminderquipo.email import send_email
from datetime import *

# posts = [
# {
#     "author": 'Shobhit',
#     "title" : 'Blog post 1',
#     "content" : 'content1',
#     "date" : 'Jan 14',
# },
# {
#     "author": 'Corey',
#     "title" : 'Blog post 2',
#     "content" : 'content2',
#     "date" : 'Jan 14',
# }
# ]


@app.route('/')
@app.route('/home')
def home():
    if current_user.is_authenticated:
        posts = Post.query.filter_by(author=current_user).all()
        return render_template('home.html', posts = posts, n_posts=len(posts))
    else:
        image_file1 = url_for('static', filename='images/bf.jpg')    
        image_file2 = url_for('static', filename='images/bf1.jpg')    
        image_file3 = url_for('static', filename='images/alarm.jpg')    
        image_file4 = url_for('static', filename='images/assi.jpg')    
        return render_template('home_def.html', im1 = image_file1, im2 = image_file2,
                                im3 = image_file3, im4 = image_file4)
    


@app.route('/about')
def about():
    return render_template('about.html', title = "About")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title = 'Register', form = form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        # if form.email.data == 'admin@blog.com' and form.password.data == 'password':
        #     flash("You have been logged in!", "success")
        #     return redirect(url_for('home'))
        # else:
        #     flash("Login Unsuccesful. Please check username and password", "danger")
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login Unsuccesful. Please check email and password", "danger")
        
    return render_template('login.html', title = 'Login', form = form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    pass


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data: 
            pass
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                             image_file = image_file, form = form)


@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # print(form.date_submission.data.date)
        post = Post(title=form.title.data, content=form.content.data, author=current_user, date_submission=form.date_submission.data)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created', 'success')

        

        subject = f"Assignment due on {post.date_submission}"
        body = f"Greetings {current_user.username},\nYou have an assignment due on {post.date_submission} for {post.title}.\nDetails:\n {post.content}"
        send_email(current_user.email, 
                    subject=subject, 
                    body=body)
        
        return redirect(url_for('home'))
    # print(form.date_submission.data)

    return render_template('create_post.html', title='Add Assignment', form=form, legend='Add Assignment')


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post )

@app.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.date_submission=form.date_submission.data
        db.session.commit()
        flash('Your assignment has been updated', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Assignment', 
                            form=form, legend='Update Assignment')


@app.route('/post/<int:post_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your assignment has been deleted', 'success')
    return redirect(url_for('home'))
