import boto3

# Test the connection
client = boto3.client("sts")
response = client.get_caller_identity()
print(response)
#expect your Userid, Account, and ARN
rekognition = boto3.client("rekognition", region_name="ap-southeast-1")
response2 = rekognition.list_collections()
print(response2)
#expect an empty list {"CollectionIds": [] }