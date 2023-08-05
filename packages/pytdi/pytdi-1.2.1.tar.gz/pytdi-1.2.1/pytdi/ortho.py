#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# BSD 3-Clause License
#
# Copyright (c) 2022, California Institute of Technology and
# Max Planck Institute for Gravitational Physics (Albert Einstein Institute)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# This software may be subject to U.S. export control laws. By accepting this
# software, the user agrees to comply with all applicable U.S. export laws and
# regulations. User has the responsibility to obtain export licenses, or other
# export authority as may be required before exporting such information to
# foreign countries or providing access to foreign persons.
#
"""
Defines first and second-generation quasi-orthogonal combinations (A, E, and T).

Authors:
    Martin Staab <martin.staab@aei.mpg.de>
    Jean-Baptiste Bayle <j2b.bayle@gmail.com>
"""

from numpy import sqrt
from .michelson import X1, Y1, Z1, X2, Y2, Z2


#: First-generation :math:`A_1` orthogonal combination.
#:
#: This combination is a linear combinations of first-generation Michelson
#: combinations, c.f. :ref:`standard-combinations:michelson combinations`.
#:
#: It is function of the beatnote measurements.
A1 = (Z1 - X1) / sqrt(2)

#: First-generation :math:`E_1` orthogonal combination.
#:
#: This combination is a linear combinations of first-generation Michelson
#: combinations, c.f. :ref:`standard-combinations:michelson combinations`.
#:
#: It is function of the beatnote measurements.
E1 = (X1 - 2 * Y1 + Z1) / sqrt(6)

#: First-generation :math:`T_1` orthogonal combination.
#:
#: This combination has a reduced sensitivity to gravitational waves,
#: but retain a high response function to instrumental noises. Therefore,
#: it is often dubbed the *null channel*.
#:
#: This combination is a linear combinations of first-generation Michelson
#: combinations, c.f. :ref:`standard-combinations:michelson combinations`.
#:
#: It is function of the beatnote measurements.
T1 = (X1 + Y1 + Z1) / sqrt(3)

#: Second-generation :math:`A_2` orthogonal combination.
#:
#: This combination is a linear combinations of second-generation Michelson
#: combinations, c.f. :ref:`standard-combinations:michelson combinations`.
#:
#: It is function of the beatnote measurements.
A2 = (Z2 - X2) / sqrt(2)

#: Second-generation :math:`E_2` orthogonal combination.
#:
#: This combination is a linear combinations of second-generation Michelson
#: combinations, c.f. :ref:`standard-combinations:michelson combinations`.
#:
#: It is function of the beatnote measurements.
E2 = (X2 - 2 * Y2 + Z2) / sqrt(6)

#: Second-generation :math:`T_1` orthogonal combination.
#:
#: This combination has a reduced sensitivity to gravitational waves,
#: but retain a high response function to instrumental noises. Therefore,
#: it is often dubbed the *null channel*.
#:
#: This combination is a linear combinations of second-generation Michelson
#: combinations, c.f. :ref:`standard-combinations:michelson combinations`.
#:
#: It is function of the beatnote measurements.
T2 = (X2 + Y2 + Z2) / sqrt(3)
