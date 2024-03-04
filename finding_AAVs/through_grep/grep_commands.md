# Trying out stuff

## Old stuff

### initial commands (was just figuring out the right flags initially)
zgrep GTGCATGA RPE_1_S5_R1_001.fastq.gz
zgrep GTGCATGA RPE_1_S5_R2_001.fastq.gz | wc -l 
92727

### after extracting the file (noticed decent improvement in speeds) 
grep GTGCATGA RPE_1_S5_R2_001.fastq | wc -l 

### command to find multiple sequences in the file
grep -e GTGCATGA -e TGTTGGAG RPE_1_S5_R2_001.fastq | sort | uniq -c

## Timing stuff

### standard command and its corresponding time (note that its run on gzipped file)
time zgrep -o -m 1000 -e GTGCATGA RPE_1_S5_R2_001.fastq.gz | sort | uniq -c

real	0m1.868s
user	0m2.069s
sys	0m0.200s

### for gunzipped file
time grep -o -m 1000 -e GTGCATGA RPE_1_S5_R2_001.fastq | sort | uniq -c

real	0m0.832s
user	0m0.402s
sys	0m0.240s

### unzipped, but with -F flag

time zgrep -o -F -m 1000 -e GTGCATGA RPE_1_S5_R2_001.fastq.gz | sort | uniq -c

real	0m1.879s
user	0m2.043s
sys	0m0.242s

no difference basically

### trying on two compressed files with and without parallelization

time zgrep -o -F -m 1000 -e GTGCATGA RPE_1_S5_R2_001.fastq.gz RPE_2_S6_R2_001.fastq.gz | sort | uniq -c

real	0m3.725s
user	0m4.009s
sys	0m0.421s

// -k is to keep the order same of files in output
time parallel -k -j 30 'zgrep -o -F -m 1000 -e GTGCATGA {} | sort | uniq -c' ::: RPE_1_S5_R2_001.fastq.gz RPE_2_S6_R2_001.fastq.gz

real	0m2.022s
user	0m4.026s
sys	0m0.527s

### all parameters

time parallel -k -j 30 'zgrep -o -F -m 1000 -e GTGCATGA -e TGTTGGAG -e GACATACG -e GAGTAACG -e GAGAGCAA -e GGTGTTAG -e ACGAACGA -e CGAAGCAA -e GTCCTGAA {} | sort | uniq -c' ::: RPE_1_S5_R2_001.fastq.gz RPE_2_S6_R2_001.fastq.gz RPE_3_S7_R2_001.fastq.gz > grep_result.txt

### final command (only dealing with the RPE files here)

time parallel -k -j 30 'zgrep -o -F -e GTGCATGA -e TGTTGGAG -e GACATACG -e GAGTAACG -e GAGAGCAA -e GGTGTTAG -e ACGAACGA -e CGAAGCAA -e GTCCTGAA {} | sort | uniq -c' ::: RPE_1_S5_R2_001.fastq.gz RPE_2_S6_R2_001.fastq.gz RPE_3_S7_R2_001.fastq.gz > grep_result.txt


# The right command/s

## -o : print only matching part of lines, -m : stop after finding those many instances
command:
time grep -o -e GTGCATGA -e TGTTGGAG RPE_1_S5_R2_001.fastq | sort | uniq -c

output:
 93264 GTGCATGA
205972 TGTTGGAG

time: 
real	9m49.021s
user	1m46.223s
sys	    0m30.417s

## The patterns (After removing empty named ones. I am gonna focus on them only):

GTGCATGA	1,029,270	42.84	AAV92YF		GTGCATGA	868,583	37.56	AAV92YF     948,926
TGTTGGAG	365,845	    15.23	Rh10		TGTTGGAG	378,761	16.38	Rh10        372303 
GACATACG	293,252	    12.21	ATX002		GACATACG	274,134	11.85	ATX002      283693 
GAGTAACG	138,779	    5.78	ATX001		GAGTAACG	154,330	6.67	ATX001      146,554
GAGAGCAA	127,729	    5.32	AAV9		GGTGTTAG	124,826	5.40	7m8         126,277
GGTGTTAG	102,580	    4.27	7m8		    GAGAGCAA	112,390	4.86	AAV9        107485 
ACGAACGA	88,528	    3.69	AAV2		CGAAGCAA	89,246	3.86	AAV8        88887  
CGAAGCAA	66,618	    2.77	AAV8		ACGAACGA	80,863	3.50	AAV2        73,740 
GTCCTGAA	484	        0.02	AAV6		GTCCTGAA	494	    0.02	AAV6        489    

# final commands

## to find all the patterns of interest in just the RPE_1_S5_R2_001.fastq file.

`time grep -o -e GTGCATGA -e TGTTGGAG -e GACATACG -e GAGTAACG -e GAGAGCAA -e GGTGTTAG -e ACGAACGA -e CGAAGCAA -e GTCCTGAA RPE_1_S5_R2_001.fastq | sort | uniq -c`

## final command (only dealing with the RPE files here)

time parallel -k -j 30 'zgrep -o -F -e GTGCATGA -e TGTTGGAG -e GACATACG -e GAGTAACG -e GAGAGCAA -e GGTGTTAG -e ACGAACGA -e CGAAGCAA -e GTCCTGAA {} | sort | uniq -c' ::: RPE_1_S5_R2_001.fastq.gz RPE_2_S6_R2_001.fastq.gz RPE_3_S7_R2_001.fastq.gz > grep_result.txt

## for the 4 files like: Ret_1_S1_R2_001.fastq.gz 

time parallel -k -j 30 'zgrep -o -F -e GTGCATGA -e TGTTGGAG -e GACATACG -e GAGTAACG -e GAGAGCAA -e GGTGTTAG -e ACGAACGA -e CGAAGCAA -e GTCCTGAA {} | sort | uniq -c' ::: Ret_1_S1_R2_001.fastq.gz Ret_2_S2_R2_001.fastq.gz Ret_3_S3_R2_001.fastq.gz Ret_4_S4_R2_001.fastq.gz > grep_result_Ret.txt

(took around 7 mins)

