'''
Best Buy
A program that lists the products of a store and makes orders
'''

from store import Store
from products import Product


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
                if active_products[product_index].get_quantity() >= amount:
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
    product_list = [
         Product("MacBook Air M2", price=1450, quantity=100),
         Product("Bose QuietComfort Earbuds", price=250, quantity=500),
         Product("Google Pixel 7", price=500, quantity=250)
                   ]
    best_buy = Store(product_list)
    while True:
        if start(best_buy) == '4':
            break


if __name__ == "__main__":
    main()
