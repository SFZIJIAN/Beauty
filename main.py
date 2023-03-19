from flask import Flask, render_template, redirect

from beauty import get_cards, get_tags, get_images

app = Flask(__name__, static_folder='/',)


@app.route('/')
def index():
    return redirect('/tags')


@app.route('/tags')
def list_tags():
    return render_template('tags.html', title='Tags', tags=get_tags())


@app.route('/cards/<tag>/<page>')
def list_cards(tag, page):
    page = int(page)
    assert page > 0
    title, count, cards = get_cards(tag, page)
    return render_template('cards.html', title=title, cards=cards,
                           page=page,
                           next=f'/cards/{tag}/{page + 1}' if page < count else None,
                           prev=f'/cards/{tag}/{page - 1}' if page != 1 else None)


@app.route('/images/<tag>/<card>')
def list_images(tag, card):
    title, images = get_images(tag, card)
    return render_template('images.html', title=title, images=images)


if __name__ == '__main__':
    app.run(debug=False)
