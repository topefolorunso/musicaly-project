variable "project" {
  description = "Your GCP Project ID"
  default     = "streamifyproject"
  type        = string
}

variable "region" {
  description = "Your project region"
  default     = "us-central1"
  type        = string
}

variable "zone" {
  description = "Your project zone"
  default     = "us-central1-a"
  type        = string
}

variable "storage_class" {
  description = "Storage class type for your bucket"
  default     = "STANDARD"
  type        = string
}

variable "vm_image" {
  description = "Image for you VM"
  default     = "ubuntu-os-cloud/ubuntu-2004-lts"
  type        = string
}

variable "network" {
  description = "Network for your instance/cluster"
  default     = "default"
  type        = string
}

variable "stg_bq_dataset" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default     = "musicaly_stg"
  type        = string
}

variable "prod_bq_dataset" {
  description = "Storage class type for your bucket. Check official docs for more info."
  default     = "musicaly_prod"
  type        = string
}

variable "bucket" {
  description = "The name of your bucket. This should be unique across GCP"
  default     = "musicaly-data-lake"
  type        = string
}