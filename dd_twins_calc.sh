#!/bin/bash
#SBATCH -n 1
#SBATCH -p HaswellPriority

echo "#time(ps) Total_New 111 100 110 twinboundary twfrac numat" >> DislocationDensity_MD.dat
cd /gpfs/scratchfs1/sumit/Ta_pillar/Compression/dumpfiles

for i in `seq 0 2000 200000`; do

timestep=0.002

	total=`awk < Ta110_compression_300K.${i}.analysis.log '/Total dislocation/{print $5}'`
	other=`awk < Ta110_compression_300K.${i}.analysis.log '/Other Burgers/{print $4}'`
	d111=`grep -F '[bcc] 1/2<111>:' Ta110_compression_300K.${i}.analysis.log | tail -1 | awk {'print $3'}`
	d100=`grep -F '[bcc] <100>:' Ta110_compression_300K.${i}.analysis.log | tail -1 | awk {'print $3'}`
	d110=`grep -F '[bcc] <110>:' Ta110_compression_300K.${i}.analysis.log | tail -1 | awk {'print $3'}`
	twin=`grep "matching atoms" Ta110_compression_300K.${i}.analysis.log | tail -1 | awk {'print $4'}`
	numat=`grep -F 'Reading ' Ta110_compression_300K.${i}.analysis.log | tail -1 | awk {'print $2'}`

	tot_new=$(awk -v v1=$total -v v2=$other 'BEGIN {print v1-v2}')
	t=$(echo "scale=6;$timestep*$i" | bc)
	twfrac=$(echo "scale=6;$twin/$numat" | bc)

	#Converting time to integer value (if needed)
	t_int=${t%.*}

	echo "$t_int $tot_new $d111 $d100 $d110 $twin $twfrac $numat" >> /gpfs/scratchfs1/sumit/Ta_pillar/Compression/Analyses/DXA/DislocationDensity_MD.dat


done
