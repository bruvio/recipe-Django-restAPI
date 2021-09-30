#!/usr/bin/env bash

export REGION="us-east-1"


myKey='NVirginia'
REPO_NAME="xxxxxx"


echo ""
echo "creating vpc stack"
echo ""
aws cloudformation create-stack --capabilities CAPABILITY_IAM --stack-name ecs-core-infrastructure --template-body file://./templates/core-infrastructure-setup.yml

aws cloudformation wait stack-create-complete --stack-name ecs-core-infrastructure

export CORE_STACK_NAME="ecs-core-infrastructure"
export vpc=$(aws cloudformation describe-stacks --stack-name $CORE_STACK_NAME --query 'Stacks[0].Outputs[?OutputKey==`VpcId`].OutputValue' --output text)
export subnet_1=$(aws cloudformation describe-stacks --stack-name $CORE_STACK_NAME --query 'Stacks[0].Outputs[?OutputKey==`PublicSubnetOne`].OutputValue' --output text)
export subnet_2=$(aws cloudformation describe-stacks --stack-name $CORE_STACK_NAME --query 'Stacks[0].Outputs[?OutputKey==`PublicSubnetTwo`].OutputValue' --output text)


echo "vpc: $vpc"
echo "subnet1: $subnet_1"
echo "subnet2: $subnet_2"



REPO_URI=$(aws ecr describe-repositories --repository-names "${REPO_NAME}" --query "repositories[0].repositoryUri" --output text 2>/dev/null || \
           aws ecr create-repository --repository-name "${REPO_NAME}"  --query "repository.repositoryUri" --output text)


echo ""
echo "repository uri" $REPO_URI


STACK_NAME="BiotechDashboard"

aws cloudformation deploy \
    --stack-name $STACK_NAME \
    --template-file ./templates/ecs-webapp-stack.yml \
    --capabilities CAPABILITY_IAM \
    --parameter-overrides KeyName=$myKey \
    VpcId=$vpc \
    SubnetId=$subnet_1,$subnet_2 \
    ContainerPort=8000 \
    DesiredCapacity=2 \
    EcsImageUri=$REPO_URI \
    EcsImageVersion='latest' \
    InstanceType=t2.micro \
    MaxSize=3



ALB_DNS=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query 'Stacks[0].Outputs[?OutputKey==`ecsalb`].OutputValue' --output text)


echo ""
echo $ALB_DNS
