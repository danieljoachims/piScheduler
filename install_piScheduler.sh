#!/bin/bash
#
# piScheduler - Installation of supporting software
# gW  2015-04-05
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

echo  ... System Updating 
sudo apt-get update -y


echo  ... Download piScheduler etc .. to the home directory
cd ~

wget https://dl.dropboxusercontent.com/u/35444930/piScheduler/piScheduler.zip   -O piScheduler.zip
unzip piScheduler.zip -x */piSchedule.prefs.json
chmod +x tmuxStart.sh

echo  ... piScheduler -- install some python supporting software
sudo apt-get install python-dev
sudo apt-get install python-pip

echo  ... piScheduler -- install 'tmux'
sudo apt-get install tmux

# pip packages
echo  ... piScheduler -- install 'python-dateutil'
sudo pip install python-dateutil

echo  ... piScheduler -- install 'APScheduler'
sudo pip install apscheduler

echo  ... piScheduler  -- install 'ephem'
sudo pip install ephem

echo  ... piScheduler  -- install 'pbkdf2'
sudo pip install pbkdf2

echo  ... piScheduler  -- install 'bottle'
sudo pip install bottle

echo  ... change to piSchedule directory
cd ~/piScheduler

python pySchedule.py -ini

