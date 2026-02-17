class Parent:
    def __init__(self, name):
        self.name = name
        print(f"Parent initialized with name: {self.name}")

class Child(Parent):
    def __init__(self, name, age):
        # Call the parent's __init__ method
        super().__init__(name)
        self.age = age
        print(f"Child initialized with age: {self.age}")

c = Child("Alice", 25)



class Robot:
    def work(self):
        print("Robot is performing basic tasks.")

class MedicRobot(Robot):
    def work(self):
        super().work()  # Do the basic tasks first
        print("MedicRobot is also healing patients.")

m = MedicRobot()
m.work()



class Base:
    def __init__(self, *args, **kwargs):
        print("Base reached")

class DecoratedBase(Base):
    def __init__(self, label, *args, **kwargs):
        print(f"Adding label: {label}")
        super().__init__(*args, **kwargs)

d = DecoratedBase(label="Primary", data="Some extra info")