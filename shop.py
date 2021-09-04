from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from cloudipsp import Api, Checkout
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# БД-Таблиці-Записи
# Таблиця
# id      title    price  info
# створюєм таблицю


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    nalich = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return self.title
        # info = db.Column(db.Text, nullable=False)
        # В терміналі прописуємо Python--> (from prim import db) -->(db.create_all())


@app.route('/')
def jopa():
    # Получаєм обєкти з бази даних
    items = Item.query.order_by(Item.price).all()  # сортуємо за ціною
    return render_template('index.html', data=items)


@app.route('/about')
def lon():
    return render_template('registr.html')


@app.route('/buy/<int:id>')
def item_buy(id):
    item = Item.query.get(id)
    api = Api(merchant_id=1396424,
              secret_key='test')
    checkout = Checkout(api=api)
    data = {"currency": "UAH",
            "amount": str(item.price)+'00'}
    url = checkout.url(data).get('checkout_url')
    return redirect(url)


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == "POST":
        title = request.form['title']
        price = request.form['price']

        item = Item(title=title, price=price)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect('/')
        except:
            return "Виникла помилка"
    else:
        return render_template('create.html')


if __name__ == '__main__':
    app.run(debug=True, port=2550)
