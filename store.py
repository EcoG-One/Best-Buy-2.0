class Store():
    '''
    Holds all products and
    allows the user to make a purchase of multiple products at once
    '''
    def __init__(self,products ):
        '''
        initiates the class
        :param products: list of products that exist in the store
        '''
        self.products = products

    def add_product(self, product):
        '''
        Adds a product to the store
        :param product: the product to be added
        '''
        self.products.append(product)

    def remove_product(self, product):
        '''
        Removes a product from store.
        :param product: the product to be removed
        '''
        try:
            self.products.remove(product)
        except ValueError:
            print(f'{product} does not exist in Store')

    def get_total_quantity(self):
        '''
        :return: how many items are in the store in total
        '''
        total = 0
        for product in self.products:
            total += product.quantity
        return total

    def get_all_products(self):
        '''
        :return: all products in the store that are active.
        '''
        all_products = []
        for product in self.products:
            if product.is_active():
                all_products.append(product)
        return all_products

    def order(self, shopping_list):
        '''
        Buys the products
        :param shopping_list: a list of tuples,
               where each tuple has 2 items:
               Product (Product class) and quantity (int).
        :return: the total price of the order.
        '''
        total_price = 0
        for item in shopping_list:
            try:
                total_price += item[0].buy(item[1])
            except ValueError:
                print(f'{item[0].name} not added to Shopping List. '
                      f'Order quantity is larger than what exists')
        return total_price
