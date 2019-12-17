# generate-tf-docs
Generation Terraform documentation based on variable.tf & outputs.tf files of the module. 


## Usage
----------------------

NOTE: Of course, you must install Python3 + pip and the next module:
```bash
$ pip3 install pyhcl
```

To get a help, run:
```bash
$ python3 generate_docs_pyhcl.py -h
usage: python3 script_name.py {ARGS}

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --md folder, --mdir folder
                        Set the directory where module exists
  --ed folder, --edir folder
                        Set the directory where example exists

created by Vitalii Natarov

```

So, to generate docs, run:
```bash
$ python3 generate_docs_pyhcl.py --mdir="/Users/captain/Projects/Terraform/aws/modules/nlb" --edir="/Users/captain/Projects/Terraform/aws/examples/nlb"
Looks like that the [OUTPUT_nlb.md] file has been created: /Users/captain/Projects/Python/Terraform
--- 0.04 seconds ---
 ============================================================
 ==========================FINISHED==========================
 ============================================================
```

Where:
- python3 - Python
- generate_docs_pyhcl.py - The script's name.
- --mdir="/Users/captain/Projects/Terraform/aws/modules/nlb" - It's path to some module (For example: nlb).
- --edir="/Users/captain/Projects/Terraform/aws/examples/nlb" - It's path to where your project is (For example I used that path).

The `/Users/captain/Projects/Terraform/aws/modules/nlb` directory have to looks like the following one:
```bash
$ tree /Users/captain/Projects/Terraform/aws/modules/nlb

/Users/captain/Projects/Terraform/aws/modules/nlb
|-- nlb.tf
|-- outputs.tf
`-- variables.tf

0 directories, 3 files
```

The `/Users/captain/Projects/Terraform/aws/examples/nlb` folder have to looks like the following one:
```bash
$ tree /Users/captain/Projects/Terraform/aws/examples/nlb

/Users/captain/Projects/Terraform/aws/examples/nlb
|-- README.md
|-- main.tf
`-- terraform.tfstate

0 directories, 3 files

```

## Output file will be something like this one...
----------------------

`````bash
# Work with AWS NLB via terraform

A terraform module for making NLB.


## Usage
----------------------
Import the module and retrieve with ```terraform get``` or ```terraform get --update```. Adding a module resource to your template, e.g. `main.tf`:

```
#
# MAINTAINER Vitaliy Natarov "vitaliy.natarov@yahoo.com"
#
terraform {
  required_version = "> 0.9.0"
}
provider "aws" {
    region                  = "us-east-1"
    shared_credentials_file = "${pathexpand("~/.aws/credentials")}"    
    profile                 = "default"
}
module "iam" {
    source                          = "../../modules/iam"
    name                            = "My-Security"
    region                          = "us-east-1"
    environment                     = "PROD"

    aws_iam_role-principals         = [
        "ec2.amazonaws.com",
    ]
    aws_iam_policy-actions           = [
        "cloudwatch:GetMetricStatistics",
        "logs:DescribeLogStreams",
        "logs:GetLogEvents",
        "elasticache:Describe*",
        "rds:Describe*",
        "rds:ListTagsForResource",
        "ec2:DescribeAccountAttributes",
        "ec2:DescribeAvailabilityZones",
        "ec2:DescribeSecurityGroups",
        "ec2:DescribeVpcs",
        "ec2:Owner",
    ]
}
module "vpc" {
    source                              = "../../modules/vpc"
    name                                = "My"
    environment                         = "PROD"
    # VPC
    instance_tenancy                    = "default"
    enable_dns_support                  = "true"
    enable_dns_hostnames                = "true"
    assign_generated_ipv6_cidr_block    = "false"
    enable_classiclink                  = "false"
    vpc_cidr                            = "172.31.0.0/16"
    private_subnet_cidrs                = ["172.31.32.0/20"]
    public_subnet_cidrs                 = ["172.31.0.0/20"]
    availability_zones                  = ["us-east-1b"]
    enable_all_egress_ports             = "true"
    allowed_ports                       = ["8080", "3306", "443", "80"]

    map_public_ip_on_launch             = "true"

    #Internet-GateWay
    enable_internet_gateway             = "true"
    #NAT
    enable_nat_gateway                  = "false"
    single_nat_gateway                  = "true"
    #VPN
    enable_vpn_gateway                  = "false"
    #DHCP
    enable_dhcp_options                 = "false"
    # EIP
    enable_eip                          = "false"
}
module "ec2" {
    source                              = "../../modules/ec2"
    name                                = "TEST-Machine"
    region                              = "us-east-1"
    environment                         = "PROD"
    number_of_instances                 = 2
    ec2_instance_type                   = "t2.micro"
    enable_associate_public_ip_address  = "true"
    disk_size                           = "8"
    tenancy                             = "${module.vpc.instance_tenancy}"
    iam_instance_profile                = "${module.iam.instance_profile_id}"
    subnet_id                           = "${element(module.vpc.vpc-publicsubnet-ids, 0)}"
    #subnet_id                           = "${element(module.vpc.vpc-privatesubnet-ids, 0)}"
    #subnet_id                           = ["${element(module.vpc.vpc-privatesubnet-ids)}"]
    vpc_security_group_ids              = ["${module.vpc.security_group_id}"]

    monitoring                          = "true"
}
module "nlb" {
    source                  = "../../modules/nlb"
    name                    = "Load-Balancer"
    region                  = "us-east-1"
    environment             = "PROD"
    
    subnets                     = ["${module.vpc.vpc-privatesubnet-ids}"]
    vpc_id                      = "${module.vpc.vpc_id}"   
    enable_deletion_protection  = false

    backend_protocol    = "TCP"
    alb_protocols       = "TCP"
    
    #It's not working properly when use EC2... First of all, comment the line under this text. Run playbook. Uncomment that line.    
    target_ids          = ["${module.ec2.instance_ids}"]
}
```

## Module Input Variables
----------------------
- `health_check_unhealthy_threshold` - Number of consecutive positive health checks before a backend instance is considered unhealthy. (`default = 3`)
- `health_check_healthy_threshold` - Number of consecutive positive health checks before a backend instance is considered healthy. (`default = 3`)
- `timeouts_update` - Used for LB modifications. Default = 10mins (`default = 10m`)
- `createdby` - Created by (`default = Vitaliy Natarov`)
- `backend_protocol` - The protocol the backend service speaks. Options: HTTP, HTTPS, TCP, SSL (secure tcp). (`default = HTTP`)
- `backend_port` - The port the service on the EC2 instances listen on. (`default = 80`)
- `idle_timeout` - The time in seconds that the connection is allowed to be idle. Default: 60. (`default = 60`)
- `enable_deletion_protection` - If true, deletion of the load balancer will be disabled via the AWS API. This will prevent Terraform from deleting the load balancer. Defaults to false. (`default = False`)
- `region` - The region where to deploy this code (e.g. us-east-1). (`default = us-east-1`)
- `health_check_port` - The port used by the health check if different from the traffic-port. (`default = traffic-port`)
- `target_ids` - The ID of the target. This is the Instance ID for an instance, or the container ID for an ECS container. If the target type is ip, specify an IP address. (`default = []`)
- `health_check_interval` - Interval in seconds on which the health check against backend hosts is tried. (`default = 10`)
- `ip_address_type` - The type of IP addresses used by the subnets for your load balancer. The possible values are ipv4 and dualstack (`default = ipv4`)
- `certificate_arn` - The ARN of the SSL Certificate. e.g. 'arn:aws:iam::XXXXXXXXXXX:server-certificate/ProdServerCert' (`default = `)
- `timeouts_create` - Used for Creating LB. Default = 10mins (`default = 10m`)
- `target_type` - The type of target that you must specify when registering targets with this target group. The possible values are instance (targets are specified by instance ID) or ip (targets are specified by IP address). The default is instance. Note that you can't specify targets for a target group using both instance IDs and IP addresses. If the target type is ip, specify IP addresses from the subnets of the virtual private cloud (VPC) for the target group, the RFC 1918 range (10.0.0.0/8, 172.16.0.0/12, and 192.168.0.0/16), and the RFC 6598 range (100.64.0.0/10). You can't specify publicly routable IP addresses (`default = instance`)
- `load_balancer_type` - The type of load balancer to create. Possible values are application or network. The default value is application. (`default = network`)
- `alb_protocols` - A protocol the ALB accepts. (e.g.: TCP) (`default = TCP`)
- `name_prefix` - Creates a unique name beginning with the specified prefix. Conflicts with name (`default = nlb`)
- `lb_internal` - If true, NLB will be an internal NLB (`default = False`)
- `orchestration` - Type of orchestration (`default = Terraform`)
- `environment` - Environment for service (`default = STAGE`)
- `subnets` - A list of subnet IDs to attach to the NLB (`default = []`)
- `deregistration_delay` - The amount time for Elastic Load Balancing to wait before changing the state of a deregistering target from draining to unused. The range is 0-3600 seconds. The default value is 300 seconds. (`default = 300`)
- `vpc_id` - Set VPC ID for ?LB (`default = `)
- `timeouts_delete` - Used for LB destroying LB. Default = 10mins (`default = 10m`)
- `name` - Name to be used on all resources as prefix (`default = TEST-NLB`)

            
## Module Output Variables
----------------------
- `lb_arn` - ARN of the lb itself. Useful for debug output, for example when attaching a WAF.
- `lb_dns_name` - The DNS name of the lb presumably to be used with a friendlier CNAME.
- `lb_listener_frontend_tcp_443_id` - The ID of the lb Listener we created.
- `lb_id` - The ID of the lb we created.
- `lb_arn_suffix` - ARN suffix of our lb - can be used with CloudWatch
- `lb_name` - ""
- `lb_listener_frontend_tcp_443_arn` - The ARN of the HTTP lb Listener we created.
- `lb_zone_id` - The zone_id of the lb to assist with creating DNS records.
- `lb_listener_frontend_tcp_80_id` - The ID of the lb Listener we created.
- `lb_listener_frontend_tcp_80_arn` - The ARN of the HTTPS lb Listener we created.
- `target_group_arn` - ARN of the target group. Useful for passing to your Auto Scaling group module.

    
## Authors
=======

Created and maintained by [Vitaliy Natarov](https://github.com/SebastianUA)
(vitaliy.natarov@yahoo.com).

License
=======

Apache 2 Licensed. See [LICENSE](https://github.com/SebastianUA/terraform/blob/master/LICENSE) for full details.

`````

## Authors
=======

Created and maintained by [Vitaliy Natarov](https://github.com/SebastianUA)(vitaliy.natarov@yahoo.com).

License
=======

Apache 2 Licensed. See [LICENSE](https://github.com/SebastianUA/generate-tf-docs/blob/master/LICENSE) for full details.
