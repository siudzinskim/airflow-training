### module 001: ###
resource "archive_file" "module-001" {
  output_path = "/tmp/dags/M001.zip"
  type        = "zip"
  source_dir  = "../modules/M001"
}

### module 002: ###
resource "archive_file" "module-002" {
  output_path = "/tmp/dags/M002.zip"
  type        = "zip"
  source_dir  = "../modules/M002"
}

