from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for
)
<<<<<<< HEAD
import requests
from constants import *
from werkzeug.utils import secure_filename
=======
>>>>>>> 1754ce064c766b838b139e75de2185e8a5b72a1b
from . import swarm

bp = Blueprint('main', __name__, url_prefix='')


@bp.route('/feed', methods=('GET', 'POST'))
def feed():
    return render_template('app/feed.html')


@bp.route('/sell', methods=('GET', 'POST'))
#@jwt_required
def sell():
    if request.method == 'POST':
        if 'gallery' in request.form:
            return redirect(url_for('main.gallery'))
        if 'sell' in request.form:
            error = None
            if 'file' not in request.files:
                error = "File is required."
            if 'title' not in request.form:
                error = "Title is required."
<<<<<<< HEAD
            if error is None:
                file = request.files['file']
                title = request.form['title']
                swarm_hash, swarm_hash_blurry = swarm.upload_image_private(file, title)
                print(swarm_hash, swarm_hash_blurry)
=======
            if 'price' not in request.form:
                error = "Price is required."
            if 'duration' not in request.form:
                error = "Duration is required."
            if 'private' not in request.form:
                error = "Private or public is required."
            if error is None:
                file = request.files['file']
                title = request.form['title']
                price = request.form['price']
                duration = int(request.form['duration'])
                private = True if request.form["private"] == 'on' else False
                swarm_hash, swarm_hash_blurry = swarm.upload_image_swarm(file, title)
                print(price, private, duration, swarm_hash, swarm_hash_blurry)
>>>>>>> 1754ce064c766b838b139e75de2185e8a5b72a1b
                return redirect(url_for('main.gallery'))
            flash(error)
    return render_template('app/sell.html')


@bp.route('/account', methods=('GET', 'POST'))
def account():
    user = {"name": "Little Caprice"}
    return render_template('app/account.html', user=user)


@bp.route('/gallery', methods=('GET', 'POST'))
#@jwt_required
def gallery():

    images = [{"title": "Little Caprice", "mime": "image/png", "bytes": swarm.get_base64_image()},
              {"title": "Landscape", "mime": "image/png", "bytes": swarm.get_base64_image()}]
    temp = []
    for x in images:
        mime = x["mime"]
        uri = "data:%s;base64,%s" % (mime, x["bytes"])
        image = {"title": x["title"], "uri": uri}
        temp.append(image)

    return render_template('app/gallery.html', images=temp)
