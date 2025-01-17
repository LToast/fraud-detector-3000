resource "aws_ecs_cluster" "this" {
  name = local.ecs_cluster_name
}

resource "aws_iam_role" "ecs_task_execution_role" {
  name = "${terraform.workspace}_${var.api_name}_ecs_task_execution_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  managed_policy_arns = [
    "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
  ]
}

resource "aws_iam_role" "ecs_task_role" {
  name = "${terraform.workspace}_${var.api_name}_ecs_task_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_security_group" "ecs_service" {
  name        = "${terraform.workspace}_${var.api_name}_ecs_sg"
  description = "Security group for ECS service"
  vpc_id      = module.vpc.vpc_id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = var.additional_tags
}

resource "aws_ecs_task_definition" "this" {
  family                   = "${terraform.workspace}_${var.api_name}_task_def"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.fargate_cpu
  memory                   = var.fargate_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
  task_role_arn            = aws_iam_role.ecs_task_role.arn

  container_definitions = jsonencode([
    {
      name   = "${terraform.workspace}_${var.api_name}_container"
      image  = aws_ecr_repository.this.repository_url
      memory = var.fargate_memory_reserved
      portMappings = [
        {
          containerPort = 80
          hostPort      = 80
          protocol      = "tcp"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-region        = var.aws_region
          awslogs-group         = aws_cloudwatch_log_group.this.name
          awslogs-stream-prefix = "${terraform.workspace}_${var.api_name}"
        }
      }
  }])
}

resource "aws_ecs_service" "this" {
  name            = "${terraform.workspace}_${var.api_name}_service"
  cluster         = aws_ecs_cluster.this.id
  task_definition = aws_ecs_task_definition.this.arn
  desired_count   = 1

  launch_type = "FARGATE"

  network_configuration {
    subnets         = module.vpc.public_subnets_ids
    security_groups = [aws_security_group.ecs_service.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.this.arn
    container_name   = "${terraform.workspace}_${var.api_name}_container"
    container_port   = 80
  }

  deployment_maximum_percent = 200

  depends_on = [aws_lb_listener.this]

  tags = var.additional_tags
}
