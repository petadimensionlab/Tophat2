rm( list=ls(all=TRUE) ) # clean up R workspace

library(Rsubread)
library(edgeR)
args <- commandArgs(trailingOnly=T)

gtf_db <- args[1] # mm9
sampleID <- args[2] # sample ID
core_num <- args[3] # core number
iodir <- args[4] # input directory

print(gtf_db)

inputfile <- paste(iodir,"/accepted_hits.bam",sep="")
fc <- featureCounts(files=inputfile,annot.ext=gtf_db,isGTFAnnotationFile=TRUE,GTF.featureType="exon",GTF.attrType="gene_id",nthreads=core_num)
## save gene-symbol and read cound file ##
setwd(iodir)
sfn <- paste(sampleID,"_rc.txt",sep="")
write.table(fc$counts,file=sfn,quote=F,col.names=F,sep="\t")

x <- DGEList(counts=fc$counts,genes=fc$annotation[,c("GeneID","Length")])
rpkm <- rpkm(x,fc$genes$Length)
sfn <- paste(sampleID,"_rpkm.txt",sep="")
write.table(rpkm,file=sfn,quote=F,col.names=F,sep="\t")
