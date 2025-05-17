#!/bin/bash

#  הגדרות בסיס 
KEY_NAME="pokemon-key"
KEY_FILE="$KEY_NAME.pem"
SECURITY_GROUP="pokemon-sg"
INSTANCE_NAME="pokemon-instance"
REGION="us-west-2"
AMI_ID="ami-0892d3c7ee96c0bf7"  # Ubuntu 22.04 for us-west-2
INSTANCE_TYPE="t2.micro"
GITHUB_REPO="https://github.com/sabrins7/Pokemon-drawer-Project.git"

# יצירת מפתח אם לא קיים 
if [ ! -f "$KEY_FILE" ]; then
    echo "Creating key pair..."
    aws ec2 create-key-pair --region $REGION --key-name "$KEY_NAME" \
        --query "KeyMaterial" --output text > "$KEY_FILE"
    chmod 400 "$KEY_FILE"
fi

#  יצירת קבוצת אבטחה אם לא קיימת 
SG_ID=$(aws ec2 describe-security-groups --region $REGION \
    --filters Name=group-name,Values=$SECURITY_GROUP \
    --query "SecurityGroups[*].GroupId" --output text)

if [ -z "$SG_ID" ]; then
    echo "Creating security group..."
    SG_ID=$(aws ec2 create-security-group --region $REGION \
        --group-name "$SECURITY_GROUP" --description "Allow SSH" \
        --query 'GroupId' --output text)

    aws ec2 authorize-security-group-ingress --region $REGION \
        --group-id "$SG_ID" --protocol tcp --port 22 --cidr 0.0.0.0/0
fi

# יצירת מכונת EC2 
echo "Launching EC2 instance..."
INSTANCE_ID=$(aws ec2 run-instances --region $REGION \
    --image-id $AMI_ID --count 1 --instance-type $INSTANCE_TYPE \
    --key-name "$KEY_NAME" --security-group-ids "$SG_ID" \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$INSTANCE_NAME}]" \
    --query "Instances[0].InstanceId" --output text)

echo "Waiting for instance..."
aws ec2 wait instance-running --region $REGION --instance-ids "$INSTANCE_ID"

PUBLIC_IP=$(aws ec2 describe-instances --region $REGION \
    --instance-ids "$INSTANCE_ID" \
    --query "Reservations[0].Instances[0].PublicIpAddress" --output text)

echo "Instance launched at IP: $PUBLIC_IP"

# חיבור לשרת והתקנה 
echo "Setting up server..."
ssh -o "StrictHostKeyChecking=no" -i "$KEY_FILE" ubuntu@$PUBLIC_IP << EOF
  sudo apt update
  sudo apt install -y python3 python3-pip git

  # הורדת הקוד מגיטהאב
  git clone $GITHUB_REPO
  cd Pokemon-drawer-Project

  pip3 install -r requirements.txt

  # הרצת המשחק בעת התחברות
  echo "python3 /home/ubuntu/Pokemon-drawer-Project/main.py" >> /home/ubuntu/.bashrc
EOF

echo " Deployment complete. Connect with:"
echo "ssh -i \"$KEY_FILE\" ubuntu@$PUBLIC_IP"
