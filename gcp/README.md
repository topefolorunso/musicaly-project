# GCP Setup

1. Create a [Google Cloud account](https://console.cloud.google.com) with your existing gmail account (follow the steps to create one if you don't already have)
2. Create a Google Cloud project and note the **Project ID**
3. Set up project [authentication and service account](https://cloud.google.com/docs/authentication/getting-started) for access with client libraries
   * Enable the following APIs
     * [IAM API](https://console.cloud.google.com/apis/library/iam.googleapis.com)
     * [IAM Service Account Credentials API](https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com)
   * Create [service account](https://cloud.google.com/iam/docs/creating-managing-service-accounts) and [Service account key](https://cloud.google.com/iam/docs/creating-managing-service-account-keys#creating) with the following specs. Learn more about service acounts [here](https://cloud.google.com/iam/docs/service-accounts)

     * Grant the following roles.
       * Storage Admin
       * Storage Object Admin
       * BigQuery Admin
     * Download service-account-keys (.json) and save in the gcp folder in the project directory. **(DO NOT share this key file publicly!)**
     * Rename the json key file to `google_credentials.json`
4. Set environment variable to point to your downloaded json key file. Replace `<path_to_your_google_credentials>` below with the path to file and run in terminal.

    ``` bash
    export GOOGLE_APPLICATION_CREDENTIALS="<path_to_your_google_credentials>"
    ```
    Note that this does not set the variable permanently. To permanently set it, append the command to the `.bashrc` or `.profile` file found in the home directory.
  