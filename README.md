# walnut

> a simply ops small tools

  * openvpn 连接时长及在线状态
  * ladp密码修改

## Build Setup

``` bash
  # build web
  cd walnut-vue
  npm install
  npm run build
  # build docker-image
  vim Dockerfile
  # pls input the env 
  cd ../
  docker build -t walnut .
  docker run -p 8080:8080 -v openvpn-log:/tmp/openvpn-status.log -v /data/db:/walnut/db walnut /run.sh
```