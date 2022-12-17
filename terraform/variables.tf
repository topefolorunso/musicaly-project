variable "project" {
  description = "Your GCP Project ID"
  default     = "musicaly-project"
  type        = string
}

variable "region" {
  description = "Your project region"
  default     = "us-east1"
  type        = string
}

variable "zone" {
  description = "Your project zone"
  default     = "us-east1-b"
  type        = string
}

variable "network" {
  description = "Network for your instance/cluster"
  default     = "default"
  type        = string
}
variable "vm_image" {
  description = "Image for you VM"
  default     = "ubuntu-os-cloud/ubuntu-2004-lts"
  type        = string
}

variable "storage_class" {
  description = "Storage class type for your bucket"
  default     = "STANDARD"
  type        = string
}

variable "staging_bigquery_dataset" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default     = "musicaly_staging"
  type        = string
}

variable "production_bigquery_dataset" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default     = "musicaly_production"
  type        = string
}

variable "bucket" {
  description = "The name of your bucket. This should be unique across GCP"
  default     = "musicaly_data_lake"
  type        = string
}