# ### module 001: ###
data "archive_file" "module-001" {
  output_path = "${local.repo_path}/dags/M001.zip"
  type        = "zip"
  source_dir  = "../modules/M001"
}

### module 003: ###
data "archive_file" "module-003" {
  output_path = "${local.repo_path}/dags/M003.zip"
  type        = "zip"
  source_dir  = "../modules/M003"
}

### module 004: ###
data "archive_file" "module-004" {
  output_path = "${local.repo_path}/dags/M004.zip"
  type        = "zip"
  source_dir  = "../modules/M004"
}

### module 006: ###
data "archive_file" "module-006" {
  output_path = "${local.repo_path}/dags/M006.zip"
  type        = "zip"
  source_dir  = "../modules/M006"
}

### module 007: ###
data "archive_file" "module-007" {
  output_path = "${local.repo_path}/dags/M007.zip"
  type        = "zip"
  source_dir  = "../modules/M007"
}

### module 008: ###
data "archive_file" "module-008" {
  output_path = "${local.repo_path}/dags/M008.zip"
  type        = "zip"
  source_dir  = "../modules/M008"
}

