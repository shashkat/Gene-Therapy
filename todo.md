### 03-03-24

~~- write the script (quantification_script_grep.py) which will take the barcodes to process and the fastqs to grep into, and give out the final quantification results for the barcodes.~~
~~- use subprocess for the part where the shell command is to be run through the script.~~
- convert the grep script to use subprocess with shell=false rather than shell=true

### 03-04-24

- do the quantification of AAV barcodes in the second dataset using the standard scripts
- cleanup the data folder a bit
~~- need to modify the script so that i can give 0 counts for the barcodes with no amounts (probably modification needs to be done after the production of the grep_results just as they are now)~~
- figure out why the batch job I submitted earlier doesnt show up. Even after scontrol with the right job id (22757815), it doesn't show up now (but earlier it did).