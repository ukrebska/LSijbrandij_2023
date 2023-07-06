#!/bin/bash 

# This script gives numbers for the dEBM variables melt, refreeze, SMB and snow fall respectively for LIS and FIS. It works best with input taken from the outfiles from get_input4post.sh and get_ysm.

experiments="alakeGLAC alake13ka plake"

echo ""
echo ">> START FIS"
echo ""

for expid in $experiments; do
	echo "...read files for ${expid}"
	infile=../data/${expid}.post.nc4
	ofile=../data/${expid}.post_FIS_tmp
	in_ysm=../data/${expid}.post_ysm.nc
	o_ysm=../data/${expid}.post_ysm_FIS_tmp
	
	echo "...selecting FIS from ymonmean" 
	cdo selindexbox,1600,1862,757,1153 $infile $ofile
	
	echo ""
	echo "This is SMB in Gt/year for FIS and ${expid}:"
	cdo output -fldsum -mulc,25 -divc,1000000 -mulc,365 -yearmean -selvar,SMB $ofile	#fldsum gives for whole region, mulc25 due to 5km resolution, divc1000000 to get from mm to km, mulc365 to get from day to year, yearmean to get averaged mm/day in one timestep
	echo "This is melt in Gt/year for FIS and ${expid}:"
	cdo output -fldsum -mulc,25 -divc,1000000 -mulc,365 -yearmean -selvar,melt $ofile
	echo "This is refreeze in Gt/year for FIS and ${expid}:"
	cdo output -fldsum -mulc,25 -divc,1000000 -mulc,365 -yearmean -selvar,refreeze $ofile
	echo "This is snow in Gt/year for FIS and ${expid}:"
	cdo output -fldsum -mulc,25 -divc,1000000 -mulc,365 -yearmean -selvar,snow $ofile
	echo ""
#	echo "...selecting FIS from yseasmean"
#	cdo selindexbox,1600,1862,757,1153 $in_ysm $o_ysm
#
#	echo ""
#	echo "This is the seasonal contributions of different variables in Gt/season for ${expid}:"
#	echo ">>> ${expid} melt:"
#	cdo output -fldsum -mulc,25 -divc,1000000 -mulc,91.25 -selvar,melt $o_ysm
#	echo ">>> ${expid} refreeze:"
#        cdo output -fldsum -mulc,25 -divc,1000000 -mulc,91.25 -selvar,refreeze $o_ysm
#	echo ">>> ${expid} SMB:"
#        cdo output -fldsum -mulc,25 -divc,1000000 -mulc,91.25 -selvar,SMB $o_ysm
#	echo ">>> ${expid} snow:"
#        cdo output -fldsum -mulc,25 -divc,1000000 -mulc,91.25 -selvar,snow $o_ysm
	echo ""
	echo "...clean up"
	echo ""
	rm *tmp
done

echo ""
echo ">> START LIS" 
echo ""

for expid in $experiments; do        
	echo "...read files for ${expid}"
        infile=../data/${expid}.post.nc
        ofile=../data/${expid}.post_LIS_tmp
        in_ysm=../data/${expid}.post_ysm.nc
        o_ysm=../data/${expid}.post_ysm_LIS_tmp
	echo ""
        echo "...selecting LIS from ymonmean--" 
        cdo selindexbox,511,1070,322,1072 $infile $ofile
        echo ""
        echo "This is SMB in Gt/year for LIS and ${expid}:"
        cdo output -fldsum -mulc,25 -divc,1000000 -mulc,365 -yearmean -selvar,SMB $ofile
        echo "This is melt in Gt/year for LIS and ${expid}:"
        cdo output -fldsum -mulc,25 -divc,1000000 -mulc,365 -yearmean -selvar,melt $ofile
        echo "This is refreeze in Gt/year for LIS and ${expid}:"
        cdo output -fldsum -mulc,25 -divc,1000000 -mulc,365 -yearmean -selvar,refreeze $ofile
        echo "This is snow in Gt/year for LIS and ${expid}:"
        cdo output -fldsum -mulc,25 -divc,1000000 -mulc,365 -yearmean -selvar,snow $ofile

#        echo ""
#        echo "...selecting LIS from yseasmean"
#        cdo selindexbox,511,1070,322,1072 $in_ysm $o_ysm
#
#        echo ""
#        echo "This is the seasonal contributions of different variables in Gt/season for ${expid}:"
#        echo ">>> ${expid} melt:"
#        cdo output -fldsum -mulc,25 -divc,1000000 -mulc,91.25 -selvar,melt $o_ysm
#        echo ">>> ${expid} refreeze:"
#        cdo output -fldsum -mulc,25 -divc,1000000 -mulc,91.25 -selvar,refreeze $o_ysm
#        echo ">>> ${expid} SMB:"
#        cdo output -fldsum -mulc,25 -divc,1000000 -mulc,91.25 -selvar,SMB $o_ysm
#        echo ">>> ${expid} snow:"
#        cdo output -fldsum -mulc,25 -divc,1000000 -mulc,91.25 -selvar,snow $o_ysm
#done

        echo ""
        echo "...cleaning up"
done

        rm ../data/*tmp
