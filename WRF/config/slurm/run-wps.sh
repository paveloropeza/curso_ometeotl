#!/bin/bash
# geogrid
JOBID1=$(sbatch --parsable run-geogrid.sh)

# Check if submission was successful
if [ -z "$JOBID1" ]; then
    echo "Failed to submit run-geogrid.sh"
    exit 1
fi

# Prepara GFS
cd $HOME/WRFV4/WPS
./link_grib.csh $HOME/GFS/gfs*

# ungrib.exe
JOBID2=$(sbatch --parsable --dependency=afterok:$JOBID1 run-ungrib.sh)

# metgrid.exe
JOBID3=$(sbatch --parsable --dependency=afterok:$JOBID2 run-metgrid.sh)
