from turtle import *

def hilbert(turtle, order, size, angle):
    if order == 0:
        return
    turtle.right(angle)
    hilbert(turtle, order-1, size, -angle)
    turtle.forward(size)
    turtle.left(angle)
    hilbert(turtle, order-1, size, angle)
    turtle.forward(size)
    hilbert(turtle, order-1, size, angle)
    turtle.left(angle)
    turtle.forward(size)
    hilbert(turtle, order-1, size, -angle)
    turtle.right(angle)

# Main program
my_turtle = Turtle()
hilbert(my_turtle, order=3, size=10, angle=90)
done()