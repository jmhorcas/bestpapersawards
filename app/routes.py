from flask import redirect, url_for, current_app


@current_app.route('/about')
def about():
    return redirect(url_for('about'))