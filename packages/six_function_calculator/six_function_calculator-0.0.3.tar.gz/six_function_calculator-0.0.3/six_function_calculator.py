"""six function calculator"""
__version__ = "0.0.3"


class Calculator():
    """This is a basic calculator that performs the following operattions
        1. Addition
        2. Subtraction
        3. Multiplication
        4. Division
        5. Finding the nth root of a number
        6. Reset Calculator Memory

        ---Doctest-----------

        >>> calc1 = Calculator()
        >>> calc1.add(10)
        10
        >>> calc1.subtract(5)
        5
        >>> calc1.multiply(100)
        500
        >>> calc1.divide(5)
        100.0
        >>> calc1.nthroot(2)
        10.0
        >>> calc1.reset()
        0
    """

    def __init__(self, calcmemory=0) -> float:
        """Initialising the calculator to a value of 0"""
        self.calcmemory = calcmemory
        return

    def add(self,number2:int) -> float:
        """Add to current number in memory and return result"""
        try:
            int(number2)
        except(NameError, TypeError, ValueError, SyntaxError):
            print("The only valid arguments are numbers \n")
        self.calcmemory = self.calcmemory + number2
        return self.calcmemory

    def subtract(self, number2:int) -> float:
        """Subtract from current number in memory and return result"""
        try:
            int(number2)
        except(NameError, TypeError, ValueError, SyntaxError):
            print("The only valid arguments are numbers \n")
        self.calcmemory = self.calcmemory - number2
        return self.calcmemory

    def multiply(self, number2:int) -> float:
        """Multiply current number in memory and return result"""
        try:
            int(number2)
        except(NameError, TypeError, ValueError, SyntaxError):
            print("The only valid arguments are numbers \n")
        self.calcmemory = self.calcmemory*number2
        return self.calcmemory

    def divide(self, number2:int) -> float:
        """Divide current number in memory and return result"""
        try:
            int(number2)
        except(NameError, TypeError, ValueError, SyntaxError):
            print("The only valid arguments are numbers \n")
            return self.calcmemory

        try:
            self.calcmemory = self.calcmemory/number2
        except ZeroDivisionError:
            print("You cannot divide by zero")
        return self.calcmemory

    def nthroot(self, number2: int) -> float:
        """nth root of the current number """
        try:
            int(number2)
        except(NameError, TypeError, ValueError, SyntaxError):
            print("The only valid arguments are numbers \n")

        def nthrooteqn (currentcalcvalue: float, nthroot: float):
            try:
                self.calcmemory =  currentcalcvalue**(1/nthroot)
            except ZeroDivisionError:
                print("You cannot divide by zero (equivalent to raising zero to a negative power)")
            return self.calcmemory

        nthrooteqn(self.calcmemory, number2)
        return self.calcmemory

    def reset(self) -> int:
        """Reset calculator memory to 0 """
        self.calcmemory = 0
        return self.calcmemory
