class BankAccaut:
    def __init__(self, name, balance):
        self.name = name
        self.__balance = balance

    def get_balance(self):
        return self.__balance

    def set_balance(self, value):
        if not isinstance(value, (int, float)):
            raise ValueError("Баланс должен быть числом")
        self.__balance = value

    def del_balance(self):
        print("Баланс удалён")
        del self.__balance

    balance = property(fget=get_balance, fset=set_balance, fdel=del_balance)


acc = BankAccaut('Deniss', 777)
