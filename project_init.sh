#!/bin/bash

# Add project path as an environment variable
$path = "/nfs/home/user/project"

export PYTHONPATH = $path

# Add S3 bucket and keys
$aws_bucket_name = ""
$aws_access_key_id = ""
$aws_secret_access_key = ""

export AWS_BUCKET_NAME = $aws_bucket_name
export AWS_ACCESS_KEY_ID = $aws_access_key_id
export AWS_SECRET_ACCESS_KEY = $aws_secret_access_key

# Add RDS MySQL login info

$mysql_host = ""
$mysql_user = ""
$mysql_password = ""

export MYSQL_HOST = $mysql_host
export MYSQL_USER = $mysql_user
export MYSQL_PASSWORD = $mysql_password