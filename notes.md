# My proceedings from the Gene-Therapy project under Professor Leah Byrne.

## 

### 01-12-24

Reading the paper on scAAVenger. Got to know that in CRISPR, it is better to insert the Cas9 protein's gene in the cell-to-be-corrected rather than giving the preformed protein. This is because then we can modulate the Cas9 expression much better and hence when the gene-cutting will happen. Also it is difficult to store preformed protein. Insertion of Cas9 can be effectively done using viral vectors, like AAVs (Adeno-associated viruses).

Need to figure out why marker gene finding is important in the cells-
`The scAAVengr pipeline can be applied to any species or tissue for which marker genes can be identified, however, as demonstrated here through screening performed in mouse brain, heart, and liver following systemic injections of pooled AAV library.`

### 01-13-24

I read yesterday about how those guys preprocessed and processed the scRNA sequencing data, which ultimately led to the identification of the celltypes of the sequenced cells. 
However, I was wondering how they figured out the infection by AAVs in these cells. That part was below the sequencing analysis parts.

question:
- They call the AAV barcodes as `AAV variant-mediated GFPbarcode`. Why would they put GFP in the barcode?

So apparently they quantified the AAV infections (by infections, I mean: some AAV infected some cell) using two methods (and later on did the union of the infections found). The two methods were: 
- from scRNA seq data 
- from some method involving PCR amplification (will look into this later, after understanding method1 well)

the AAV infection quantification from scRNA seq data was done using Salmon transcript quantification, followed by finding out the reads with the AAV barcodes present.

question:
- If Salmon does transcript quantification, then after using it, they would have just ended up with the quantifications of the transcripts no, how did they figure out the number of reads with the different AAVs?

Need to know about GC bias and how AAVs infect cells.

### 01-14-24

I found the data from the paper, and I am gonna try to follow the steps of processing (and preprocessing, which will require more resources) the scRNAseq data. 

step1. will be to try and see how the AAV barcodes were found out in the reads (Salmon was used for this). Need to ask questions from Aman regarding this if it doesn't make sense. So need to first understand usage of Salmon.

step2. will be to begin with the processed gene abundances and perform on them, all the steps which were performed to find out the celltypes for each cell. This was done using Scanpy.

Day end-  I installed salmon using Docker (basically pulled its image) as coudnt run the binary because it was made for linux and conda install also didnt work because of my outdated conda. 
Next step is to use the docker image of salmon to process files (Still on step 1).

### 01-15-24

i tried to run a docker container (in interactive mode) and was able to do that and check installation of salmon successfully. Now, I need to understand the command which was used to quantify the transcripts. Basically, in the GEO page, they have provided a barcodes file and another file, which says that in the barcodes file, which ones are the AAV barcodes.
So what I was thinking is that the AAV barcodes would be a part of the transcripts.fa file, so that those barcodes would be recognized as some genes in the cells (datapoints), and we would be able to identify which cells were infected by which AAVs. But apparently they have made those barcodes a part of the barcodes file, which contains the identifiers for the cells, but I dont know how it works that way, and how to run Salmon according to this input format.

### 01-18-24

Updates from the last few days:
I got access to the github repo of the scAAVengr pipeline.
Made account on ACCESS for access to HPCs.

About the doubt regarding how presence of AAVs were found in the sequenced data, I still have to figure that out. 

So looking at the github repo, I see that in the step where they are making the AAV (GFP) vs Cell matrix, they are taking as input a file with name like: LB1_BYR819A1_S1_R2_001.subgfp.seqkitlocate.txt.

Hence, next task: know more about seqkit and what this file would possibly contain. Also need to clarify what is the deal with this GFP thing with AAV.

Later tasks: read the single cell best practices given at the bottom of the repository Readme.

### 01-19-24

### 01-29-24

- Met with Aman and got to know how to join the CRC (Pitt cluster). And also within that, in which folder do I have storage (it was something like /bgfs/lbyrne/shashkat, though I am not exactly sure of the first folder). Also we connect to the htc server rather than h2p. Important link: https://crc.pitt.edu/getting-started/accessing-cluster
- Discussed that initially, just doing QC with Fastqc would be sufficient. 
- Also looked into the box folder shared by Ally.
- Aman showed me examples of how he runs scripts on the cluster.
- Also he is currently trying to get me access to the other cluster (I think PSC), as we have credits there and it has more functionalities.
- I can go through the slurm documentation he provided me with.

### 02-05-24

- Aman got access to the PSC cluster. My already existing ACCESS id can be used to get me allocation.
- I am gonna look into the data for now and do qc using fastqc.
- I initially looked at the fastqc results of the two reads from Brain tissue. 
My initial thoughts: 
    - why are the reads in file 1 so short (only 28bp), and in the file 2, there are some reads which are longer (28-90bp).
    - there are certain overrepresented sequences in the second read file (they are likely adapter sequences, as source is: 'Clontech SMARTer II A Oligonucleotide')
    - Per tile sequence quality: I dont understand how the different cells have different values of position in read. How are the 2d dimensions of flow cell covered like this?
    - In the starting of per base sequence content, the lines are shaky, indicating position related bias of nucleotides. But I am not sure if my inference is correct. Professor Mcmanus said that its probably fine.

### 02-06-24

- To do: understand why the reads are the way they are (one long one short). 
- But before that, I read a bit about why the initial few bases in reads have nucleotide-bias. This is because when the primers (next point) are attached to the mRNA (or fragments of mRNA) initially, for reverse transcription, they show a preference for certain starting sequences. But for later nucleotides, the nucleotide bias balances out pretty much. This is because even though the primers have certain binding preferences, those sequences may occur many times in the RNA molecules and the composition of ATCG in later nucleotides will be more balanced. 
- the primers used to initiate reverse transcription are random hexamers.

Need to process the raw reads to get h5ad files of cell-gene expression and do qc on them.

So the thing is, to process the files according to the proper protocol, I will need to have access to the cluster, because there are many programs which will be required to follow the pipeline they have told about in the paper. So for now, for the initial qc estimation, I can use kallisto and obtain the h5ad files and do qc on them using scanpy.

So when i run kb-quant command, the gene-expression matrices produced will automatically be filtered of low quality cells and transcripts. This is done by bustools in the background. Hence I can estimate the quality of the original raw data also by the number of cells/transcripts that remain after this.

Need to know species so that I can download the right genome for creating index!! (Assuming mouse for now)

for some time, figured kb-python installation as its latest version (0.28.2) was giving problems. Version 0.27.3 worked.

command for quantification (run from data/box_data/PGTB_Library_08_11_23 folder):

kb count -i ../../references/mouse/index.idx -g ../../references/mouse/t2g.txt -x 10xv2 -t 8 -o kallisto_output --h5ad \
fastqs/Brain_3_S5_R1_001.fastq.gz \
fastqs/Brain_3_S5_R2_001.fastq.gz

At end of day, I did get the kallisto results, but scanpy is not able to read the file and says that it has multiple genomes. So the next first thing is to clarify the species.

### 02-07-24

Gonna operate on the cluster today. Will begin with quantification of the AAVs.

for some reason installing kb-python using pip install didnt install it in the conda env directory, but in this location: /ihome/lbyrne/shashkat/.local/lib/python3.8/site-packages

command run on cluster (from the fastqs folder within PGTB_Library_08_11_23, with the human reference genome index files just inside the data folder)

kb count -i ../../index.idx -g ../../t2g.txt -x 10xv2 -t 8 -o kallisto_human_ref_output --h5ad \
fastqs/Brain_3_S5_R1_001.fastq.gz \
fastqs/Brain_3_S5_R2_001.fastq.gz

gave some error, which i didnt look into, as i realized for the meeting's results, i can just run it locally on the human ref.

kb count -i ../../references/human/index.idx -g ../../references/human/t2g.txt -x 10xv2 -t 8 -o kallisto_human_output --h5ad \
fastqs/Brain_3_S5_R1_001.fastq.gz \
fastqs/Brain_3_S5_R2_001.fastq.gz

able to process the adata.h5ad produced yesterday using kallisto (the species is mp mouse, as aligning with that yielded ~650 cells but with human around 150). Took some time to find out nomenclature of mouse mito, hb, rb genes. This is needed for qc.

kb count -i ../../references/mouse/index.idx -g ../../references/mouse/t2g.txt -x 10xv3 -t 8 -o kallisto_mouse_output_brain --h5ad \
fastqs/Brain_3_S5_R1_001.fastq.gz \
fastqs/Brain_3_S5_R2_001.fastq.gz

Ask in the github issue of kb-python, that kallisto documentation says to supply only one sample of fastqs at a time. Is it the same with kb-python? or does it deal with multiple samples given to the kb quant command at once?

### 02-15-24

question for aman- 

what is batch system (PSC)- if got the following error upon running STAR.

pid 2814004 (STAR) killed: rss memory 12292.08 MB exceeded limit 11264 MB
Computations using more than 1800 cpu seconds
and/or 11264 MB of memory should use the batch system.

### 02-21-24

Need to transfer files from box to psc. Trying out installing rclone for that. Some problem in running 

command run to create salmon index for mouse: (pwd: /ocean/projects/tra240003p/skatiyar) 
salmon index --transcripts salmon_index/mouse/gencode.vM34.transcripts.fa.gz --kmerLen 31 --index salmon_index/mouse --gencode

- I need to also generate a decoy aware index the next time

sbatch -o `pwd`/OUT_ERR/salmon_gfp_quant_%j.out  psc_specific/salmon_gfp.sh \
    -p `pwd` \
    -d fastqs/ \
    -n Brain_3_S5 \
    -r salmon_index/mouse

### 02-28-24

- finally the PGTB_eye data (the new dataset) is on my PSC.
- I am gonna run a simple grep command to find out the presence of AAV barcodes in the files for now.

### 02-29-24

I have put the grep commands, and the related progress in the file: finding_AAVs/grep_commands.md

- To do: 
    - process the raw fastqs using cellranger (by thoroughly following the cellranger documentation)
    - Quantify AAVs properly in the second data samples.

- REMEMBER TO CITE GNU PARALLEL IF ANY PUBLICATION HAPPENS

### 03-03-24

- trying out the grep command on the other files (eariler had tried on the RPE files but the results were a bit strange esp for the barcode which was in least amount, so testing on the 4 Ret files too).

- The command run was (extra information in finding AAVs/grep_commands):
time parallel -k -j 30 'zgrep -o -F -e GTGCATGA -e TGTTGGAG -e GACATACG -e GAGTAACG -e GAGAGCAA -e GGTGTTAG -e ACGAACGA -e CGAAGCAA -e GTCCTGAA {} | sort | uniq -c' ::: Ret_1_S1_R2_001.fastq.gz Ret_2_S2_R2_001.fastq.gz Ret_3_S3_R2_001.fastq.gz Ret_4_S4_R2_001.fastq.gz > grep_result_Ret.txt

- processing of the grep results in finding_AAVs/process_grep_results.ipynb file.

- If the results are still strange like the RPE ones, will have to think about why that could be (non-specific finding of the barcodes?). Then will move to the actual scripts for AAV barcode quantification.

- got the -f flag for grep command which can be used to specify the filename into which we need to look for the barcodes. Need to complete the other parts of the script.

### 03-04-2024

- made the script which will take the list of fastqs (in the form of a file) and the barcodes (again, in the form of a file) and produce the csv of the quantifications of the barcodes in each file. This csv can later be processed using the notebook in : finding_AAVs/process_grep_results.ipynb

- the command which was run to execute the script (from PGTB_library folder in psc):
`python grep_script/quantification_script.py grep_script/fastqs.txt grep_script/barcodes.txt grep_script/fastq_barcode_matrix.csv`

- an important correction which i made at this point: the resultant csv file had the barcode counts in sorted order, but the barcodes column didnt have barcodes in sorted order. Hence, changed the script appropriately.

- did the initial quantification successfully. The related files are stored in finding_AAVs/through_grep. 

- Ali asked me to do the quantifications of the bigger (extended) barcodes, because there was nonspecific finding of barcodes happening. However, my script till now was incapable of dealing with patterns having zero counts in the grep results. I modified to script (which involved using the -H option of grep) so that it could deal with patterns having zero count in grep. Validated intitial results on the RPE_1_S5_R2_001.fastq.gz file using manual grep command.

- sent the mail to Ali with the results for the longer barcodes.


