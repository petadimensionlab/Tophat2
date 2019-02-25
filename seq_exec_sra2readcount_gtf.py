import os

refdb = 'hg38' # hg19 / mm9 / mm10
is_pairend = 'yes'
is_sra = 'yes'

is_qualitycheck = 'yes'
is_trimming = 'yes'
is_delete_FASTQ = 'no'
core_num = str(8) # core number
gtf_file = refdb+'.gtf'

fr = open('samplelist.csv','r').readlines()
fr.pop(0) # remove header
for line in fr:
    line = line.replace('\n','')
    lst = line.split(',')
    item = lst[0]
    input_dir = lst[1]
    output_dir = lst[2]
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    msg = '%s is now processing...' % (item)
    print( msg )
    cmd = 'python exec_sra2readcount_gtf.py %s %s %s %s %s %s %s %s %s %s %s' % (is_sra,is_pairend,is_qualitycheck,is_trimming,is_delete_FASTQ,refdb,item,core_num,gtf_file,input_dir,output_dir)
    print( cmd )
    os.system(cmd)
