#!/bin/bash
SESSION=piSchedule
tmux="tmux -2 -f tmux.conf"
 
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
       $tmux new -s $SESSION
       exit 0
fi
