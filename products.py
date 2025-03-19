from abc import ABC, abstractmethod

class Product:
    '''
    product available in the store
      :param name: product name
      :param price: product price
      :param quantity: product quantity
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
        self.promotion = None

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
        :return: a string that represents the product and promotion
        '''
        if self.promotion:
            return (f"{self.name}, Price: {self.price}, "
                    f"Quantity: {self.quantity}. "
                    f"Promotion: {self.promotion.name}")
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"

    def buy(self, quantity):
            '''
            Buys a given quantity of the product.
            Returns the total price (float) of the purchase.
            Updates the quantity of the product.
            In case of a problem raises an Exception (ValueError).
            :param quantity:
            :return: the total price (float) of the purchase.
            '''
            if quantity > self.quantity:
                raise ValueError("Not enough items in stock")

            if self.promotion:
                total_price = self.promotion.apply_promotion(self, quantity)
            else:
                total_price = self.price * quantity
            self.quantity -= quantity  # Reduce the stock
            if self.quantity == 0:
                self.active = False

            return total_price

    def set_promotion(self, promotion):
        '''Setter function for promotion
        '''
        self.promotion = promotion


class NonStockedProduct(Product):
    '''
    Products, not physical, with unlimited stock.
    Quantity is set to zero and always stays that way
    '''
    def __init__(self, name, price):
        super().__init__(name, price, quantity=0)
        self.active = True

    def show(self):
        '''
        overrides the show method of the Product class
        :return: a string that represents the product and promotion
        '''
        if self.promotion:
            return (f"{self.name}, Price: {self.price}, Quantity: Unlimited. "
                    f"Promotion: {self.promotion.name}")
        return f"{self.name}, Price: {self.price}, Quantity: Unlimited."

    def buy(self, quantity: int):
        '''
        overrides the buy method of the Product class
        Buys a given quantity of the product.
        Returns the total price (float) of the purchase.
        In case of a problem raises an Exception (ValueError).
        :param quantity:
        :return: the total price (float) of the purchase.
        '''
        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)
        return self.price * quantity


class LimitedProduct(Product):
    '''
    Products that can only be purchased limited times in an order
    '''
    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        super().__init__(name, price, quantity)
        self.maximum = maximum

    def show(self):
        '''
       overrides the show method of the Product class
       :return: a string that represents the product and promotion
       '''
        if self.promotion:
            return (f"{self.name}, Price: {self.price}, "
                    f"Quantity: {self.quantity}, Maximum: {self.maximum}. "
                    f"Promotion: {self.promotion.name}")
        return (f"{self.name}, Price: {self.price}, Quantity: {self.quantity},"
                f" Maximum: {self.maximum}")

    def buy(self, quantity: int):
        '''
        overrides the buy method of the Product class
        Buys a given quantity of the product,
        only if this quantity is not bigger than the maximum allowed.
        Returns the total price (float) of the purchase.
        In case of a problem raises an Exception (ValueError).
        :param quantity:
        :return: the total price (float) of the purchase.
        '''
        if quantity > self.maximum:
            raise ValueError(f"Cannot buy more than {self.maximum} "
                             f"items at once")
        return super().buy(quantity)


class Promotion(ABC):
    '''
    Abstract class for varius types of promotion
    '''
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity):
        '''
       Abstract method to apply promotion
       '''
        pass


class PercentageDiscount(Promotion):
    '''
    Percentage discount Promotion
    '''
    def __init__(self, name, percentage):
        super().__init__(name)
        self.percentage = percentage

    def apply_promotion(self, product, quantity):
        '''
        Applies the Percentage discount Promotion
        :param product:
        :param quantity:
        :return: price after applying the promotion
        '''
        return product.price * quantity * (1 - self.percentage / 100)


class SecondHalfPrice(Promotion):
    '''
    Second item at half price Promotion
    '''
    def __init__(self, name):
        super().__init__(name)

    def apply_promotion(self, product, quantity):
        '''
        Applies the Second item at half price Promotion
        :param product:
        :param quantity:
        :return: price after applying the promotion
        '''
        full_price_count = (quantity + 1) // 2
        half_price_count = quantity - full_price_count
        return ((full_price_count * product.price)
                + (half_price_count * product.price / 2))


class BuyTwoGetOneFree(Promotion):
    '''
    Buy 2, get 1 free Promotion
    '''
    def __init__(self, name):
        super().__init__(name)

    def apply_promotion(self, product, quantity):
        '''
        Applies the Buy 2, get 1 free Promotion
        :param product:
        :param quantity:
        :return: price after applying the promotion
        '''
        regular_price_count = quantity - (quantity // 3)
        return product.price * regular_price_count