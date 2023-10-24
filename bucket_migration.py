import boto3
import json
import logging

# Setup logging
# Setup logging with a custom format including timestamps
logging.basicConfig(filename='tagging.log', 
                    level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s', 
                    datefmt='%Y-%m-%d %H:%M:%S')


required_tags = {
    "UUCode": "",
    "DelegationID": "",
    "MergerCandidate": "",
}

# Initialize a session using Amazon DynamoDB
session = boto3.session.Session(region_name='us-east-1')
s3 = session.client('s3')

def get_all_s3_buckets():
    # Function to get a list of all S3 buckets
    response = s3.list_buckets()
    return [bucket['Name'] for bucket in response['Buckets']]

def get_bucket_tags(bucket_name):
    # Function to get the tags of a specific bucket
    try:
        response = s3.get_bucket_tagging(Bucket=bucket_name)
        return {tag['Key']: tag['Value'] for tag in response['TagSet']}
    except s3.exceptions.from_code('NoSuchTagSet'):
        return {}

def update_bucket_tags(bucket_name, new_tags):
    # Function to update the tags of a specific bucket
    try:
        # Get existing tags
        existing_tags = get_bucket_tags(bucket_name)
        
        # Merge existing and new tags
        merged_tags = {**existing_tags, **new_tags}
        
        s3.put_bucket_tagging(
            Bucket=bucket_name,
            Tagging={
                'TagSet': [{'Key': k, 'Value': v} for k, v in merged_tags.items()]
            }
        )
    except Exception as e:
        logging.error(f"Failed to update tags for {bucket_name}: {e}")

def process_buckets(buckets):
    # Function to process a list of buckets
    updated_bucket_count = 0  # Initialize a counter for updated buckets
    for index, bucket in enumerate(buckets, start=1):
        print(f'Processing bucket {index} of {len(buckets)}: {bucket}')
        current_tags = get_bucket_tags(bucket)
        missing_tags = {k: v for k, v in required_tags.items() if k not in current_tags}
        if missing_tags:
            updated_tags = {**current_tags, **missing_tags}
            update_bucket_tags(bucket, updated_tags)
            logging.info(f"Updated tags for {bucket}: {json.dumps(updated_tags)}")
            updated_bucket_count += 1  # Increment the counter when a bucket is updated

    return updated_bucket_count  # Return the count of updated buckets

if __name__ == "__main__":
    # Main script execution
    all_buckets = get_all_s3_buckets()
    updated_count = process_buckets(all_buckets)
    summary_message = f'Script completed. {updated_count} of {len(all_buckets)} buckets updated.'
    print(summary_message)
    logging.info(summary_message)
