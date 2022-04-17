#/bin/bash

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 099405913193.dkr.ecr.us-east-1.amazonaws.com

echo 'Login successfully'

docker tag dsl-editor-${2}-image:${1} 099405913193.dkr.ecr.us-east-1.amazonaws.com/dsl-editor-image-repository:dsl-editor-${2}-image-${1}

echo 'Image tagged'

docker push 099405913193.dkr.ecr.us-east-1.amazonaws.com/dsl-editor-image-repository:dsl-editor-${2}-image-${1}

echo 'Image pushed'
