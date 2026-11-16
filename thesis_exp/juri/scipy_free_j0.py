"""Bessel J0 without scipy (the system scipy is broken against numpy 2): numerical integral
J0(x) = (1/pi) * int_0^pi cos(x sin t) dt, trapezoid on 20001 points (error < 1e-10 for |x| < 100)."""
import numpy as np
_T = np.linspace(0.0, np.pi, 20001)


def j0(x):
    return float(np.trapezoid(np.cos(x * np.sin(_T)), _T) / np.pi)


if __name__ == "__main__":                 # spot values (Abramowitz & Stegun Table 9.1)
    for x, ref in ((0.0, 1.0), (1.0, 0.7651976866), (2.404825557695773, 0.0), (5.0, -0.1775967713)):
        print(x, j0(x), ref)
