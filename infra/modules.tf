# ### module 001: ###
# resource "archive_file" "module-001" {
#   output_path = "/tmp/dags/M001.zip"
#   type        = "zip"
#   source_dir  = "../modules/M001"
# }
#
# ### module 002: ###
# resource "archive_file" "module-002" {
#   output_path = "/tmp/dags/M002.zip"
#   type        = "zip"
#   source_dir  = "../modules/M002"
# }
#
# ### module 003: ###
# resource "archive_file" "module-003" {
#   output_path = "/tmp/dags/M003.zip"
#   type        = "zip"
#   source_dir  = "../modules/M003"
# }
#
# ### module 004: ###
# resource "archive_file" "module-004" {
#   output_path = "/tmp/dags/M004.zip"
#   type        = "zip"
#   source_dir  = "../modules/M004"
# }
#
### module 005: ###
resource "archive_file" "module-005" {
  output_path = "/tmp/dags/M005.zip"
  type        = "zip"
  source_dir  = "../modules/M005"
}

### module 006: ###
resource "archive_file" "module-006" {
  output_path = "/tmp/dags/M006.zip"
  type        = "zip"
  source_dir  = "../modules/M006"
}

