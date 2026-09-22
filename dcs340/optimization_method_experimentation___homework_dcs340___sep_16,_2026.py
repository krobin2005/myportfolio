# -*- coding: utf-8 -*-
"""Optimization Method Experimentation | Homework DCS340 | Sep 16, 2026

Original file is located at
    https://colab.research.google.com/drive/10jddf17AM2lgzsNNgvP4LW-mAMGqrYaT
"""

import numpy as np
import matplotlib.pyplot as plt

x_vals = np.linspace(0, 5, 500)

# Define our pumpkin function
def f(x):
    return 4 - (x - 2)**2

# Define the derivative (needed for Newton and Gradient Descent)
# f'(x) = -2(x - 2)
def df(x):
    return -2 * (x - 2)

# Define the second derivative (needed for Newton's Method)
# f''(x) = -2
def ddf(x):
    return -2

def bisection_method(a, b, tolerance=0.01) -> float:
  """
  Finds the root of the derivative of f(x) using the bisection method to locate the peak.

  Parameters:
  a (float): The lower bound of the interval.
  b (float): The upper bound of the interval.
  tolerance (float): The desired accuracy for the root.

  Returns:
  float: The estimated x-coordinate of the peak within the given tolerance.
  """
  # We look for where the derivative df(x) is 0
  # Check if the function changes sign over the interval [a, b].
  # If df(a) and df(b) have the same sign, a root might not be in this interval,
  # or there might be multiple roots, making bisection unsuitable.
  if df(a) * df(b) > 0:
      print("The peak might not be between these points!") # Inform the user about potential issues.
      return None # Return None as no reliable peak can be found.

  # Continue iterating as long as the interval is larger than the specified tolerance.
  # The condition (b - a) / 2 > tolerance checks if the current error is too high.
  while (b - a) / 2 > tolerance:
      midpoint = (a + b) / 2 # Calculate the midpoint of the current interval.
      # If the derivative at the midpoint is exactly zero, we've found the peak.
      if df(midpoint) == 0:
          return midpoint # Return the midpoint as the peak.
      # If the sign of df(a) and df(midpoint) are different, the root (peak) is in the left half.
      elif df(a) * df(midpoint) < 0:
          b = midpoint # Shrink the interval by moving the upper bound to the midpoint.
      # Otherwise, the root (peak) must be in the right half of the interval.
      else:
          a = midpoint # Shrink the interval by moving the lower bound to the midpoint.

  # Once the loop terminates, the interval is sufficiently small.
  # Return the midpoint of the final interval as the approximation of the peak.
  return (a + b) / 2

def newtons_method(start_x, iterations=5):
  """
  Finds the peak of the function f(x) using Newton's method.

  Parameters:
  start_x (float): The initial guess for the x-coordinate of the peak.
  iterations (int): The number of iterations to perform for convergence.

  Returns:
  float: The estimated x-coordinate of the peak after the specified iterations.
  """
  x = start_x # Initialize the current estimate of the peak's x-coordinate with the starting guess.
  print(f"Starting Newton's Method at x = {x}") # Print the initial starting point.

  # Loop for a specified number of iterations to refine the estimate.
  for i in range(iterations):
      # Newton's update rule for optimization: x = x - f'(x) / f''(x)
      # This formula uses the first and second derivatives to iteratively get closer to the root of the first derivative (which is the peak).
      x = x - df(x) / ddf(x)
      # Print the current iteration number, the updated x value, and the function value at that x.
      print(f"Iteration {i+1}: x = {x:.4f}, f(x) = {f(x):.4f}")

  return x # Return the final estimated x-coordinate of the peak after all iterations.

def main():
  peak_bisect = bisection_method(0, 5)
  print(f"Bisection Method found peak near: {peak_bisect:.4f}")
  print("-" * 100)
  peak_newton = newtons_method(start_x=0.5)
  print(f"\nNewton found the peak at: {peak_newton} meters.")
  plt.plot(x_vals, f(x_vals), label='Pumpkin Path')
  plt.axvline(2, color='red', linestyle='--', label='Actual Peak (x=2)')
  plt.title("Pumpkin Trajectory")
  plt.xlabel("Distance (m)")
  plt.ylabel("Height (m)")
  plt.legend()
  plt.grid(True)
  plt.show()

if __name__ == "__main__":
    main()

"""Reflection:
This assignment helped me compare optimization methods by \
observing how bisection and Newton's method merge toward\
the same peak from different starting assumptions. I reminded me \
heaveally of merge sort as a sorting method. \
Bisection is more robust when the function's sign change is known, \
while Newton's method is faster when the derivative and second derivative \
are reliable and the starting point is well chosen. Overall, \
the experiment showed that optimization accuracy depends not only on the formula, \
but also on the method's assumptions and the quality of the initial guess.
"""

