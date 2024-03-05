import subprocess
import sys
import pandas as pd

# check if the number of input arguments is correct
if len(sys.argv) != 4:
    print('Usage: python quantification_script_grep.py <fastqs_to_process_file> <input_barcodes_file> <output_file_name>')
    sys.exit(1)

# extract file names from input arguments
fastqs_to_process_file = sys.argv[1]
input_barcodes_file = sys.argv[2]
output_file_name = sys.argv[3]

# take as input the file with the names of the fastqs which are to be processed
with open(fastqs_to_process_file, 'r') as f:
    fastqs = f.readlines()
    fastqs = [x.strip() for x in fastqs]

# prepare the command string:
command = r"time parallel -k -j 30 'zgrep -o -F -H -f " +  input_barcodes_file +  r" {} | sort | uniq -c' ::: "

# command = r"zgrep -o -F -f " +  input_barcodes_file +  r" temp.fastq.gz | sort | uniq -c"

# BELOW IS THE INITIAL IMPLEMENTATION WITH THE SHELL=FALSE OPTION
# command = ['time','parallel','-k','-j','30',"'zgrep",'-o', '-F', '-f', input_barcodes_file, '{}', '|', 'sort', '|', 'uniq', "-c'", ':::']
# command.extend(fastqs)
# add the output file to the command string
# command.append('>')
# command.append('grep_output.txt')


# add the fastqs to the command string
for fastq in fastqs:
    command = command + fastq + ' '

# Add the output file to the command string
command = command + '> grep_output.txt'

print(command)

subprocess.run(command, shell=True)

# process the output file to get the counts of the barcodes

# get the number of barcodes (as that will determine how to split the output file)
with open(input_barcodes_file, 'r') as f:
    barcodes = f.readlines()
    barcodes = [x.strip() for x in barcodes]
    sorted_barcodes = sorted(barcodes) # this is very important as the output of grep is in sorted order
    num_barcodes = len(barcodes)

# read the output file and store the counts of the barcodes for each fastq
counts = {}
with open('grep_output.txt', 'r') as f:
    output = f.readlines()
    output = [x.strip() for x in output]

# NO LONGER NEEDED AS I AM INITALIZING THE NONEXISTENT BARCODES WITH 0 COUNTS NOW 
# ensure that len(output) is len(fastqs) * num_barcodes
# if len(output) != len(fastqs) * num_barcodes:
#     print('Error: the output file does not have the correct number of lines')
#     sys.exit(1)

# make a dict to store the counts of the barcodes for each fastq
counts = {}
for line in output:
    # split the line into the count and the fastq and barcode
    count, fastq_barcode = line.split(' ')
    # split the fastq and barcode using the ':' delimiter
    fastq, barcode = fastq_barcode.split(':')
    if fastq not in counts:
        counts[fastq] = {}
        # initialize the counts for the barcodes (so that nonexistent ones have a count of 0)
        for barcode in sorted_barcodes:
            counts[fastq][barcode] = 0
    counts[fastq][barcode] = int(count)

# OLD IMPLEMENTATION OF THE COUNTS DICTIONARY
# make a dict to store the counts of the barcodes for each fastq
# counts = {}
# for fastq_num, fastq in enumerate(fastqs):
#     counts[fastq] = {}
#     for barcode_num, barcode in enumerate(sorted_barcodes):
#         counts[fastq][barcode] = int(output[fastq_num*num_barcodes + barcode_num].split(' ')[0])
        # barcode counts stored above, now make the final dataframe type object which will be the result


# make a dataframe from the counts dict

# make empty dataframe
df = pd.DataFrame()

df["barcodes"] = sorted_barcodes
for fastq in counts:
    df[fastq] = [counts[fastq][barcode] for barcode in sorted_barcodes]

# write the dataframe to a file
df.to_csv(output_file_name, index=False)
