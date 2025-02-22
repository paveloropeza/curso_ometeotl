#!/bin/bash

#SBATCH -J demo_WRF4_metgrid
#SBATCH -p golden
#SBATCH -N1
#SBATCH --ntasks-per-node 1
#SBATCH -o slurm.%x.%j.out
#SBATCH -e slurm.%x.%j.err

cd $HOME/WRFV4/WPS
ml restore wrf-operativo

srun metgrid.exe
