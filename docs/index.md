# FastQCParser

## FastQCParser User Guide:

***
It is recommended to open this via browser: <a href="https://ms2206.github.io/FastQCParser">User Guide</a>
***

## Introduction
A Python program to parse FastQCtext files, and generate reports and plots.

1. Clone directory: `git clone https://github.com/ms2206/FastQCParser.git`
2. Make a new python environment based from requirments.yaml `conda env create -f requirements.yaml --<NAME>`
3. Load environment <NAME> env. `conda activate <NAME>`
4. Change directory into FastQCParser
5. Example Usage: `python3 src/main.py data/raw/fastqc_data2.txt fastqc_2 -a`

-- plots are downloaded to the users `~/Downloads/` folder.
***
## Set up
Example Usage:
With python3, run executable found at `src/main.py`.

Pass `data/raw/fastqc_data2.txt` (or any fastqc file) - as input file, and `fastqc_2` as
output directory (or use a customer directory name).

Use optional argument `-a`.

`python3 src/main.py <FASTQ FILE> <DIR_NAME> [<OPTIONAL_ARGS>]`

`python3 src/main.py data/raw/fastqc_data2.txt fastqc_2 -a`

<img src="process_flow/FastQCParser - Set up.svg" alt="FastQCParser Process Flow" width="20000px">

***
## Optional Args
Help and misc information provided by ArgeParse for optional arguments.  

`python3 src/main.py -h`

<img src="process_flow/FastQCParser - PF.svg" alt="FastQCParser Process Flow" width="20000px">

***
## Example Plots
### Adapter Content
Plot's adapter content by position.
<img src="example_img/adap_cont_plot.png" alt="adap_cont_plot" width="1000px">

### Kmer Content
Plot's kmer content by position.
<img src="example_img/kmer_cont_plot.png" alt="kmer_cont_plot" width="1000px">

### Overrepresented sequences
Plot's Per base N content.
<img src="example_img/per_base_N_cont_plot.png" alt="per_base_N_cont_plot" width="1000px">

### Per base sequence content
Plot's Per base sequence content.
<img src="example_img/per_base_seq_content_plot.png" alt="per_base_seq_content_plot" width="1000px">

### Per sequence quality scores
Plot's Per sequence quality scores.
<img src="example_img/per_base_seq_qual_plot.png" alt="per_base_seq_qual_plot" width="1000px">

### Per sequence GC content
Plot's Per sequence GC content.
<img src="example_img/per_seq_GC_cont_plot.png" alt="per_seq_GC_cont_plot" width="1000px">

### Per sequence quality scores
Plot's Per sequence quality scores.
<img src="example_img/per_seq_qual_scores_plot.png" alt="per_seq_qual_scores_plot" width="1000px">

### Per tile sequence quality
Plot's Per tile sequence quality.
<img src="example_img/per_tile_seq_qual_plot.png" alt="per_tile_seq_qual_plot" width="1000px">

### Sequence Duplication Levels
Plot Sequence Duplication Levels.
<img src="example_img/seq_dup_plot.png" alt="seq_dup_plot" width="1000px">
***
## GitHub
<https://github.com/ms2206/FastQCParser.git>