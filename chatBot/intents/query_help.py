import random
import json
import boto3
import time

class QueryHelp:
    def redshift_execute(self,sampleid_,sql):
        print("sampleid_",sampleid_)
        client_rs = boto3.client('redshift-data',region_name='us-east-1')
        cluster = "redshift-cluster-1"
        database = "dev"
        user = "dataapiuser"
        result=client_rs.execute_statement(ClusterIdentifier=cluster, Database=database, DbUser=user, Sql=str(sql))
        time.sleep(5)
        response=client_rs.get_statement_result(Id=result["Id"])['Records'][0][0]['longValue']
        time.sleep(5)
        print("hi",response)

        return response

    def athena_execute(self,sampleid_,sql):
        client_athena = boto3.client('athena',region_name='us-east-1')
        print(str(sql))
        athenaQuery=client_athena.start_query_execution(QueryString=str(sql),ResultConfiguration={'OutputLocation':'s3://rahulab3/athena_output/'})
        time.sleep(5)
        print("athenaQuery",athenaQuery)
        response=client_athena.get_query_results(QueryExecutionId=athenaQuery['QueryExecutionId'])['ResultSet']['Rows'][1]['Data'][0]['VarCharValue']
        time.sleep(5)
        print("hi",response)

        return response

    def execute(self):
        intent_request = self.intent_request
        question = self.intent_request['inputTranscript'].upper()
        queryEng = self.intent_request['currentIntent']['slots']['queryEngine'].upper()
        sampleid_= self.intent_request['currentIntent']['slots']['sampleid'].upper()
        rs_sql="select count(1) from ab3.var_part_by_sample_2 as v where v.partition_0 = '" + sampleid_ + "';"
        athena_sql="select count(1) from var_part_by_sample_2 as v where v.partition_0 = '" + sampleid_ + "';"
        if queryEng=='REDSHIFT':
            print("queryEng",queryEng,sampleid_)
            response=self.redshift_execute(sampleid_,rs_sql)
            print("response",response)
        elif queryEng=='ATHENA':
            response=self.athena_execute(sampleid_,athena_sql)

        return response

    def __init__(self,intent_request):
        self.intent_request = intent_request
