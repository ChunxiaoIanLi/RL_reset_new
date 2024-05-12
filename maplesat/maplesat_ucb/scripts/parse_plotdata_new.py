import sys, getopt
import pandas as pd
import numpy as np

argv = sys.argv[1:]

inputFile=""
outputFile="out.txt"
col=[] 
subtract = False
divide = False
add = False
upperLimit = 5000.0
lowerLimit = 0

if len(argv) <= 1:
	print("Usage:")
	print("1. To check the list of columns header, run:")
	print("python3 parse_plotdata.py -i INPUTFILE")
	print("2. To parse the file, run:")
	print("python3 parse_plotdata.py -i INPUTFILE -o OUTPUTFILE -c COL_A,COL_B,...,COL_X")
	print("3. To parse the file and subtract two columns (col_1 - col_2), run:")
	print("python3 parse_plotdata.py -i INPUTFILE -o OUTPUTFILE -c COL_1,COL_2 -s TRUE")
	exit(1)

try:
	opts, args = getopt.getopt(argv, "i:o:c:s:d:a:", ["input=", "output=", "col=", "subtract=", "divide=", "add="])
	  
except:
	print("Exception in parsing the commandline args.")

for opt, arg in opts:
	if opt in ['-i', '--input']:
		inputFile = arg
	elif opt in ['-o', '--output']:
		outputFile = arg
	elif opt in ['-c', '--col']:
		col = arg.split(",")
	elif opt in ['-s', '--subtract']:
		if arg == "TRUE":
			subtract = True
	elif opt in ['-d', '--divide']:
		if arg == "TRUE":
			divide = True
	elif opt in ['-a', '--add']:
		if arg == "TRUE":
			add = True

# If no col is specified, simply prints out the header
if len(col) == 0:    
	print("Column Header:")
	for headers in splittedFirstLine:
		print(headers)
	exit(0)

# Sanity check for input columns
try:
	col = [int(numeric_string) for numeric_string in col]
except:
	print("Error in converting columns into a numeric array")
	exit(1)

statsDF = pd.read_csv(inputFile)

if subtract:
	if len(col) != 2:
		print("Size of the Columns for Subtraction is not 2")
		exit(1)
	
	outputDF = statsDF.iloc[:,col[0]] - statsDF.iloc[:,col[1]]
	outputDF = outputDF.sort_values(ascending = True)
	outputDF.fillna(upperLimit, inplace=True)

elif divide:
	if len(col) != 2:
		print("Size of the Columns for Division is not 2")
		exit(1)

	outputDF = statsDF.iloc[:,col[0]].divide(statsDF.iloc[:,col[1]])
	outputDF.fillna(lowerLimit, inplace=True)
	outputDF.replace([np.inf, -np.inf], 0, inplace=True)
	outputDF = outputDF.sort_values(ascending = True)

elif add:
	if len(col) < 2:
		print("Size of the Columns for Addition is less than 2")
		exit(1)
	
	outputDF = statsDF.iloc[:,col[0]]
	# print(outputDF)
	for iter in range (len(col) - 1):
		outputDF = outputDF + statsDF.iloc[:,col[iter + 1]]
	outputDF = pd.concat([outputDF,statsDF.iloc[:,19]], axis=1)
	outputDF.iloc[outputDF.iloc[:,1] == "INDETERMINATE", 0] = len(col) * upperLimit
	outputDF = outputDF.iloc[:,0]
	outputDF.fillna(len(col) * upperLimit, inplace=True)
	outputDF = outputDF.sort_values(ascending = True)

else:
	outputDF = statsDF.iloc[:,col]
	outputDF = pd.concat([outputDF,statsDF.iloc[:,19]], axis=1)
	outputDF.iloc[outputDF.iloc[:,-1] == "INDETERMINATE", 0] = upperLimit
	outputDF.pop(outputDF.columns[-1])
	outputDF.fillna(upperLimit, inplace=True)
	outputDF = outputDF.sort_values(ascending = True, by=outputDF.columns[0])

outputDF.to_csv(outputFile, header=None, index=False)
