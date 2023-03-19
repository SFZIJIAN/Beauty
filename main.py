from flask import Flask, render_template, redirect

from beauty import get_cards, get_tags

app = Flask(__name__, static_folder='/')


@app.route('/')
def index():
    return redirect('/tags')


@app.route('/tags')
def list_tags():
    return render_template('tags.html', title='Tags', tags=get_tags())


@app.route('/cards/<tag>')
def list_cards(tag):
    title, cards = get_cards(tag)
    return render_template('cards.html', title=title, cards=cards)


@app.route('/images/<tag>/<card>')
def list_images(tag, card):
    return f'Tag={tag}, Card={card}'


if __name__ == '__main__':
    app.run(debug=True)
