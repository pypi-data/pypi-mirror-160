six_function_calculator
-----------------------

This is a simple calculator. 
This calculator starts with an initial value of 0 within memory. It stores the results of previous calculations within memory, subsequent calculations use the current value stored in memory. 


This calculator performs 6 functions

1. Addition of a maximum of two numbers at a time
2. subtraction of a maximum of two numbers at a time
3. Mutiplication of a maximum of two numbers at a time
4. Division involving two numbers
5. Finding the nth root of a number
6. Reseting the calculator's working memory to 0

Licence: MIT (see LICENCE)

Installing this package 
-----------------------

pip install six_function_calculator

Example
-------


from six_function_calculator import Calculator 

-Creating an instance of Calculator:

calculator1 = Calculator() 

-Using this instance of Calculator 

calculator1.add(0) -> 0

calculator1.add(2) -> 2

calculator1.add(4) -> 6






