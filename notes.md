anything like `this`, which doesnt look like code, is probably a quote from a paper (context can be understood from above few lines of it).

01-12-24

Reading the paper on scAAVenger. Got to know that in CRISPR, it is better to insert the Cas9 protein's gene in the cell-to-be-corrected rather than giving the preformed protein. This is because then we can modulate the Cas9 expression much better and hence when the gene-cutting will happen. Also it is difficult to store preformed protein. Insertion of Cas9 can be effectively done using viral vectors, like AAVs (Adeno-associated viruses).


Need to figure out why marker gene finding is important in the cells-
`The scAAVengr pipeline can be applied to any species or tissue for which marker genes can be identified, however, as demonstrated here through screening performed in mouse brain, heart, and liver following systemic injections of pooled AAV library.`

01-13-24

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

01-14-23

I found the data from the paper, and I am gonna try to follow the steps of processing (and preprocessing, which will require more resources) the scRNAseq data. 

step1. will be to try and see how the AAV barcodes were found out in the reads (Salmon was used for this). Need to ask questions from Aman regarding this if it doesn't make sense. So need to first understand usage of Salmon.

step2. will be to begin with the processed gene abundances and perform on them, all the steps which were performed to find out the celltypes for each cell. This was done using Scanpy.

Day end-  I installed salmon using Docker (basically pulled its image) as coudnt run the binary because it was made for linux and conda install also didnt work because of my outdated conda. 
Next step is to use the docker image of salmon to process files (Still on step 1).

01-15-23

i tried to run a docker container (in interactive mode) and was able to do that and check installation of salmon successfully. Now, I need to understand the command which was used to quantify the transcripts. Basically, in the GEO page, they have provided a barcodes file and another file, which says that in the barcodes file, which ones are the AAV barcodes.
So what I was thinking is that the AAV barcodes would be a part of the transcripts.fa file, so that those barcodes would be recognized as some genes in the cells (datapoints), and we would be able to identify which cells were infected by which AAVs. But apparently they have made those barcodes a part of the barcodes file, which contains the identifiers for the cells, but I dont know how it works that way, and how to run Salmon according to this input format.

01-18-23

Updates from the last few days:
I got access to the github repo of the scAAVengr pipeline.
Made account on ACCESS for access to HPCs.

About the doubt regarding how presence of AAVs were found in the sequenced data, I still have to figure that out. 
