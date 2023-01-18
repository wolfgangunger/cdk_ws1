## aws docu 
https://cdkworkshop.com/

## commands
mkdir cdk_ws1
cd cdk_ws1

cdk init sample-app --language python

## on windows :
.venv\Scripts\activate.bat

pip install -r requirements.txt

aws configure

cdk synth

cdk bootstrap

cdk ls

cdk deploy
#or
cdk deploy --all

# at the very end !
cdk destroy 
cdk destroy --all

## further infos on stacks and constructs
https://www.sccbrasil.com/blog/aws/cdk-stack-construct.html

## structuring the project
structure your project ( and the stacks) in layers
iam
vpc
kms/ssm
storage
databases
computing
monitoring
etc