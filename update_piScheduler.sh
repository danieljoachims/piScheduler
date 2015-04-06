#!/bin/bash
#
# piScheduler - updating					gW  2015-04-05
# Download of piSchedule without any *.ini *.log files 
#
# Copyright (C) 2015 G.Wahl <gneandr@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#


echo Download piScheduler etc ..  download piSchedule without any *.ini *.log files 

cd ~

wget https://dl.dropboxusercontent.com/u/35444930/piScheduler/piScheduler.zip  -O piScheduler.zip
unzip piScheduler.zip -x */*.ini */*.log */piSchedule.prefs.json
ls -ll
ls -ll piScheduler

cd ~/piScheduler
python piSchedule.py -ini
