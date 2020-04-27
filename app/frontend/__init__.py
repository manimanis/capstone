import os
from pprint import pprint
from urllib.parse import urlencode

import requests
from flask import Blueprint, request, render_template, session, redirect, \
    url_for, flash
from .. import auth0, ENDPOINTS_BASE_URL
from ..auth import verify_decode_jwt, Auth0User, AUTH0_CLIENT_ID, \
    populate_user_infos, generate_random_picture
from ..models import User, Student, Teacher

main = Blueprint('main', __name__)


PICTURE_HOST = 'https://randomuser.me/api/portraits/lego/'


@main.route('/')
def home():
    user_info = session.get('user_info')
    auth_user = Auth0User(user_info)
    if auth_user.is_authenticated():
        user = User.get_by_username(auth_user.user_id)
        # User should: exist in the database, has permissions and role.
        # if some information is missing than we conclude that this is the
        # first user login
        if (user is None
                or auth_user.picture is None
                or not auth_user.has_permissions()
                or not auth_user.has_role()):
            return redirect('/select_profile')
    return render_template('index.html',
                           auth_user=auth_user,
                           endpoints_url=ENDPOINTS_BASE_URL)


@main.route('/login')
def login():
    return auth0.authorize_redirect(
        redirect_uri=os.environ.get('AUTH0_CALLBACK_URI'),
        audience=os.environ.get('AUTH0_APP_AUDIENCE')
    )


@main.route('/select_profile', methods=['GET', 'POST'])
def select_profile():
    def is_url_image(image_url):
        """Test if the url is for an image"""
        image_formats = ("image/png", "image/jpeg", "image/jpg")
        r = requests.head(image_url)
        if r.headers["content-type"] in image_formats:
            return True
        return False

    user_info = session.get('user_info')
    auth_user = Auth0User(user_info)
    if request.method == 'GET':
        if not auth_user.is_authenticated():
            return redirect('/')
        return render_template('select_profile.html', auth_user=auth_user)
    elif request.method == 'POST':
        role = request.form.get('role')
        fullname = request.form.get('fullname')
        picture = request.form.get('picture')
        is_picture = is_url_image(picture)
        if not role or fullname == '' or not is_picture:
            flash('Incomplete form fill.')
            if not is_picture:
                auth_user.picture = generate_random_picture()
            return render_template('select_profile.html',
                                   auth_user=auth_user,
                                   endpoints_url=ENDPOINTS_BASE_URL)
        auth_user.picture = picture
        auth_user.fullname = fullname
        roles = auth_user.get_roles()
        user = User.get_by_username(auth_user.user_id)
        if user is not None and user.delete():
            user = None
        if user is None:
            if role == 'student':
                user = Student(username=auth_user.user_id,
                               picture=picture,
                               fullname=auth_user.fullname)
            elif role == 'teacher':
                user = Teacher(username=auth_user.user_id,
                               picture=picture,
                               fullname=auth_user.fullname)
            completed = (auth_user.set_role(auth_user.user_id, roles[role])
                         and user.insert())
        else:
            completed = False
        if not completed:
            flash('Cannot setup user account!', 'error')
            return render_template('select_profile.html', auth_user=auth_user,
                                   endpoints_url=ENDPOINTS_BASE_URL)
        else:
            flash('Thank you, your account was setup correctly. '
                  'You can login again.')
            # Update user session
            user_info['user_id_db'] = user.id
            user_info['role'] = role
            user_info['picture'] = picture
            user_info['fullname'] = fullname
            user_info['permissions'] = Auth0User.get_permissions(
                auth_user.user_id)
            session['user_info'] = user_info
            return redirect('/')


@main.route('/logout')
def logout():
    # Clear session stored data
    session.clear()
    # Redirect user to logout endpoint
    params = {
        'returnTo': url_for('main.home', _external=True),
        'client_id': AUTH0_CLIENT_ID
    }
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


@main.route('/callback')
def callback_handling():
    """Callback after successful login"""
    # Collect data about user from three sources:
    # Auth0 token, Auth0 user infos, and local database
    try:
        # Handles response from payload endpoint
        token = auth0.authorize_access_token()
        resp = auth0.get('userinfo')
        infos = resp.json()
        # Populate 'user_info' session var
        session['user_info'] = populate_user_infos(token, infos)
    except:
        return redirect('/logout')

    return redirect('/')


@main.route('/profile')
def show_profile():
    user_info = session.get('user_info')
    auth_user = Auth0User(user_info)
    return render_template('profile.html', auth_user=auth_user,
                           endpoints_url=ENDPOINTS_BASE_URL)
