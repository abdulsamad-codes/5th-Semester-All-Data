# Product price (immutable)
price_a = 500
price_b = price_a
price_b = price_b - 50

if price_a == 500:
    print("Price A unchanged:", price_a)

# Shopping cart (mutable)
cart = ["milk", "bread", "eggs"]
shared_cart = cart.copy() # we created a different copy of shared cart
# so there is no change in the shared copy  
shared_cart.append("juice")

if len(cart) == 4:
    print("BUG: original cart modified!", cart)
else:
    print("BUG Fixed, We have two different carts right now, cart and shared cart")

# Safe copy
cart_a = ["pen", "notebook"]
cart_b = cart_a.copy()
cart_b.append("eraser")

if cart_a == cart_b:
    print("Same items")
if cart_a is cart_b:
    print("Same cart object")
else:
    print("Different cart objects")
