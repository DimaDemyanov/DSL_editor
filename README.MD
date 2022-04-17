**To start DSL editor server in docker container use the following commands:** 

```cd editor-master```

```docker build -t dsl-editor-server-image:<some-tag-id> .```

```docker run -d -p 127.0.0.1:8083:8083 --name dsl-editor-app dsl-editor-server-image:<some-tag-id>```

**To start DSL editor front in docker container use the following commands:** 

```cd front```

```docker build -t dsl-editor-front-image:<some-tag-id> .```

```docker run -d -p 127.0.0.1:3000:3000 --name dsl-editor-front-app dsl-editor-front-image:<some-tag-id>```

**Push images to Amazon ECR**  

First build image locally

Then run ```push-front-image.sh <some-tag-id> <image-kind>```, where ```some-tag-id``` is the tag of built image and ```image-kind``` is ```server``` or ```front```

**AWS info**

To set up DNS to EC2 instance please follow the instruction:
https://docs.amazonaws.cn/en_us/AWSEC2/latest/UserGuide/dynamic-dns.html

Current DNS is provided by:
https://www.noip.com/