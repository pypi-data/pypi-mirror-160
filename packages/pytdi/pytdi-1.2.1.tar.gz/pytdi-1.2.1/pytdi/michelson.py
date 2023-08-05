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
Defines TDI first-and-second-generation Michelson variables.

Authors:
    Martin Staab <martin.staab@aei.mpg.de>
    Jean-Baptiste Bayle <j2b.bayle@gmail.com>
"""

from . import core
from . import intervar


#: First-generation :math:`X_1` Michelson combination.
#:
#: This combination is defined as a function of the :math:`\eta` intermediary
#: variables. Use them with the inter-spacecraft beatnotes if you want to
#: bypass intermediary variables.
X1_ETA = core.LISATDICombination.from_string('13121 -13121')

#: First-generation :math:`Y_1` Michelson combination.
#:
#: This combination is defined as a function of the :math:`\eta` intermediary
#: variables. Use them with the inter-spacecraft beatnotes if you want to
#: bypass intermediary variables.
Y1_ETA = X1_ETA.rotated()


#: First-generation :math:`Z_1` Michelson combination.
#:
#: This combination is defined as a function of the :math:`\eta` intermediary
#: variables. Use them with the inter-spacecraft beatnotes if you want to
#: bypass intermediary variables.
Z1_ETA = Y1_ETA.rotated()

#: First-generation :math:`X_1` Michelson combination.
#:
#: This combination is the composition of ``X1_ETA`` and the intermediary
#: variables. Therefore, it is function of the beatnote measurements.
X1 = X1_ETA @ intervar.ETA_SET

#: First-generation :math:`Y_1` Michelson combination.
#:
#: This combination is the composition of ``Y1_ETA`` and the intermediary
#: variables. Therefore, it is function of the beatnote measurements.
Y1 = Y1_ETA @ intervar.ETA_SET

#: First-generation :math:`Z_1` Michelson combination.
#:
#: This combination is the composition of ``Z1_ETA`` and the intermediary
#: variables. Therefore, it is function of the beatnote measurements.
Z1 = Z1_ETA @ intervar.ETA_SET


#: Second-generation :math:`X_2` Michelson combination.
#:
#: This combination is defined as a function of the :math:`\eta` intermediary
#: variables. Use them with the inter-spacecraft beatnotes if you want to
#: bypass intermediary variables.
X2_ETA = core.LISATDICombination.from_string('131212131 -121313121')

#: Second-generation :math:`Y_2` Michelson combination.
#:
#: This combination is defined as a function of the :math:`\eta` intermediary
#: variables. Use them with the inter-spacecraft beatnotes if you want to
#: bypass intermediary variables.
Y2_ETA = X2_ETA.rotated()

#: Second-generation :math:`Z_2` Michelson combination.
#:
#: This combination is defined as a function of the :math:`\eta` intermediary
#: variables. Use them with the inter-spacecraft beatnotes if you want to
#: bypass intermediary variables.
Z2_ETA = Y2_ETA.rotated()

#: Second-generation :math:`X_2` Michelson combination.
#:
#: This combination is the composition of ``X2_ETA`` and the intermediary
#: variables. Therefore, it is function of the beatnote measurements.
X2 = X2_ETA @ intervar.ETA_SET

#: Second-generation :math:`Y_2` Michelson combination.
#:
#: This combination is the composition of ``Y2_ETA`` and the intermediary
#: variables. Therefore, it is function of the beatnote measurements.
Y2 = Y2_ETA @ intervar.ETA_SET

#: Second-generation :math:`Z_2` Michelson combination.
#:
#: This combination is the composition of ``Z2_ETA`` and the intermediary
#: variables. Therefore, it is function of the beatnote measurements.
Z2 = Z2_ETA @ intervar.ETA_SET
