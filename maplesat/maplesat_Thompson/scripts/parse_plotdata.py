import sys, getopt

argv = sys.argv[1:]

inputFile=""
outputFile="out.txt"
col=[] 
subtract = False
divide = False
add = False

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


 # write SDCL data
file = open(inputFile, "r")
lines = file.readlines()
	
splittedFirstLine = lines[0].strip("\n").split(",")

if len(col) == 0:    
	print("Column Header:")
	for headers in splittedFirstLine:
		print(headers)
	exit(0)

colSelected = []
outputColSize = 0

# In a subtraction/division/addition scenario, we only need 1 column output
if not (subtract or divide or add):
	outputColSize = len(col)
else:
	outputColSize = 1

for x in range(outputColSize):
	colSelected.append([])

if subtract:
	if len(col) != 2:
		print("Size of the Columns for Subtraction is not 2")
		exit(1)
	
	for iter in range(len(lines)):
		if iter != 0:
			splittedLine = lines[iter].strip("\n").split(",")

			index1 = int(col[0])
			index2 = int(col[1])
			toAppend1 = splittedLine[index1]
			toAppend2 = splittedLine[index2]

			if toAppend2 == "" or toAppend1 == "":
				colSelected[0].append(5000)
			else:
				colSelected[0].append(float(toAppend1) - float(toAppend2))
elif divide:
	if len(col) != 2:
		print("Size of the Columns for Division is not 2")
		exit(1)
	
	for iter in range(len(lines)):
		if iter != 0:
			splittedLine = lines[iter].strip("\n").split(",")

			index1 = int(col[0])
			index2 = int(col[1])
			toAppend1 = splittedLine[index1]
			toAppend2 = splittedLine[index2]

			if toAppend2 == "" or toAppend1 == "" or float(toAppend2) == 0:
				colSelected[0].append("0")
			else:
				colSelected[0].append(float(toAppend1) / float(toAppend2))
elif add:
	if len(col) <= 2:
		print("Size of the Columns for Addition is less than 2")
		exit(1)
	
	

	for iter in range(len(lines)):
		if iter != 0:
			outputVal = 0
			splittedLine = lines[iter].strip("\n").split(",")
			for colIter in range(len(col)):
				index = int(col[colIter])
				toAppend = splittedLine[index]

				if toAppend == "" or splittedLine[19] == "INDETERMINATE":
					outputVal = 10000
					break
				else:
					outputVal = outputVal + float(toAppend)
					if (outputVal > 5000):
						print(splittedLine[1])

			colSelected[0].append(float(outputVal))

else:
	for iter in range(len(lines)):
		if iter != 0:
			splittedLine = lines[iter].strip("\n").split(",")

			for x in range(len(col)):
				index = int(col[x])
				toAppend = splittedLine[index]
				if toAppend == "" or splittedLine[19] == "INDETERMINATE":
					colSelected[x].append(5000) # Place Holder
				else:
					colSelected[x].append(float(toAppend))
			
file.close()

# # print(cpuTime)
if subtract:
	index1 = int(col[0])
	index2 = int(col[1])
	colSelected[0].sort(key = float)

	# Parse Output File Names
	header1 = splittedFirstLine[index1].split(" ")
	header2 = splittedFirstLine[index2].split(" ")
	header_name = header1[0] + "-subtract-" + header2[0]

	print(header_name)
	outputFileStr = outputFile.split(".")
	if len(outputFileStr) == 1:
		file = open((outputFile + "_" + header_name), "w")
	else:
		outputFileName = (outputFileStr[0] + "_" + header_name)
		for it in range (1, len(outputFileStr)):
			outputFileName = outputFileName + "." + outputFileStr[it]
		file = open(outputFileName, "w")
	# Output File Names Parsed
	count = 1
	for item in colSelected[x]:
		# file.writelines(str(count) + " " + str(item) + "\n")
		file.writelines(str(item) + "\n")
		count = count + 1
	file.close()

elif divide:
	index1 = int(col[0])
	index2 = int(col[1])
	colSelected[0].sort(key = float)

	# Parse Output File Names
	header1 = splittedFirstLine[index1].split(" ")
	header2 = splittedFirstLine[index2].split(" ")
	header_name = header1[0] + "-divide-" + header2[0]

	print(header_name)
	outputFileStr = outputFile.split(".")
	if len(outputFileStr) == 1:
		file = open((outputFile + "_" + header_name), "w")
	else:
		outputFileName = (outputFileStr[0] + "_" + header_name)
		for it in range (1, len(outputFileStr)):
			outputFileName = outputFileName + "." + outputFileStr[it]
		file = open(outputFileName, "w")
	# Output File Names Parsed
	count = 1
	for item in colSelected[x]:
		# file.writelines(str(count) + " " + str(item) + "\n")
		file.writelines(str(item) + "\n")
		count = count + 1
	file.close()

elif add:
	index1 = int(col[0])
	index2 = int(col[1])
	colSelected[0].sort(key = float)

	# Parse Output File Names
	header1 = splittedFirstLine[index1].split(" ")
	header2 = splittedFirstLine[index2].split(" ")
	header_name = header1[0] + "-add-" + header2[0]

	print(header_name)
	outputFileStr = outputFile.split(".")
	if len(outputFileStr) == 1:
		file = open((outputFile + "_" + header_name), "w")
	else:
		outputFileName = (outputFileStr[0] + "_" + header_name)
		for it in range (1, len(outputFileStr)):
			outputFileName = outputFileName + "." + outputFileStr[it]
		file = open(outputFileName, "w")
	# Output File Names Parsed
	count = 1
	for item in colSelected[x]:
		# file.writelines(str(count) + " " + str(item) + "\n")
		file.writelines(str(item) + "\n")
		count = count + 1
	file.close()

else:
	for x in range(outputColSize):
		index = int(col[x])
		colSelected[x].sort(key = float)

		# Parse Output File Names
		header = splittedFirstLine[index].split(" ")
		header_name = header[0]

		print(header_name)
		outputFileStr = outputFile.split(".")
		if len(outputFileStr) == 1:
			file = open((outputFile + "_" + header_name), "w")
		else:
			outputFileName = (outputFileStr[0] + "_" + header_name)
			for it in range (1, len(outputFileStr)):
				outputFileName = outputFileName + "." + outputFileStr[it]
			file = open(outputFileName, "w")
		# Output File Names Parsed
		count = 1
		for item in colSelected[x]:
			# file.writelines(str(count) + " " + str(item) + "\n")
			file.writelines(str(item) + "\n")
			count = count + 1
		file.close()

# # write CDCL data
# file = open("ParsedResults/SATComp2020_ParsedMaplesat.txt", "r")
# lines = file.readlines()

# cpuTime = []

# for line in lines:
#     splittedLine = line.split(",")
#     time = splittedLine[14]
#     if time == "":
#         cpuTime.append("5000.00")
#     else:
#         cpuTime.append(time)

# file.close()

# cpuTime.sort(key = float)

# file = open("PlotData/SATComp2020_PlotDataMaplesat.txt", "w")

# count = 1
# for item in cpuTime:
#     file.writelines(str(count) + " " + item + "\n")
#     count = count + 1
# file.close()
