terraform {
  backend "s3" {
    bucket  = "fraud-detector-3000-terraform-backend"
    region  = "us-east-2"
    key     = "state.tfstate"
    encrypt = true
  }
}
