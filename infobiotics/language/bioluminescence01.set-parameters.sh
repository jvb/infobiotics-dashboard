#!/bin/sh

infile=bioluminescence01.sbml

calculate () {
	expression=$1
	scale=16
	result=$(echo "$expression" | wcalc -P$scale -q)
	echo $result
}

round () {
	expression=$1
	result=$(echo "round($expression)" | wcalc -q)
	echo $result
}

NA="(6.02214179*10^23)" # avogadros number

####################
# parameter values #
####################

VN="(1*10^-13)" # nuclear volume (10^-13 litres)

# initial species levels
B_IM="100" # initial number of bacteria

S_IC="(1*10^-6)" # signal molecule concentration (molars)

# association rate
KON="(1*10^6)"

# equilibrium dissociation constants
KD1="(2*10^-8)" # B + S <-> B.S
KD2="(1*10^-8)" # B.B + S <-> B.B.S
KD3="(1*10^-12)" # B + B <-> B.B
KD5="(1*10^-6)" # B.S + B <-> B.B.S

k4="1.0"

########################
# end parameter values #
########################

# initial number of signal molecules
S_IM=$(round "${S_IC}*${NA}*${VN}")

CON=$(calculate "${KON}/(${NA}*${VN})")
CON_DIMER=$(calculate "2.0*${KON}/(${NA}*${VN})")

# reaction constants
# B + S <-> B.S
kon1=${CON}
koff1=$(calculate "${KD1}*${KON}")

# B.B + S <-> B.B.S
kon2=${CON}
koff2=$(calculate "${KD2}*${KON}")

# B + B <-> B.B
kon3=${CON_DIMER}
koff3=$(calculate "${KD3}*${KON}")

# B.S + B <-> B.B.S
kon5=${CON}
koff5=$(calculate "${KD5}*${KON}")

##################
# set parameters #
##################

printf "B_IM = %s\n" ${B_IM}
sbml-set-initial-amount $infile B "module1:1:" ${B_IM}

printf "S_IM = %d %s\n" ${S_IM} "$(echo ${S_IC} | sed 's/)/ M)/')"
sbml-set-initial-amount $infile S "module1:1:" ${S_IM}

printf "KD1 = %s\n" $KD1
printf "kon1 = %0.2e\n" $kon1
sbml-set-reaction-constant $infile kon1 $kon1
printf "koff1 = %0.2e\n" $koff1
sbml-set-reaction-constant $infile koff1 $koff1

printf "KD2 = %s\n" $KD2
printf "kon2 = %0.2e\n" $kon2
sbml-set-reaction-constant $infile kon2 $kon2
printf "koff2 = %0.2e\n" $koff2
sbml-set-reaction-constant $infile koff2 $koff2

printf "KD3 = %s\n" $KD3
printf "kon3 = %0.2e\n" $kon3
sbml-set-reaction-constant $infile kon3 $kon3
printf "koff3 = %0.2e\n" $koff3
sbml-set-reaction-constant $infile koff3 $koff3

printf "KD5 = %s\n" $KD5
printf "kon5 = %0.2e\n" $kon5
sbml-set-reaction-constant $infile kon5 $kon5
printf "koff5 = %0.2e\n" $koff5
sbml-set-reaction-constant $infile koff5 $koff5

printf "k4 = %0.2e\n" $k4
sbml-set-reaction-constant $infile k4 $k4
