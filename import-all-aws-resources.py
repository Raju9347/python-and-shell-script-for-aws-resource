import boto3
import csv

def get_resources_by_tags(tag_key, tag_value):
    client = boto3.client('resourcegroupstaggingapi', region_name='us-east-1')  # Specify your region

    response = client.get_resources(
        TagFilters=[
            {
                'Key': tag_key,
                'Values': [tag_value]
            }
        ]
    )

    resources = response['ResourceTagMappingList']
    return resources

def main():
    tag_key = 'application'
    tag_value = 'soo'
    resources = get_resources_by_tags(tag_key, tag_value)

    with open('resources.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Resource ARN', 'Resource Name', 'Owner'])

        for resource in resources:
            resource_arn = resource['ResourceARN']
            tags = {tag['Key']: tag['Value'] for tag in resource['Tags']}
            resource_name = tags.get('resourcename', 'N/A')
            owner = tags.get('Owner', 'N/A')
            writer.writerow([resource_arn, resource_name, owner])
            print(f"Resource ARN: {resource_arn}")
            print(f"Resource Name: {resource_name}")
            print(f"Owner: {owner}")
            print("-" * 40)

    print("The resources have been written to resources.csv")

if __name__ == "__main__":
    main()
