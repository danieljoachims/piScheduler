#!/bin/bash
#
# Handle piSchedule with using 'tmux'
#

SESSION=piSchedule
tmux="tmux -2 -f tmux.conf"
piDir="~/piScheduler"


echo "Hello, "$USER" "
echo "  Script will handle 'tmux' for 'piSchedule'."
echo
echo -n "  Do you want to run 'piSchedule' with 'tmux' [Y/n]: "
read mode


if [[ ${mode,,} != "y" || $mode == "" ]]; then
  echo "  'piSchedule' will not use 'tmux'."
  cd ~/piScheduler
  python piSchedule.py -ini
  exit 1
fi


# if the session is already running, just attach to it.
$tmux has-session -t $SESSION
if [ $? -eq 0 ]; then
       echo "  Session $SESSION already exists. Attaching."
       sleep 1
       $tmux attach -t $SESSION
       exit 0;
   else
       echo "  Session $SESSION unknown. Will be created!"
       sleep 1
       # create a new session, named $SESSION
       tmux new-session -d -s $SESSION
       #tmux send-keys "echo  *** piSchedule will be started with 'tmux' .. wait a moment **" C-m
       tmux send-keys "cd ~/piScheduler" C-m
       tmux send-keys "python piSchedule.py -ini" C-m

       tmux -2 attach-session -t $SESSION 

       exit 0
fi
