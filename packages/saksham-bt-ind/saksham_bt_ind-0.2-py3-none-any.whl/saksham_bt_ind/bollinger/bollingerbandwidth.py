#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
#
# Copyright (C) 2022 Finnovesh Inc.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from backtrader.indicators.bollinger import BollingerBands

class BollingerBandwidth(BollingerBands):
    '''
    Extends the Bollinger Bands with a bandwidth line
    '''
    alias = ("BBbandwidth", "BollingerBandwidth")
    lines = ('bbbandwidth',)
    plotinfo = dict(subplot=True, sameaxis = True, plotlog = True)
    plotlines = dict(bbbandwidth=dict(_name='%BBBW', color='lime'))  # display the line as %B on chart

    def __init__(self):
        super(BollingerBandwidth, self).__init__()
        self.l.bbbandwidth = (self.l.top - self.l.bot) / self.l.mid
       

    def next(self):
        #print("Next Indicator -> " + round(self.l.bbbandwidth[0],4).__str__())
        self.l.top[0] = round(self.l.top[0],4)
        self.l.bot[0] = round(self.l.bot[0],4)
        self.l.mid[0] = round(self.l.mid[0],4)
        self.l.bbbandwidth[0] = round(((self.l.top[0] - self.l.bot[0]) / self.l.mid[0]),4)
     