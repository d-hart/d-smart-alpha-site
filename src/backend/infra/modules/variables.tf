#Variables start----------------------------------------------------------#
variable "function_name" {}
variable "assume_role" {}
variable "code_source" {}
variable "handler" {}
variable "layers" {
    default = null
}
variable "environment_var" {}
#Variables end----------------------------------------------------------#