#!/bin/bash
# script run-real.sh
#SBATCH -J real_WRF4
#SBATCH -p golden
#SBATCH -N 1
#SBATCH --ntasks-per-node 22
#SBATCH -o slurm.%x.%j.out
#SBATCH -e slurm.%x.%j.err

cd $HOME/WRFV4/WRF
ml restore wrf-operativo

export CORES=22
/sbin/logsave REGISTRO_REAL.txt mpirun -np $CORES real.exe
