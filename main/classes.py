# class BankAccaut:
#     def __init__(self, name, balance):
#         self.name = name
#         self.__balance = balance
#
#     def get_balance(self):
#         return self.__balance
#
#     def set_balance(self, value):
#         if not isinstance(value, (int, float)):
#             raise ValueError("Баланс должен быть числом")
#         self.__balance = value
#
#     def del_balance(self):
#         print("Баланс удалён")
#         del self.__balance
#
#     balance = property(fget=get_balance, fset=set_balance, fdel=del_balance)
#
#
# acc = BankAccaut('Deniss', 777)

# from string import digits
#
#
# class User:
#     def __init__(self, login, password):
#         self.login = login
#         self.password = password
#         self.__secret = 'secretsecretsecret'
#
#     @property
#     def secret(self):
#         s = input("Введите пашь пароль")
#         if s == self.password:
#             return self.__secret
#         raise ValueError("Vale parool")
#
#     @property
#     def password(self):
#         print("getter called")
#         return self.__password
#
#     @staticmethod
#     def is_num(password):
#         for digit in digits:
#             if digit in password:
#                 return True
#         return False
#
#     # @staticmethod
#     # def brutforce(password):
#     #     with open('./passbrut.txt') as f:
#     #         lines = f.readlines()
#     #         for line in lines:
#     #             line = line.strip()
#     #             password = str(password).strip()
#     #             if line == password:
#     #                 return True
#     #         return False
#
#     @password.setter
#     def password(self, value):
#         print("setter called")
#         if not isinstance(value, (str)):
#             raise TypeError("Вы ввели не строку")
#         if len(value) < 4:
#             raise ValueError("Длина слишком мала. Минимум 4 символа")
#         if len(value) > 12:
#             raise ValueError("Длина слишкомв елика. Максимум 12 символа")
#         if not User.is_num(value):
#             raise ValueError("Пароль должен содержать хотябы одну цифру.")
#         # if User.brutforce(value):
#         #     raise ValueError("Пароль слабый!.")
#         self.__password = value
#
#     @password.deleter
#     def password(self):
#         del self.__password
#
#
# x = User("user", '55944212')
#
# # first = User("narvere", 1234456)
# # first.password = 15
# # print(first.password)
#
#
# # with open('passbrut.txt') as f:
# #     lines = f.readlines()
# #
# #     aaa = '55944212'
# #
# #     for line in lines:
# #         line = line.strip()
# #         if line == aaa:
# #             print("ok")

# class Example:
#     @staticmethod
#     def static_hello():
#         print("hello static")
#
#     @classmethod
#     def class_hello(cls):
#         print(f"hello {cls}")

class Departamen:
    PYTHON_DEV = 3
    GO_DEV = 3
    REACT_DEV = 2

    def make_backend(self):
        print("Python an Go")

    def make_frontend(self):
        print("React")


it1 = Departamen()
