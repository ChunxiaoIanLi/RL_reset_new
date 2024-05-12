import csv
import sys

def main():
    # Parsing commandline inputs
    if (len(sys.argv) != 2):
        print("Usage: python3 process-reset-stats.py FILENAME")
        exit(1)

    filename = sys.argv[1]

    # Variable declaration
    totalResetWin = 0
    totalResetLose = 0
    totalNoResetWin = 0
    totalNoResetLose = 0

    # User-defined Variables
    localEMA_filename = filename + ".new-cpu-time-reset-50%-local-EMA"
    LBD_filename = filename + ".new-cpu-time-reset-50%-lbd"
    LLR_filename = filename + ".new-cpu-time-reset-50%-lr"
    doReset_filename = filename + ".new-cpu-time-do-reset-50%"

    decay = 0.8
    csv_arr = []
    csv_header = ["CPU-Time", "#Conflicts", "#Decision", "restartLearningRate", "restartEMA", "LLR>EMA?", "Reset-Decision", "reset-Outcome", "NoReset-Outcome"]
    llr_arr = []
    llr_header = ["CPU-Time", "ResetConflictCounter", "ResetDecisionCounter", \
    "LLR", "globalEMA", "doReset", "localEMA", "chunkEMA-2", "chunkEMA-3",	\
    "chunkEMA-4", "chunkEMA-5", "Avg-2", "Avg-3", "Avg-4", "Avg-5", \
    "localChunkedEMA-2", "globalChunkedEMA-2", "localChunkedEMA-3", "globalChunkedEMA-3", \
    "localChunkedEMA-4", "globalChunkedEMA-4", "localChunkedEMA-5", "globalChunkedEMA-5" \
    ]

    chunking = [2, 3, 4, 5]
    startingChunkingIndex = 7


    with open(localEMA_filename, 'r') as csv_file:
        reader = csv.reader(csv_file)
        
        for row in reader:
            csv_arr.append(row)
        csv_file.close()

        for a in range (len(csv_arr)):
            csv_arr[a].append(int(csv_arr[a][3] > csv_arr[a][4]))

    with open(doReset_filename, 'r') as csv_file:
        reader = csv.reader(csv_file)
        counter = 0
        for row in reader:
            csv_arr[counter].append(int(row[1]))
            counter = counter + 1
        csv_file.close()
        
    
    iter = 0
    while (iter < (len(csv_arr) - 1)):
        if (csv_arr[iter][6] == 1):       
            csv_arr[iter].append(csv_arr[iter+1][5])

            if (csv_arr[iter+1][5] == 1):
                totalResetWin = totalResetWin + 1
            else:
                totalResetLose = totalResetLose + 1
        else:
            csv_arr[iter].append("")
        iter = iter + 1
    csv_arr[iter].append("")

    iter = 0
    while (iter < (len(csv_arr) - 1)):
        if (csv_arr[iter][6] == 0):
            csv_arr[iter].append(csv_arr[iter+1][5])

            if (csv_arr[iter+1][5] == 1):
                totalNoResetWin = totalNoResetWin + 1
            else:
                totalNoResetLose = totalNoResetLose + 1
        else:
            csv_arr[iter].append("")
        iter = iter + 1
    csv_arr[iter].append("")

    # print(csv_arr)
    print("totalResetWin: " + str(totalResetWin))
    print("totalResetLose: " + str(totalResetLose))
    print("totalNoResetWin: " + str(totalNoResetWin))
    print("totalNoResetLose: " + str(totalNoResetLose))
    
    with open('stats.csv', mode='w') as stats_file:
        writer = csv.writer(stats_file)
        writer.writerow(csv_header)

        for a in range (len(csv_arr)):
            writer.writerow(csv_arr[a])
        stats_file.close()
    
    with open(LLR_filename, 'r') as csv_file:
        reader = csv.reader(csv_file)
        
        for row in reader:
            llr_arr.append(row)
        csv_file.close()

    for item in chunking:
        iter = 0

        for b in range (item):
            llr_arr[b].append(0)

        while (iter + item < len(llr_arr)):
            maxSize = 0
            if (item < (len(llr_arr) - iter)):
                maxSize = item
            else:
                maxSize = (len(llr_arr) - iter)

            chunkedEMA = 0
            for a in range (maxSize):
                chunkedEMA *= decay
                chunkedEMA += (float(llr_arr[iter+a][1]) / float(llr_arr[iter+a][2]) * (1 - decay))
            
            # Adjust the index offline
            llr_arr[iter+item].append(chunkedEMA)
            iter = iter + 1
    
    for item in chunking:
        iter = 0

        for b in range (item):
            llr_arr[b].append(0)
        
        while (iter + item < len(llr_arr)):
            maxSize = 0
            if (item < (len(llr_arr) - iter)):
                maxSize = item
            else:
                maxSize = (len(llr_arr) - iter)

            totalConflict = 0
            totalDecision = 0
            
            for a in range (maxSize):
                totalConflict += float(llr_arr[iter+a][1])
                totalDecision += float(llr_arr[iter+a][2])
            
            totalLearningRate = 1.0 * totalConflict / totalDecision
            
            # Adjust the index offline
            llr_arr[iter+item].append(totalLearningRate)
            iter = iter + 1

    for x in range (len(chunking)):
        index = startingChunkingIndex + x
        localChunkedEMA = 0
        globalChunkedEMA = 0
        for a in range (len(llr_arr)):
            localChunkedEMA *= decay
            globalChunkedEMA *= decay
            if (float(llr_arr[a][6]) != 0):
                localChunkedEMA += llr_arr[a][index]
            else:
                localChunkedEMA = 0
            globalChunkedEMA += llr_arr[a][index]
            llr_arr[a].append(localChunkedEMA)
            llr_arr[a].append(globalChunkedEMA)
            

    with open('llr.csv', mode='w') as stats_file:
        writer = csv.writer(stats_file)
        writer.writerow(llr_header)

        for a in range (len(llr_arr)):
            writer.writerow(llr_arr[a])
        stats_file.close()

if __name__ == "__main__":
    main()