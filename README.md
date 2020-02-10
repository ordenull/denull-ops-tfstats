# Terraform Stats
Gather resource counts from Terraform state files.

## Usage
    usage: tfstats [-h] [--verbose] [--include [field=value [field=value ...]]]
                 [--exclude [field=value [field=value ...]]] [--recursive]
                 [--path PATH]

    optional arguments:
    -h, --help            show this help message and exit
    --verbose             Be verbose and print debugging info
    --include [field=value [field=value ...]]
                          Only include resources matching filter
    --exclude [field=value [field=value ...]]
                          Exclude items with fieldname=fieldvalue
    --recursive           Travese the path recursively
    --path PATH           Terraform state directory with .tfstate files

## Examples
If your Terraform state is stored remotely, you will need to download it to the local filesystem. This can be
accomplished using the `terraform state pull > state.tfstate` command.

### Count all resources except data queries and null_resources_
    tfstats --exclude 'mode=data' 'type=null_resource' --recursive --path .

    +----------------------------------+-------+
    | Type                             | Count |
    +----------------------------------+-------+
    | aws_acm_certificate              | 1     |
    | aws_acm_certificate_validation   | 1     |
    | aws_alb                          | 6     |
    | aws_alb_listener                 | 12    |
    | aws_alb_listener_rule            | 56    |
    | aws_alb_target_group             | 16    |
    | aws_autoscaling_attachment       | 16    |
    | aws_autoscaling_group            | 7     |
    | aws_autoscaling_policy           | 16    |
    | aws_cloudwatch_event_rule        | 8     |
    | aws_cloudwatch_event_target      | 8     |
    | aws_cloudwatch_metric_alarm      | 40    |
    | aws_db_instance                  | 1     |
    | aws_db_subnet_group              | 1     |
    | aws_default_security_group       | 1     |
    | aws_ebs_volume                   | 2     |
    | aws_egress_only_internet_gateway | 1     |
    | aws_eip                          | 3     |
    | aws_eks_cluster                  | 1     |
    | aws_iam_instance_profile         | 13    |
    | aws_iam_role                     | 19    |
    | aws_iam_role_policy              | 22    |
    | aws_iam_role_policy_attachment   | 39    |
    | aws_instance                     | 6     |
    | aws_internet_gateway             | 1     |
    | aws_lambda_function              | 8     |
    | aws_lambda_permission            | 8     |
    | aws_launch_template              | 7     |
    | aws_lb_listener_certificate      | 4     |
    | aws_lb_listener_rule             | 6     |
    | aws_nat_gateway                  | 3     |
    | aws_network_acl                  | 1     |
    | aws_network_acl_rule             | 16    |
    | aws_route                        | 23    |
    | aws_route53_health_check         | 8     |
    | aws_route53_record               | 33    |
    | aws_route53_zone                 | 3     |
    | aws_route_table                  | 7     |
    | aws_route_table_association      | 9     |
    | aws_s3_bucket                    | 3     |
    | aws_s3_bucket_object             | 1     |
    | aws_secretsmanager_secret        | 11    |
    | aws_security_group               | 26    |
    | aws_security_group_rule          | 85    |
    | aws_sns_topic                    | 1     |
    | aws_sns_topic_policy             | 1     |
    | aws_sns_topic_subscription       | 1     |
    | aws_ssm_parameter                | 24    |
    | aws_subnet                       | 9     |
    | aws_volume_attachment            | 2     |
    | aws_vpc                          | 1     |
    | aws_vpc_dhcp_options             | 1     |
    | aws_vpc_dhcp_options_association | 1     |
    | aws_vpc_endpoint                 | 2     |
    | aws_vpc_peering_connection       | 1     |
    | datadog_synthetics_test          | 9     |
    | helm_release                     | 28    |
    | kubernetes_cluster_role          | 1     |
    | kubernetes_cluster_role_binding  | 3     |
    | kubernetes_config_map            | 1     |
    | kubernetes_namespace             | 3     |
    | kubernetes_service_account       | 2     |
    | random_string                    | 8     |
    | Total                            | 658   |
    +----------------------------------+-------+

### Only count AWS EC2 instances
    tfstats --include 'mode=resource' 'type=aws_instance' --recursive --path .

    +--------------+-------+
    | Type         | Count |
    +--------------+-------+
    | aws_instance | 63    |
    | Total        | 63    |
    +--------------+-------+
