# Serverless Application with AWS and Pulumi

### Overview

This project is about an application that runs by itself on AWS, without needing servers, thanks to a tool called Pulumi. It automatically takes care of files you upload to a cloud storage in AWS called AWS S3. Right after a file is uploaded, an AWS Lambda function (a small piece of code that runs on demand) kicks in to record details about the file in an AWS database named DynamoDB.

Key features of this project are :

- **Automatic Processing** : **The project uses AWS Lambda to run code automatically whenever a file is uploaded to S3, so we don't need to manage any servers**. This means you don't have to worry about the underlying infrastructure or its maintenance. The code runs only when needed, ensuring efficient resource use and reducing costs. By automating the response to file uploads, the system can scale automatically to handle any volume of data seamlessly.

- **Data Persistence** : **We are storing the file metadata in a DynamoDB table, demonstarting how to interact with NoSQL databases in a serverless context. DynamoDB offers fast, flexible storage that scales automatically**. This setup allows for quick retrieval and analysis of file information in the DynamoDB table, supporting real-time processing needs and enabling a wide range of applications, from analytics to data archiving, without the overhead of managing a traditional database.

- **Infrastructure as Code(IaC)** : **The project uses Pulumi to define,deploy and manage AWS resources in a repeatable and predictable manner**. Infrastructure as Code enables you to automate the setup of your AWS environment, making it easy to reproduce and scale. With Pulumi, you can version control your infrastructure just like application code, simplifying updates and collaboration. This approach reduces the potential for human error, speeds up deployment processes, and ensures consistency across development, testing, and production environments.

This guide gives you everything you need to start using this application, including what you'll need to have ready, how to set it up, how it's built, and how to use it.

### Prerequisites

- AWS account
- Pulumi Account and CLI
- Python installed
- AWS CLI configured with user credentials

### Project Structure

- **`/lambda_function`** : Contains the AWS Lamda function code. Inside, you'll find a Python script **(`process_s3_uploads.py`)** responsible for processing the S3 bucket upload events. This script interacts with DynamoDB to log file metadata.
- **`/serverless_infrastructure/pulumi_project`**: Contains Pulumi IaC(Infra) scripts for deploying AWS resources. This directory includes:
  - **`main.py`** : The main script defining the AWS resources like S3 buckets, Lambda functions, and DynamoDB tables needed for the application.
  - **`Pulumi.yaml`**: The configuration file for the Pulumi project, specifying project details and Pulumi settings.
  - **`requirements.txt`** : Lists the dependencies required by Pulumi to deploy the infrastructure, ensuring anyone who runs the project will have the right tools and versions.
  - **`compute.py`** : Sets up an IAM role with policies for S3 and DynamoDB access, preparing the security and access controls for the Lambda function.
  - **`serverless_component.py`**: Constructs the core infrastructure of the serverless application by creating an S3 bucket for file uploads and a DynamoDB table for data storage, neatly packaged as a reusable Pulumi component. It also exports key identifiers for these resources.

### Setup and Deployment

1. **Configure AWS CLI** : Ensure the [AWS CLI](https://aws.amazon.com/cli/) is installed and configured with your credentials:

   ```
   aws configure
   ```

2. **Install Pulumi** : Follow the [Pulumi installation guide](https://www.pulumi.com/docs/install/)
3. **Setup an AWS project with Pulumi**: Read and familiarize yourself with the [Pulumi guide for AWS here](https://www.pulumi.com/docs/install/).
4. **Deploy your Pulumi Project**: Navigate to the **`/serverless_infrastructure/pulumi_project`** directory and run:

```
   pulumi up
```

This command creates or updates your AWS resources based on your Pulumi scripts. Follow the prompts to complete the deployment. 5. **Deploy the Lambda function** : Ensure your AWS Lambda function code is ready in **`/lambda_function`**. Deploy it as part of the Pulumi script or manually through the AWS console.

### Architecture

This serverless application is designed for simplicity and scalability using the powerful features of AWS services and Pulumi for seamless orchestration. Here is a breakdown of it's architecture :

#### AWS Lamda Function Trigger :

The application kicks into action with file uploads to an AWS S3 bucket. Each upload generates an event that triggers an AWS Lambda function. This function is specifically designed to react to new uploads by executing a pre-defined set of operations without the need for a continuously running server.

#### Role of DynamoDB

The AWS Lambda function's primary role is to log each file upload event into an AWS DynamoDB table, **`my-serverless-infra-index-table-a24e71b`**, by creating a new record. For each uploaded file, the function records the file's unique identifier **(`s3_object_key`)** and the exact time of upload **(`timestamp`)**. This process transforms the AWS S3 bucket into an event-driven source that feeds data processing workflows, with DynamoDB acting as the persistent storage for these events.

### Usage

This application automates the processing of files uploaded to an AWS S3 bucket, logs upload events via an AWS Lambda function, and stores file information in a DynamoDB table. Here's how to use the application:

#### Uploading Files to the AWS S3 Bucket

##### 1. Via AWS Management Console:

- Navigate to the S3 section in the AWS Management Console.
- Find and open the bucket designated for file uploads (e.g., your-bucket-name).
- Click the "Upload" button, select your file(s), and confirm the upload.

##### 2. Using AWS CLI:

- Ensure you have the AWS CLI installed and configured.
- Use the following command to upload a file:
  ```
  aws s3 cp your-file.txt s3://your-bucket-name/
  ```
- Replace `your-file.txt` with the path to your file and `your-bucket-name` with the name of your AWS S3 bucket.

#### Viewing Logs or Outputs from the AWS Lambda Function

##### Accessing Execution Logs:

- Go to the AWS Management Console and open the CloudWatch service.
- Navigate to "Logs" in the sidebar and find the log group associated with your AWS Lambda function (typically named **`/aws/lambda/your-lambda-function-name`**).
- Click on the log group to view the streams, which contain detailed logs of each function invocation, including any custom **`print`** statements or errors.

#### Querying the DynamoDB Table for Processed File Metadata

##### 1.Via AWS Management Console:

- Open the DynamoDB section in the AWS Management Console.
- Locate and select your table (e.g., **`my-serverless-infra-index-table-a24e71b`**).
- Use the "Items" tab to browse the entries. You can also use the built-in search features to query specific items based on file metadata.

##### 2. Using AWS CLI:

- To retrieve an item from your DynamoDB table, use the following command:
  ```
  aws dynamodb get-item --table-name my-serverless-infra-index-table-a24e71b --key '{"id": {"S": "your-file-key"}}'
  ```
- Replace **`my-serverless-infra-index-table-a24e71b`** with your table name and **"your-file-key"** with the actual key of the file you're interested in.

By following these steps, you can effectively upload files to the designated AWS S3 bucket, monitor the processing through the AWS Lambda function logs, and view the resulting metadata records stored in DynamoDB.

### References

- [Pulumi Documentation](https://www.pulumi.com/docs/) - For guidance on defining cloud infrastructure with Pulumi.
- [AWS Documentation](https://docs.aws.amazon.com/) - For insights into using AWS services and navigating the AWS console.
- [Chat GPT](https://chat.openai.com/) - For general guidance, answering questions related to project development, and troubleshooting assistance.
