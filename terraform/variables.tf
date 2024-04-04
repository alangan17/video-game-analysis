variable "credentials" {
  description = "Path to the credentials file"
  default     = "../keys/gcp-creds.json"
}

variable "project" {
  description = "Project Name"
  default     = "video-game-analysis"
}

variable "region" {
  description = "Region Name"
  default     = "us-west1"
}

variable "location" {
  description = "Project Location"
  default     = "US"
}

variable "bq_dataset_name" {
  description = "My BigQuery Dataset Name"
  default     = "vga"
}

variable "gcs_bucket_name" {
  description = "Google Cloud Bucket Name"
  default     = "vga-bucket-latest"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDARD"
}
