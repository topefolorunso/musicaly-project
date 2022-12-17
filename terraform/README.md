# infrastructure setup

## prerequisite
* a service account 
* credential key file saved in your local machine

After following the steps below, the following resources will be provisioned in GCP:
* Firewall Rule
* 2 Compute Instances
  - kafka-vm
  - airflow-vm
* Cloud Storage Bucket
* Dataproc Cluster
  - 1 master node
* BigQuery Dataset
  - Staging
  - Production

## how to setup

1. setup terraform
   - download [terraform](https://www.terraform.io/downloads)
   - add terraform to [path](https://gist.github.com/nex3/c395b2f8fd4b02068be37c961301caa7)

2. configure the terraform [`variables.tf`](variables.tf) file
   - specify your project ID in line 3
   - edit other variables as you see fit

3. run the following commands in your terminal
   - navigate to the terraform directory
      ```bash
      cd ~/musicaly-project/terraform
      ```
   - initiatalize terraform and download the required dependencies

      ```bash
      terraform init
      ```
   - preview the infrastructure to be provisioned
      ```bash
      terraform plan
      ```
   - apply the config and provision the infrastructure
      ```bash
      terraform apply
      ```
   - to tear down the resources after completing the project
      ```bash
      terraform destroy
      ```
