class Logger:
    def log(self, message):
        print(f"[LOG]: {message}")

class Connection:
    def connect(self):
        print("Connecting to database...")

# Multiple Inheritance
class DatabaseService(Logger, Connection):
    def start(self):
        self.connect()
        self.log("Service started successfully.")

db = DatabaseService()
db.start()



class A:
    def greet(self):
        print("Hello from A")

class B(A):
    def greet(self):
        print("Hello from B")

class C(A):
    def greet(self):
        print("Hello from C")

class D(B, C):
    pass

d = D()
d.greet()  # This will call B's version

# How to check the search order:
print(D.__mro__) 
# Output: (D, B, C, A, object)



class Base:
    def __init__(self):
        print("Base Init")

class Left(Base):
    def __init__(self):
        print("Left Init")
        super().__init__()

class Right(Base):
    def __init__(self):
        print("Right Init")
        super().__init__()

class Sub(Left, Right):
    def __init__(self):
        print("Sub Init")
        super().__init__()

s = Sub()
# Notice how Right.__init__ is called by Left's super() call!


class JSONSerializerMixin:
    def to_json(self):
        import json
        return json.dumps(self.__dict__)

class Employee:
    def __init__(self, name, position):
        self.name = name
        self.position = position

class TechEmployee(Employee, JSONSerializerMixin):
    pass

dev = TechEmployee("John", "Python Developer")
print(dev.to_json())