from typing import Callable
import typing
import timeit
import asyncio

async def integrate_async(fn: Callable[[float], float], a: float, b: float, samples: int = 200) -> float:
    sample_width = (b - a) / samples
    async def calculate_slice(sample: int):
        sample_input = a + sample_width*sample
        area = sample_width * (fn(sample_input) + 0.5 * (fn(sample_input + sample_width) - fn(sample_input)))
        return area
    tasks = []
    for i in range(samples):
        tasks.append(asyncio.create_task(calculate_slice(i)))
    integral = 0

    for task in asyncio.as_completed(tasks):
        integral += await task
    
    return integral


def integrate(fn: Callable[[float], float], a: float, b: float, samples: int = 200) -> float:
    sample_width = (b - a) / samples
    integral = 0
    sample_input = a

    for _ in range(samples):
        integral += sample_width * (fn(sample_input) + 0.5 * (fn(sample_input + sample_width) - fn(sample_input)))
        sample_input += sample_width
    
    return integral


def function(x):
    return 0.25*x**3 - 2*x**2 + 3*x + 3

print(timeit.timeit("""
import asyncio
asyncio.run(integrate_async(function, 0, 10, 5000))""", 
"""
import asyncio
async def integrate_async(fn, a: float, b: float, samples: int = 200) -> float:
    sample_width = (b - a) / samples
    async def calculate_slice(sample: int):
        sample_input = a + sample_width*sample
        area = sample_width * (fn(sample_input) + 0.5 * (fn(sample_input + sample_width) - fn(sample_input)))
        return area
    tasks = []
    for i in range(samples):
        tasks.append(asyncio.create_task(calculate_slice(i)))
    integral = 0

    for task in asyncio.as_completed(tasks):
        integral += await task
    
    return integral

def function(x):
    return 0.25*x**3 - 2*x**2 + 3*x + 3""", number=10))

print(timeit.timeit("""integrate(function, 0, 10, 5000)""", """def integrate(fn, a: float, b: float, samples: int = 200) -> float:
    sample_width = (b - a) / samples
    integral = 0
    sample_input = a

    for _ in range(samples):
        integral += sample_width * (fn(sample_input) + 0.5 * (fn(sample_input + sample_width) - fn(sample_input)))
        sample_input += sample_width
    
    return integral


def function(x):
    return 0.25*x**3 - 2*x**2 + 3*x + 3""", number = 10))
