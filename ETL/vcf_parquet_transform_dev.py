#pyspark script to convert VCF to parquet

import hail as hl
from bokeh.io import show, output_notebook
from bokeh.layouts import gridplot
from pprint import pprint
from  pyspark.sql.functions import col, lit
import os
import sys
from pyspark.sql import SparkSession
import subprocess

inputs = str(sys.argv[1]).split('#')
print(inputs)
sample_id=inputs[0].split(',')
pathparams=inputs[1].split(',')
year=pathparams[0]
month=pathparams[1]
week=pathparams[2]
hl.init()
spark = SparkSession.builder.getOrCreate()

for i in sample_id:
	print("for loop",i)
	filename = 's3://rahulab3test/dev_input_vcf/year=' + year + '/month=' + month + '/wk=' + week + '/' + i + '/' + i + '.hard-filtered.vcf.bgz'
	#if "additional_698_related" in filename:
	#	continue
	#else:
		#sample_id = os.path.basename(filename).replace(".hard-filtered.vcf.bgz","")
	#sample_id_=str(i.split('/')[-1].split('.')[0])
	vds=hl.import_vcf(filename,reference_genome='GRCh38')
	variant_table = vds.make_table()
	v_spark=variant_table.to_spark()
	v_spark_renamed=v_spark.toDF("locus.contig","locus.position","alleles","rsid","qual","filters",'info.AC','info.AF','info.AN','info.DB','info.DP','info.END','info.FS','info.FractionInformativeReads','info.LOD','info.MQ','info.MQRankSum','info.QD','info.R2_5P_bias','info.ReadPosRankSum','info.SOR',"AD","AF","DP","FIR2","F2R1","GP","GQ","GT.alleles","GT.phased","MB","PL","PRI","PS","SB","SQ")
	v_spark_renamed=v_spark_renamed.withColumn("sample_id",lit(i))
	v_spark_renamed=v_spark_renamed.withColumn('ref',v_spark_renamed.alleles[0]).withColumn('alt',v_spark_renamed.alleles[1])
	v_spark_renamed = v_spark_renamed.withColumnRenamed("locus.contig","chrom").withColumnRenamed("locus.position","pos")
	v_spark_renamed.createOrReplaceTempView("variant_v")
	df=spark.sql("SELECT SELECT concat(chrom, ':', ref, ':', alt, ':', cast(pos as string)) as variant_id,* FROM variant_v where length(chrom)<6")
	df.write.parquet('s3://rahulab3test/dev_output_parquet/'+i+'/')
