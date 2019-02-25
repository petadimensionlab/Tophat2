import os, sys, shutil

argvs = sys.argv
argc = len(argvs)
if argc!=12:
    msg = 'Usage: # python %s <is_sra: yes or no> <is_pairend: yes or no> <is_qualitycheck: yes or no> <is_trimming: yes or no> <is_delete_FASTQ: yes or no> <reference-db> <sample-ID> <core-number> <gtf-file> <input-directory> <output-directory>' % (argvs[0])
    print( msg )
    quit()

## args ##
is_sra = argvs[1] # check the type of input-data (sra or fastq)
is_pairend = argvs[2]
is_qualitycheck = argvs[3]
is_trimming = argvs[4]
is_delete_FASTQ = argvs[5]
refdb = argvs[6] # mm9
sampleID = argvs[7]
core_num = argvs[8] # core number
gtf_file = argvs[9]
input_dir = argvs[10]
output_dir = argvs[11]

## directories ##
ws_dir = os.getcwd()
#input_dir = os.path.join(ws_dir,'input')
#output_dir = os.path.join(ws_dir,'output')
sample_dir = os.path.join(output_dir,sampleID)

## create a directory for given sample ID ##
if os.path.exists(sample_dir):
    msg = 'Directory %s already exists.' % (sampleID)
    print( msg )
else:
    os.mkdir(sample_dir)

## tools ##
tool_dir = '/Users/petadimensionlab/ws/apps/sra2rc/tools'
bowtie2_indexes = os.path.join(tool_dir,'bowtie2/indexes/'+refdb)
fastq_dump = os.path.join(tool_dir,'sratoolkit/bin2/fastq-dump')
fastqc = os.path.join(tool_dir,'FastQC/fastqc')
Trimmomatic_dir = os.path.join(tool_dir,'Trimmomatic')
bowtie2dir = os.path.join(tool_dir,'bowtie2')
tophat2 = os.path.join(tool_dir,'tophat/tophat2')
bam2rc = '%s/exec_bam2readcount_gtf.R' % (tool_dir)

## GTF ##
gtfdir = '/Users/petadimensionlab/ws/apps/sra2rc/gtf'
gtf = os.path.join(gtfdir,gtf_file)

#### Execution ####
#sample_PATH = os.path.join(input_dir,sampleID)
os.chdir(sample_dir)


## 3rd step : Tophat ##
msg = '%s : tophat2...' % (sampleID)
print( msg )
options = '-p %s -o %s %s' % (core_num,sample_dir,bowtie2_indexes)
if is_pairend =='yes':
    if is_trimming == 'yes':
        fastq1 = '%s_R1_trim_paired.fastq.gz' % (sampleID)
        fastq2 = '%s_R2_trim_paired.fastq.gz' % (sampleID)
    else:
        fastq1 = '%s_1.fastq.gz' % (sampleID)
        fastq2 = '%s_2.fastq.gz' % (sampleID)
    cmd = 'export PATH=$PATH:%s && %s %s %s %s' % (bowtie2dir,tophat2,options,fastq1,fastq2)
else:
    if is_trimming == 'yes':
        fastq = '%s_trim.fastq.gz' % (sampleID)
    else:
        fastq = '%s.fastq.gz' % (sampleID)
    cmd = 'export PATH=$PATH:%s && %s %s %s' % (bowtie2dir,tophat2,options,fastq)
    #print( cmd )
os.system(cmd)

## 4th step : Extract read count from bam file ##
msg = '%s : Bam to read count...' % (sampleID)
print( msg )
cmd = 'R --vanilla --slave --args %s %s %s %s < %s' % (gtf,sampleID,core_num,sample_dir,bam2rc)
#print cmd
os.system(cmd)

## 5th step : Delete copied FASTQ file ##
if is_delete_FASTQ == 'yes':
    os.chdir(sample_dir) # confirm that we are in the output directory
    msg = '%s : Delete copied/dumped FASTQ files...' % (sampleID)
    print( msg )
    if is_pairend =='yes':
        fastq1 = '%s_1.fastq.gz' % (sampleID)
        fastq2 = '%s_2.fastq.gz' % (sampleID)
        cmd = 'rm %s %s' % (fastq1,fastq2)
    else:
        fastq = '%s_1.fastq.gz' % (sampleID)
        cmd = 'rm %s' % (fastq)
    os.system(cmd)

## finish ##
msg = '%s : finish!' % (sampleID)
print( msg )
os.chdir(ws_dir)
