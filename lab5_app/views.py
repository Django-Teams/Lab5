import lab5_app.consts as consts
import lab5_app.clearly_not_a_db as not_db

from sys import maxsize
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods

# Create your views here.

def index(req):
    return redirect("/home")

def home(req):
    return render(req, "lab5_app/home.html", {})

def contacts(req):
    return render(req, "lab5_app/contacts.html", {})

def shop(req):
    ctx = {
        "dishes": zip(range(len(not_db.dishes)), not_db.dishes)
    }
    return render(req, "lab5_app/shop.html", ctx)

def shop_item_dish(req, dish_id:int):
    ingredients = not_db.ingredients
    
    dish = not_db.dishes[dish_id]
    curr_ingredients = []
    max_dishes = maxsize
    cost_per_dish = 0
    
    # calc each dish's cost
    for ingredient in dish["recipe"].keys():
        curr_ingredients.append(ingredients[ingredient])
        
        # max portions not counting existing orders
        possible_portions = ingredients[ingredient]["amount"] // dish["recipe"][ingredient]
        # sustract amount of currently made orders
        for order in not_db.current_orders:
            if ingredient in order[0]["recipe"].keys():
                possible_portions -= order[1]
        if max_dishes > possible_portions:
            max_dishes = possible_portions
        
        cost_per_dish += dish["recipe"][ingredient] * ingredients[ingredient]["price"]
    
    ctx = {
        "dish": dish,
        "dish_id": dish_id,
        "ingredients": curr_ingredients,
        "max_dishes": max_dishes,
        "cost_per_dish": cost_per_dish
    }
    return render(req, "lab5_app/item.html", ctx)

def shop_item_add(req):
    dish_id = int(req.GET["id"])
    amount = int(req.GET["amount"])
    not_db.current_orders.append([not_db.dishes[dish_id], amount])
    return redirect("/shop")

def cart(req):
    curr_orders = not_db.current_orders
    ingredients = not_db.ingredients
    total_cost = 0
    # calc total cost
    for order in curr_orders:
        recipe = order[0]["recipe"]
        ingredient_cost = 0
        for k in recipe.keys():
            cost = ingredients[k]["price"]
            amount = recipe[k]
            ingredient_cost += round(amount * cost * consts.NAVAR, 2)
        ingredient_cost *= order[1]
        total_cost += ingredient_cost
        # order[2] = ingredient_cost
        order.append(ingredient_cost)
    
    ctx = {
        "curr_orders": zip(range(len(curr_orders)), curr_orders),
        "total_cost": round(total_cost, 2)
    }
    return render(req, "lab5_app/cart.html", ctx)

@require_http_methods(["POST"])
def order_del(req):
    body_unicode = req.body.decode('utf-8')
    if "value=" in body_unicode:
        id = int(body_unicode[6:])
        del not_db.current_orders[id]
        return HttpResponse("")