import matplotlib.pyplot as plt
import numpy as np
import collections
import math


def parametric_plot(x, y, samples, lbl):
    t = np.linspace(0, 1, samples)
    plt.plot(x(t), y(t), label=lbl)


def spline(samples=100):
    targets = []
    Location = collections.namedtuple('Location', ['x', 'y', 'theta'])

    while True:
        print(targets)

        try:
            print("Enter a non-number at any time to terminate and graph.")
            x = float(input("X-value: "))
            y = float(input("Y-value: "))
            theta = float(input("Orientation: "))
            targets.append(Location(x, y, theta))
        except ValueError:
            if input("\nGraph spline? (y/n) ") == "y":
                break

    prev = targets[0]

    for pos in targets[1:]:
        # Calculate position changes and slopes
        Dx = pos.x - prev.x
        Dy = pos.y - prev.y
        Sp = math.tan(prev.theta * math.pi / 180)
        Sn = math.tan(pos.theta * math.pi / 180)

        # Calculate parametric equation coefficients
        denom = Sn - Sp  # denominator in coefficients

        x1 = (2 * Dy - (Sn + Sp) * Dx) / denom
        x2 = 2 * (Sn * Dx - Dy) / denom
        x3 = prev.x

        y1 = ((Sn + Sp) * Dy - 2 * Sn * Sp * Dx) / denom
        y2 = Sp * x2
        y3 = prev.y

        # Add curve to plot
        parametric_plot(lambda t: x1*t*t + x2*t + x3,
                        lambda t: y1*t*t + y2*t + y3,
                        samples, str((pos.x, pos.y)))
        print("x1: %.4f, x2: %.4f, x3: %.4f" % (x1, x2, x3))
        print("y1: %.4f, y2: %.4f, y3: %.4f" % (y1, y2, y3))

        prev = pos

    plt.legend()
    plt.show()


def partial_cubic_spline(b_vals, samples=100):
    ends = []
    Location = collections.namedtuple('Location', ['x', 'y', 'theta'])

    for i in range(2):
        x = float(input("X-value: "))
        y = float(input("Y-value: "))
        theta = float(input("Orientation: "))
        ends.append(Location(x, y, theta))

    # Calculate position changes and slopes
    Dx = ends[1].x - ends[0].x
    Dy = ends[1].y - ends[0].y
    Si = math.tan(ends[0].theta * math.pi / 180)
    Sf = math.tan(ends[1].theta * math.pi / 180)

    for b in b_vals:
        x1 = Dx - b
        x2 = b
        x3 = ends[0].x

        y1 = 2 * Dx * Sf - 2 * Dy + b * (Si - Sf)
        y2 = 3 * Dy - 2 * Dx * Sf + b * (Sf - 2 * Si)
        y3 = b * Si
        y4 = ends[0].y

        # Add curve to plot
        parametric_plot(lambda t: x1 * t**2 + x2 * t + x3,
                        lambda t: y1 * t**3 + y2 * t**2 + y3 * t + y4,
                        samples, b)
        print("x1: %.4f, x2: %.4f, x3: %.4f" % (x1, x2, x3))
        print("y1: %.4f, y2: %.4f, y3: %.4f, y4: %.4f" % (y1, y2, y3, y4))

    plt.legend()
    plt.show()


#spline(1000)
#spline(1000)
partial_cubic_spline([0.1 * x**3 for x in range(-5, 6)], 1000)
