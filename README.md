# S3 Bucket Tag Migration Batch Script

## Overview
This is a master script to batch migrate and manage the tagging of AWS S3 buckets. The defult setup ensures that specific tags (`UUCode`, `DelegationID`, and `MergerCandidate`) are present on each bucket.  Change these values to suit your environment.  If any of these tags are missing from a bucket, the script will ADD each of them. Existing resource tags are maintained and stay intact.  Logging of operations is also integrated for tracking and troubleshooting purposes.

## Prerequisites
- **Python 3.x** installed.  
- **Boto3 library** installed. Boto3 is the Amazon Web Services (AWS) Software Development Kit (SDK) for Python. It allows Python developers to write software that makes use of services like Amazon S3 and Amazon EC2.
- AWS credentials set up either via environment variables, AWS configuration file, or IAM roles.

## How to Use

1. Ensure your AWS credentials are properly configured. You can either:
   - Set up the AWS credentials using `aws configure`.
   - Use environment variables.
   - Assign an IAM role (if running within AWS services like EC2).

2. Modify the `required_tags` dictionary in the script if you want to change or add new tags.

3. Run the script: python s3_bucket_tagging.py

4. Check the `tagging.log` file for logs and any potential errors.

## Features
- **Logging:** The script logs its operations to a file named `tagging.log`. This helps in tracking which buckets were updated and if there were any errors during the execution.
- **Bucket Listing:** Script displays the progress of execution on all S3 buckets.
- **Tag Verification & Update:** The script checks each bucket for the presence of the required tags. If any required tags are missing, the script will update the bucket with the missing tags.
- **Error Handling:** Proper error handling is implemented. If there's an issue updating the tags of a bucket, an error message will be logged.
- **Logging:** INFO/DEBUG mode.  Script actions are logged and summarized.
## Notes
- The script currently operates in the `us-east-1` region. If you wish to change this, modify the `region_name` parameter when initializing the session.
- The script assumes that the required tags (`UUCode`, `DelegationID`, and `MergerCandidate`) should be added with empty values if they're missing from a bucket. Update the `required_tags` dictionary if you need different default values.

## Contribution
Feel free to fork the repository and submit pull requests for any enhancements or bug fixes. Feedback and suggestions are also welcome.

## License
This script is released under the MIT License. You're free to use, modify, distribute, and sublicense it. However, please ensure you understand and comply with the terms of the license before using or distributing this software.



