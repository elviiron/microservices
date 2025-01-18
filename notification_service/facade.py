from comand import PlaceOrderComand

class OrderFacade:
    def __init__(self, order_repo, email_service):
        self.place_order_command = PlaceOrderComand(order_repo, email_service)

    def place_order(self, name, city, address, email, product_list_str):
        self.place_order_command.execute(name, city, address, email, product_list_str)