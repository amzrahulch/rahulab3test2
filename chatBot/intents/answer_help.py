import random
import json
import boto3

class AnswerHelp:
    def __init__(self,intent_request):
        self.intent_request = intent_request

    def execute(self):
        question = self.intent_request['inputTranscript'].lower()
        response = ""

        #emr
        if len(response) < 1:
            for h in ['emr','what is emr']:
                if h in question:
                    response = "Amazon EMR is the industry-leading cloud big data platform for processing vast amounts of data using open source tools such as Apache Spark, Apache Hive, Apache HBase, Apache Flink, Apache Hudi, and Presto. Amazon EMR makes it easy to set up, operate, and scale your big data environments by automating time-consuming tasks like provisioning capacity and tuning clusters."

        #annotation
        if len(response) < 1:
            for h in ['annotation','define annotation']:
                if h in question:
                    response = "DNA annotation or genome annotation is the process of identifying the locations of genes and all of the coding regions in a genome and determining what those genes do."

        #genome sequencing
        if len(response) < 1:
            for h in ['emr','what is genome sequencing']:
                if h in question:
                    response = "The sequence tells scientists the kind of genetic information that is carried in a particular DNA segment."

        #variant
        if len(response) < 1:
            for h in ['emr','what is a variant']:
                if h in question:
                    response = "An alteration in the most common DNA nucleotide sequence. The term variant can be used to describe an alteration that may be benign, pathogenic, or of unknown significance."

        return response
