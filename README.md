
# ~~woiden_extend~~

## ==删库跑路==

## 简介

**woided和Hax自动续订**

Hax需要修改下参数

+ 添加`BAIDU语音识别API`，用于音频验证(新用户免费一年30000次)
+ 添加`TWOCAPTCHA_TOKEN`，在音频验证码不可用时选择这个验证(收费，一次6分钱)


## 支持方式
python script和docker运行需要稍微修改(不能提醒最后续签日期 目前集成在github action)

- github action

`run action`

或者托管自己的服务器，ip大概率不会被ban  [参考教程](https://docs.github.com/cn/actions/hosting-your-own-runners/about-self-hosted-runners)
- python script

`python3 main.py`
- docker

`docker run -e USERNAME=xxx -e PASSWORD=xxx -e TWOCAPTCHA_TOKEN=xxx  -e HOST=hax.co.id  -it --rm  [镜像]` 
- 自己服务器 + crontab

将代码拉下来，构建docker镜像或者直接使用python脚本，把命令添加到crontab里面

- `python3 main.py`
- `docker run -e USERNAME=xxx -e PASSWORD=xxx -e TWOCAPTCHA_TOKEN=xxx  -e HOST=hax.co.id  -it --rm  [镜像]`

## 特性





<h1></h1>

HaxExtend文件是参考 https://github.com/lyj0309/HaxExtend 项目基础修改的，已经弃用
