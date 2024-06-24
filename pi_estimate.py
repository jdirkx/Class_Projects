"""Estimate the value of Pi with Monte Carlo simulation.
Author:  Jacob Dirkx
Credits:  Myself
"""
import random
import doctest
import points_plot
GOOD_PI = 3.141592653589793
SAMPLES = 5000
NUM_IN = 0

def  rand_point_unit_sq() -> tuple[float, float]:
    for iter in range(SAMPLES):
        """Returns random x,y both in range 0..1.0, 0..1.0.
        """
        x = random.random()
        y = random.random()
    return x, y

def in_unit_circle(x: float, y: float) -> bool:
    """ returns boolean value, true if point is in circle"""
    global NUM_IN  
    if x**2 + y**2 <= 1:
        NUM_IN += 1
        return True
    else:
        return False

def relative_error(est: float, expected: float) -> float:
    """ takes difference of estimate and actual pi and returns % error
    """
    abs_error = est - expected
    rel_error = abs(abs_error / expected)
    print(f"Relative error is approximately {(rel_error*100)}%")

def plot_random_points(n_points: int = SAMPLES):
    """Generate and plot n_points points
    in interval (0,0) to (1,1)
    Creates a window
    """
    points_plot.init()
    for i in range(n_points):
        x, y = rand_point_unit_sq()
        Loc = in_unit_circle(x,y)
        if Loc == True:
            points_plot.plot(x, y, color_rgb=(255, 10, 10))
        else:
            points_plot.plot(x, y, color_rgb=(240, 240, 240))

def pi_approx() -> float:
    " returns pi estimate"
    estimate = (NUM_IN/SAMPLES) * 4
    return estimate

def main():
    doctest.testmod()
    plot_random_points() 
    estimate = pi_approx()
    print(f"Pi is approximately {estimate}")
    relative_error(pi_approx(), GOOD_PI)
    points_plot.wait_to_close()

if __name__ == "__main__":
    main()
