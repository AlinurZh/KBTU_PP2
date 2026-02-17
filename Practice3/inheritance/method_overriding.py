class Employee:
    """Base class for all employees"""
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
    
    def work(self):
        """Basic work method"""
        return f"{self.name} is working"
    
    def get_salary(self):
        """Basic salary calculation"""
        return self.salary
    
    def take_break(self):
        return f"{self.name} is taking a 15-minute break"
    
    def __str__(self):
        """String representation"""
        return f"Employee: {self.name}"


class Manager(Employee):
    """Manager class with overridden methods"""
    def __init__(self, name, salary, department, bonus):
        super().__init__(name, salary)
        self.department = department
        self.bonus = bonus
    
    def work(self):
        """Override: Managers work differently"""
        return f"{self.name} is managing the {self.department} department"
    
    def get_salary(self):
        """Override: Include bonus in salary"""
        base_salary = super().get_salary()  # Call parent method
        return base_salary + self.bonus
    
    def take_break(self):
        """Override completely: Different break time"""
        return f"{self.name} is in a meeting (no breaks for managers!)"
    
    def __str__(self):
        """Override string representation"""
        return f"Manager: {self.name}, Department: {self.department}"


class Developer(Employee):
    """Developer class with method overriding"""
    def __init__(self, name, salary, programming_language):
        super().__init__(name, salary)
        self.programming_language = programming_language
    
    def work(self):
        """Override: Developers code"""
        return f"{self.name} is coding in {self.programming_language}"
    
    def debug(self):
        """New method specific to Developer"""
        return f"{self.name} is debugging code"


class Intern(Employee):
    """Intern with partial method overriding"""
    def __init__(self, name, salary, mentor):
        super().__init__(name, salary)
        self.mentor = mentor
    
    def work(self):
        """Override with extension: Call parent + add more"""
        parent_work = super().work()  # Call parent's work method
        return f"{parent_work} under supervision of {self.mentor}"
    
    def get_salary(self):
        """Override with modification"""
        base = super().get_salary()
        return base * 0.5  # Interns get 50% salary