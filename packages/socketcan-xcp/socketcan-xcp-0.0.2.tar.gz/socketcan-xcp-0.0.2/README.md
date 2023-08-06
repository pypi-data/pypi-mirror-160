# socketcan-xcp

![coverage](https://gitlab.com/Menschel/socketcan-xcp/badges/master/coverage.svg)
![pipeline](https://gitlab.com/Menschel/socketcan-xcp/badges/master/pipeline.svg)

[Documentation](https://menschel.gitlab.io/socketcan-xcp/)

A python 3 interface to Universal Measurement and Calibration Protocol XCP

# Description

Goal of this project is to make XCP available in python in a "pythonic" way.

Keep implementation as simple as possible.
Use python3 built-in functions and bytearrays as well as standard modules like struct and enum wherever possible.

# Why yet another implementation of XCP

While there is pyxcp implementation available, it has Windows dependencies and is in general not feasible to adapt. Instead this XCP implementation is done from scratch in pure python.

