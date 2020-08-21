import itertools

max_price = 30
for item, price in zip(itertools.product(main_courses, desserts, drinks), itertools.product(price_main_courses, price_desserts, price_drinks)):
    course, dessert, drink = item
    if sum(price) <= max_price:
        print(f'{course} {dessert} {drink} {sum(price)}')
