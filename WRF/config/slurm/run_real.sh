#!/bin/bash

# script run-real.sh
#SBATCH -J real_WRF4
#SBATCH -p id
#SBATCH -N 3
#SBATCH --ntasks-per-node 22
#SBATCH -o slurm.%x.%j.out
#SBATCH -o slurm.%x.%j.err

cd $HOME/WRFV4/WRF
ml load intel/2022u2/compilers
ml load curl hdf5 jasper libaec libpng mpi netcdf-c netcdf-fortran zlib
ml load wrf/4.2.1

export CORES=66
/sbin/logsave REGISTRO_REAL.txt mpirun -np $CORES real.exe
