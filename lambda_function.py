import json
import os
import timeit
import boto3


#TAG_START_NAME = os.environ["ENV"]


instanciasiniciadas=""
def get_cluster(teste="N"):
    rds_client_get = boto3.client("rds",region_name="sa-east-1")
    responseget = rds_client_get.describe_db_clusters() 
    resposta = "Nenhuma instancia iniciada"   
    for info in responseget["DBClusters"]:
        clustername = info['DBClusterIdentifier']
        statuscluster = get_status(clustername)
        if statuscluster == "stopped" and teste == "N":
            arn = info['DBClusterArn']
            valortag = list_tags_for_resource(arn)
            if valortag == "True":
                resposta  = action_cluster(clustername)  
        if teste=="S":
                resposta  = action_cluster(clustername,"S")                   
    return resposta


def get_status(clusternameconsulta):
    rds_client_get = boto3.client("rds",region_name="sa-east-1")
    responseget = rds_client_get.describe_db_clusters()
    for info in responseget["DBClusters"]:
        clustername = info['DBClusterIdentifier']
        if clustername == clusternameconsulta:
            statuscluster = info['Status']
    return statuscluster

def get_arn(clusternameconsulta):
    rds_client_get = boto3.client("rds",region_name="sa-east-1")
    responseget = rds_client_get.describe_db_clusters()
    for info in responseget["DBClusters"]:
        clustername = info['DBClusterIdentifier']
        if clustername == clusternameconsulta:
            arn = info['DBClusterArn']
    return arn

def list_tags_for_resource(arn, teste = "N"):
    if teste == "S":
        return "True"
    rds_client_get = boto3.client("rds",region_name="sa-east-1")    
    tags = rds_client_get.list_tags_for_resource(
        ResourceName=arn,
    )['TagList']

    for tag in tags:
        if tag["Key"] == "TAG_START_NAME":
            if tag["Value"] == "True":
                valortag = tag["Value"]
    return valortag


def action_cluster(clustername, teste="N"): 
    if teste == "S":
        return(clustername)
    else:
        rds_client = boto3.client("rds",region_name="sa-east-1") 
        response = rds_client.start_db_cluster(DBClusterIdentifier = clustername)
        global instanciasiniciadas
        instanciasiniciadas = instanciasiniciadas + " " + clustername
        return response




def main() -> None:
    get_cluster()

def lambda_handler(event, context):  
    main()
    return{"statuscode": 200, "body":json.dumps(""), "Instâncias Iniciadas: ": instanciasiniciadas}

if __name__ == "__main__":
    start = timeit.default_timer()
    lambda_handler(None,None)
    end = timeit.default_timer()
    print("Time: %f" % (end - start))

