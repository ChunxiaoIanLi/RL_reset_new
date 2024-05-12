# Input validation
if [[ $# -ne 1 ]]; then
	echo "Usage: $0 <INPUT_DIR>"
	exit -1
fi

# Set up parameters
INPUT_DIR="${1}"

# Generate list of files
find "${INPUT_DIR}" -name "*.cnf" -exec readlink -f {} \;
