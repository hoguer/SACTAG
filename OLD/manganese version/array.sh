#!/bin/bash
## script master.sh
#$ -S /bin/bash
#$ -cwd
#$ -v PATH
python master.py ../temp_in/file$SGE_TASK_ID