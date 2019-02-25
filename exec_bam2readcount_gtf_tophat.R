rm( list=ls(all=TRUE) ) # clean up R workspace

library(Rsubread)
library(edgeR)

gtf_db <- "/Users/petadimensionlab/ws/apps/sra2rc/gtf/hg38.gtf"
core_num <- 4
iodir <- "/Users/petadimensionlab/Downloads/test_star0123/SRR1531314/"

#cdir <- getwd()
#tbln <- "../samplelist.csv"
#tbl <- read.table(tbln,sep=",",header=T)
#sIDs <- tbl$filename
sID <- "SRR1531314"

#for (sID in sIDs) {
  inputfile <- paste(iodir, "SRR1531314.Aligned.toTranscriptome.out.bam",sep="")
  fc <- featureCounts(files=inputfile,annot.ext=gtf_db,isGTFAnnotationFile=TRUE,GTF.featureType="exon",GTF.attrType="gene_name",nthreads=core_num)
  ## save gene-symbol and read cound file ##
  output_dir <- iodir
  setwd(output_dir)
  sfn <- paste(sID,"_rc.txt",sep="")
  write.table(fc$counts,file=sfn,quote=F,col.names=F,sep="\t")
  
  x <- DGEList(counts=fc$counts,genes=fc$annotation[,c("GeneID","Length")])
  rpkm <- rpkm(x,fc$genes$Length)
  sfn <- paste(sID,"_rpkm.txt",sep="")
  write.table(rpkm,file=sfn,quote=F,col.names=F,sep="\t")
#}

