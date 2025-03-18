
class Product():
    '''
    product available in the store
      :param name: product name
      :param  price: product price
      :param  quantity: product quantity
      :param  active: product condition
    '''
    def __init__(self, name, price, quantity):
        '''
        Initiator (constructor)
        Creates the instance variables (active is set to True).
        If something is invalid (empty name
        / negative price or quantity), raises an exception.
          :param name: product name
          :param  price: product price
          :param  quantity: product quantity
        '''
        if name == '':
            raise ValueError("Invalid input, Product must have a name")
        if price < 0:
            raise ValueError("Invalid input, Price cannot be negative")
        if quantity < 0:
            raise ValueError("Invalid input, Quantity cannot be negative")
        self.name = name
        self.price = price
        self.quantity = quantity
        if self.quantity > 0:
            self.active = True
        else:
            self.active = False

    def get_quantity(self):
        '''
        Getter method for quantity
        :return: the quantity of a product
        '''
        return self.quantity

    def set_quantity(self, quantity):
        '''
        Setter function for quantity.
        If quantity reaches 0, deactivates the product
        :param quantity: the quantity to set
        '''
        self.quantity = quantity
        if self.quantity == 0:
            self.active = False

    def is_active(self):
        '''
        Getter function for active.
        :return:  True if the product is active, otherwise False
        '''
        return self.active

    def activate(self):
        '''
        Activates the product.
        '''
        self.active = True

    def deactivate(self):
        '''
        Deactivates the product.
        '''
        self.active = False

    def show(self):
        '''
        :return: a string that represents the product
        '''
        return f'{self.name}, Price: ${self.price}, Quantity: {self.quantity}'

    def buy(self, quantity):
        '''
        Buys a given quantity of the product.
        Returns the total price (float) of the purchase.
        Updates the quantity of the product.
        In case of a problem raises an Exception (ValueError).
        :param quantity:
        :return:
        '''
        if self.quantity < quantity:
            raise ValueError("Error while making order!"
                             " Quantity larger than what exists")
        self.set_quantity(self.quantity - quantity)
        return quantity * self.price
