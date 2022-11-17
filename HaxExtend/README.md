## HaxExtend
## 简介
Hax和woided的免费vps续费  
支持多种续费方式
### github action
使用github的服务器进行续费，方便  
已知问题：
+ github服务器大多ip已经被验证码和网站屏蔽，所以大概率不会成功

### github action with 自建服务器
把你自己的服务器添加到github action中，运行，ip大概率不会被ban  
[参考教程](https://docs.github.com/cn/actions/hosting-your-own-runners/about-self-hosted-runners)

### 自己服务器 + crontab
将docker镜像pull下来，把命令添加到crontab里面  
`docker run -e USERNAME=xxx -e PASSWORD=xxx -e TWOCAPTCHA_TOKEN=xxx  -e HOST=hax.co.id  -it --rm  ghcr.io/lyj0309/hax_extend:latest`

### 云函数
敬请期待

## 特性
使用docker将python，浏览器打包，直接运行即可  
可以自己选择添加`TWOCAPTCHA_TOKEN`，在音频验证码不可用时选择这个验证(收费，一次6分钱)
![image.png](https://wx1.sinaimg.cn/large/008rgIcAly1h1wi8lbsasj30f80b7ac6.jpg)

#### 参考

- https://www.python.org/
- https://www.selenium.dev/
- https://www.youtube.com/watch?v=As-_hfZUyIs
- https://github.com/SongLiKod/HaxExtend
- https://github.com/actions/virtual-environments/blob/main/images/macos/macos-12-Readme.md
- https://github.com/win2happy/win2Lee