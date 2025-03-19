from abc import ABC, abstractmethod

class Product:
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
            return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}. Promotion: {self.promotion.name}"
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}"


    def buy(self, quantity):
            '''
            Buys a given quantity of the product.
            Returns the total price (float) of the purchase.
            Updates the quantity of the product.
            In case of a problem raises an Exception (ValueError).
            :param quantity:
            :return:
            '''
            if quantity > self.quantity:
                raise ValueError("Not enough items in stock")

            if self.promotion:
                total_price = self.promotion.apply_promotion(self, quantity)
                # For "Buy 2, Get 1 Free" promotion
                if isinstance(self.promotion, BuyTwoGetOneFree):
                    actual_quantity = quantity + (quantity // 2)
                else:
                    actual_quantity = quantity
            else:
                total_price = self.price * quantity
                actual_quantity = quantity

            self.quantity -= actual_quantity  # Reduce the stock
            if self.quantity == 0:
                self.active = False

            return total_price

    def set_promotion(self, promotion):
        self.promotion = promotion


class NonStockedProduct(Product):
    def __init__(self, name: str, price: float):
        super().__init__(name, price, quantity=0)
        self.active = True

    def show(self) -> str:
        if self.promotion:
            return f"{self.name}, Price: {self.price}, Quantity: Unlimited. Promotion: {self.promotion.name}"
        return f"{self.name}, Price: {self.price}, Quantity: Unlimited."

    def buy(self, quantity: int) -> float:
        if self.promotion:
            return self.promotion.apply_promotion(self, quantity)
        return self.price * quantity


class LimitedProduct(Product):
    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        super().__init__(name, price, quantity)
        self.maximum = maximum

    def show(self) -> str:
        if self.promotion:
            return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, Maximum: {self.maximum}. Promotion: {self.promotion.name}"
        return f"{self.name}, Price: {self.price}, Quantity: {self.quantity}, Maximum: {self.maximum}"

    def buy(self, quantity: int) -> float:
        if quantity > self.maximum:
            raise ValueError(f"Cannot buy more than {self.maximum} items at once")
        return super().buy(quantity)


class Promotion(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def apply_promotion(self, product, quantity: int) -> float:
        pass


class PercentageDiscount(Promotion):
    def __init__(self, name: str, percentage: float):
        super().__init__(name)
        self.percentage = percentage

    def apply_promotion(self, product, quantity: int) -> float:
        return product.price * quantity * (1 - self.percentage / 100)


class SecondHalfPrice(Promotion):
    def __init__(self, name: str):
        super().__init__(name)

    def apply_promotion(self, product, quantity: int) -> float:
        full_price_count = (quantity + 1) // 2
        half_price_count = quantity - full_price_count
        return (full_price_count * product.price) + (half_price_count * product.price / 2)


class BuyTwoGetOneFree(Promotion):
    def __init__(self, name: str):
        super().__init__(name)

    def apply_promotion(self, product, quantity: int) -> float:
        regular_price_count = quantity - (quantity // 3)
        return product.price * regular_price_count