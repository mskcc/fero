Edit config.ini file with relevant paths

Run 

```
python3 process_files.py config.ini
```


Note

Before running process_files.py, the following are assumed:

    1) The paths are in /juno/archive/msk/cmo/ci/manual_projects/
        - If not, you must 
            - mkdir the main dir, based on ProjectName in request file
            - copy the MPGR files into the main dir
            - copy the fastq files into the newly-created dir
        - Also make sure the mapping file paths are updated to reflect these changes
    2) Each sample has a barcode
        - If not, you have to create them:
            - NDS one-liner
                If
                    FASTQ == path to the FASTQ file
                Then
                    BARCODE=$(zcat $FASTQ | head -1 | sed 's/.*://')
            - OR make one up as a last resort; the pipelines don't seem to use them
