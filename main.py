'''
Best Buy
A program that lists the products of a store and makes orders
'''

from store import Store
from products import (Product, NonStockedProduct, LimitedProduct,
                      PercentageDiscount, SecondHalfPrice, BuyTwoGetOneFree)


def print_all_products(store):
    '''
    prints all products in the store that are active.
    :param store: the store that has the products
    '''
    print(6 * "-")
    products_list = store.get_all_products()
    if len(products_list) == 0:
        print("No products in stock")
    else:
        i = 1
        for product in products_list:
            print(f'{i}. {product.show()}')
            i += 1
    print(6 * "-")


def create_shopping_list(store):
    '''
    Creates the Shopping List and makes the order
    :param store: the store we order to
    '''
    print_all_products(store)
    if store.get_total_quantity() == 0:
        return
    shopping_list = []
    print('When you want to finish order, enter empty text.')
    while True:
        choice = input('Which product # do you want? ')
        if choice == '':
            break
        try:
            product_index = int(choice) - 1
            while True:
                amount = int(input("What amount do you want? "))
                if amount > 0:
                    break
                print("Invalid amount")
        except ValueError:
            print("Error adding product!")
        else:
            active_products = store.get_all_products()
            if 0 <= product_index < len(active_products):
                product_to_add =  active_products[product_index]
                if isinstance(product_to_add, NonStockedProduct) or product_to_add.get_quantity() >= amount:
                    if isinstance(product_to_add, LimitedProduct) and amount > product_to_add.maximum:
                        print(f"Cannot buy more than {product_to_add.maximum} items at once")
                    else:
                        shopping_list.append(
                            (active_products[product_index], amount)
                        )
                        print("Product added to Shopping list!\n")
                else:
                    print("Order quantity is larger than what exists."
                          "Product not added to Shopping list!\n")
            else:
                print("Error adding product!")
    total = store.order(shopping_list)
    if total > 0:
        print(f'Order made! Total payment: ${total}')
    else:
        print("No order has been made")



def start(store):
    '''
     Shows the user the application menu and executes his choice
    :param store: the store the user is shopping at
    :return: user's choice
    '''
    while True:
        choice = input('\n   Store Menu\n'
                   '   ----------\n'
                   '1. List all products in store\n'
                   '2. Show total amount in store\n'
                   '3. Make an order\n'
                   '4. Quit\n'
                   'Please choose a number: ')
        if choice in ['1', '2', '3', '4']:
            break
        print("Error with your choice! Try again!")
    if choice == '1':
        print_all_products(store)
    if choice == '2':
        print(f'Total of {store.get_total_quantity()} items in store')
    if choice == '3':
        create_shopping_list(store)
    if choice == "4":
        return choice


def main():
    '''
    main function, sets up initial stock of inventory,
    creates shop and start the program flow
    '''
    # setup initial stock of inventory
    product_list = [
        Product("MacBook Air M2", price=1450, quantity=100),
        Product("Bose QuietComfort Earbuds", price=250, quantity=500),
        Product("Google Pixel 7", price=500, quantity=250),
        NonStockedProduct("Windows License", price=125),
        LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
        ]
    # Create promotion catalog
    second_half_price = SecondHalfPrice("Second Half price!")
    buy_two_get_one_free = BuyTwoGetOneFree("Buy 2, Get 1 Free!")
    thirty_percent = PercentageDiscount("30% off!", percentage=30)

    # Add promotions to products
    product_list[0].set_promotion(second_half_price)
    product_list[1].set_promotion(buy_two_get_one_free)
    product_list[3].set_promotion(thirty_percent)

    # Create the store with the product list
    best_buy = Store(product_list)
    # Start the store interface
    while True:
        if start(best_buy) == '4':
            print("Thank you for shopping at Best Buy.\nGoodbye!")
            break


if __name__ == "__main__":
    main()
