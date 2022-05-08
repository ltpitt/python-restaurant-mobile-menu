from flask import Flask, render_template, request, redirect, url_for, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurant')
@app.route('/restaurants')
def show_restaurants():
    """
    Show all the restaurants into the db
    :return:
    """
    restaurants = session.query(Restaurant).order_by(Restaurant.name).all()
    return render_template('restaurants.html', restaurants=restaurants)


@app.route('/restaurant/new', methods=['GET', 'POST'])
def new_restaurant():
    """
    Show all the restaurants into the db
    :return:
    """
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['restaurant-name'])
        session.add(newRestaurant)
        session.commit()
        return redirect(url_for('show_restaurants'))
    else:
        return render_template('newRestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    """
    Show all the restaurants into the db
    :return:
    """
    editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['restaurant-name']:
            editedRestaurant.name = request.form['restaurant-name']
        session.add(editedRestaurant)
        session.commit()
        return redirect(url_for('show_restaurants'))
    else:
        return render_template('editRestaurant.html', restaurant=editedRestaurant)


@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def delete_restaurant(restaurant_id):
    """
    Show all the restaurants into the db
    :return:
    """
    deleteRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(deleteRestaurant)
        session.commit()
        return redirect(url_for('show_restaurants'))
    else:
        return render_template('deleteRestaurant.html', restaurant=deleteRestaurant)


@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def show_menu(restaurant_id):
    """
    Show all the restaurants into the db
    :return:
    """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id)
    return render_template(
        'menu.html', restaurant=restaurant, items=items)


@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
    """
    Show all the restaurants into the db
    :return:
    """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['item-name'], description=request.form[
            'item-description'], price=request.form['item-price'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        return redirect(url_for('show_menu', restaurant_id=restaurant.id))
    else:
        return render_template('newMenuItem.html', restaurant=restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_id):
    """
    Show all the restaurants into the db
    :return:
    """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['item-name']:
            editedItem.name = request.form['item-name']
        if request.form['item-description']:
            editedItem.description = request.form['item-description']
        if request.form['item-price']:
            editedItem.price = request.form['item-price']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('show_menu', restaurant_id=restaurant.id))
    else:
        return render_template('editMenuItem.html', restaurant=restaurant, item=editedItem)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, menu_id):
    """
    Show all the restaurants into the db
    :return:
    """
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    deleteItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        return redirect(url_for('show_menu', restaurant_id=restaurant.id))
    else:
        return render_template('deleteMenuItem.html', restaurant=restaurant, item=deleteItem)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
