#!/bin/bash
## script master.sh
#$ -S /bin/bash
#$ -cwd
#$ -v PATH
qsub -t 1-`ls -l ../temp_in | wc -l` array.sh