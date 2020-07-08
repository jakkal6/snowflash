#!/bin/bash --login
########## SBATCH Lines for Resource Request ##########
#SBATCH --time=12:00:00       # limit of wall clock time - how long the job will run (same as -t)
#SBATCH --nodes=1             # number of different nodes - could be an exact number or a range of nodes (same as -N)
#SBATCH --ntasks=1            # number of tasks - how many tasks (nodes) that you require (same as -n)
#SBATCH --cpus-per-task=1     # number of CPUs (or cores) per task (same as -c)
#SBATCH --mem-per-cpu=1G      # memory required per allocated CPU (or core) - amount of memory (in bytes)
#SBATCH --job-name snow1      # you can give your job a name for easier identification (same as -J)
#SBATCH --mail-user=zacjohn@msu.edu 
#SBATCH --mail-type=BEGIN,END
########## Command Lines to Run ##########
 
module purge
module load intel/2018b
module load HDF5/1.10
module load GSL

conda activate flashbang
cd /mnt/gs18/scratch/users/john7457/flash2snowglobes
#cd ${HOME}/flash2snowglobes

python flash2snowglobes.py
 
scontrol show job $SLURM_JOB_ID     ### write job information to output file

