
import unittest
from lambda_function import action_cluster, list_tags_for_resource
import boto3
import mock
import os
from moto import mock_rds2

nomecluster = ""
arn = ""
@mock.patch.dict(os.environ,{'ENV': "mytemp"})
@mock_rds2
class TestActionCluster(unittest.TestCase):
    def test_action_cluster(self):
        mock_lambda_handler()
        global nomecluster
        import lambda_function      
        self.assertEqual(lambda_function.action_cluster(nomecluster,'S'),nomecluster)
    
    def test_get_arn(self):
        global arn
        import lambda_function      
        self.assertEqual(lambda_function.get_arn(nomecluster),arn)

    def test_get_status(self):
        global nomecluster
        import lambda_function      
        self.assertEqual(lambda_function.get_status(nomecluster),"available")

    def test_list_tags_for_resource(self):
        global arn
        import lambda_function      
        self.assertEqual(lambda_function.list_tags_for_resource(arn, "S"),"True")

    def test_get_cluster(self): 
        import lambda_function      
        self.assertEqual(lambda_function.get_cluster("S"),"db-master-1")


def mock_lambda_handler():
    client = boto3.client('rds',region_name='sa-east-1')
    client.create_db_cluster(
        BackupRetentionPeriod=1,
        CharacterSetName="profilex",
        OptionGroupName="profilex",
        AvailabilityZones=["sa-east-1b"],
        Tags=[{'Key': "testes",'Value': "testes"}],        
        CopyTagsToSnapshot=False,
        DBClusterParameterGroupName='default.aurora',
        DBSubnetGroupName='profilex',
        DeletionProtection=False,
        EnableIAMDatabaseAuthentication=False,
        EngineVersion='5.7.mysql_aurora.2.10.0',
        Engine='aurora-mysql',
        KmsKeyId="arn:teste",
        MasterUsername ="root",
        MasterUserPassword='hunter2',
        PreferredBackupWindow="01:00-03:00",
        PreferredMaintenanceWindow="sun:06:00-sun:07:00 UTC",
        StorageEncrypted=False,
        VpcSecurityGroupIds= ["454s8d8de"],
        DBClusterIdentifier='db-master-1',
        DatabaseName='staging-aurora',
        Port=8085
    )
    rds_client_get = boto3.client("rds",region_name="sa-east-1")
    responseget = rds_client_get.describe_db_clusters()    
    global nomecluster 
    global arn
    for info in responseget["DBClusters"]:
        nomecluster = info['DBClusterIdentifier']
        arn = info['DBClusterArn'] 
    with mock.patch("boto3.client") as mock_client:
        mock_client.return_value = client
        print(mock_client.return_value)



# if __name__ == "__main__":
#     unittest.main()





