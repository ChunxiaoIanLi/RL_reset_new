# Input validation
if [[ $# -ne 2 ]]; then
	echo "Usage: $0 <PARSED_FILE_1> <PARSED_FILE_2>"
	exit -1
fi

# Set up parameters
FILE_1="${1}"
FILE_2="${2}"
TRUE="true"
SKIP_INDETERMINATE="false"

check_file_exists() {
	FILE_TO_CHECK="${1}"
	if [[ ! -f ${FILE_TO_CHECK} ]]; then
		echo "Could not find file '${FILE_TO_CHECK}'"
		exit -1
	fi
}

# Check that all required files exist
check_file_exists ${FILE_1}
check_file_exists ${FILE_2}

# Check that compared files are the same length
FILE_1_LENGTH=($(wc -l ${FILE_1})); FILE_1_LENGTH=${FILE_1_LENGTH[0]}
FILE_2_LENGTH=($(wc -l ${FILE_2})); FILE_2_LENGTH=${FILE_2_LENGTH[0]}

if [[ ${FILE_1_LENGTH} -ne ${FILE_2_LENGTH} ]]; then
	echo "Parsed files are different lengths (${FILE_1_LENGTH} and ${FILE_2_LENGTH})"
	exit -1
fi

# Read files
i=0
exec 3<"${FILE_1}"
exec 4<"${FILE_2}"

while read LINE_1 <&3; do
	read LINE_2 <&4
	
	# Ensure that the lines compare the same CNF
	CNF_1=${LINE_1#*,}; CNF_1=${CNF_1%%,*}
	CNF_2=${LINE_2#*,}; CNF_2=${CNF_2%%,*}
	
	if [[ ${CNF_1} != ${CNF_2} ]]; then
		echo "Files compare different CNFs: '${CNF_1}' and '${CNF_2}'"
		exit -1
	fi
	
	# Compare satisfiability
	SAT_1=${LINE_1##*,}
	SAT_2=${LINE_2##*,}

	if [[ ${SAT_1} != ${SAT_2} ]]; then
		if [[ ${SKIP_INDETERMINATE} == $TRUE ]]; then
			echo "${i} ${SAT_1} ${SAT_2}"
		elif [[ ${SAT_1} != INDETERMINATE && ${SAT_2} != INDETERMINATE ]]; then
			echo "${i} ${SAT_1} ${SAT_2}"
		fi
	fi

	i=$((i + 1))
done
