
# ~~woiden_extend~~

## 删库跑路

## 简介

**Woiden和Hax自动续订**

github action默认每天执行3次任务，正确情况下只需一次就可以成功续订，成功率接近💯，每天成功续订后面任务就会暂停可以不产生多余的解码平台扣费

<kbd>注意:</kbd>

> Hax续订没有调试，需要修改下配置，两个没什么差别，只需要修改URL

> `google reCaptcha v2` 语音验证有可被ban，因为github的Actions虚机托管在Azure上，每次重新执行Actions的run workflow都会导致切换公网IP，有的IP被别人使用过（干啥就不知道了嘿嘿！），所以识别成了机器人，图片验证挺稳定，项目目前是先执行语音验证，语音验证失败再执行图片验证<br/>
> `google reCaptcha v3` 验证目前没弄明白这个网站入口在哪块，代码有v3方法，目前是跳过v3验证，成功率挺正常，正常情况代码自动重试5次内就可以成功，有懂的可用研究下google reCaptcha v3


## 参数
> `USERNAME: Woiden或Hax的用户名`</br>
> `PASSWORD: Woiden或Hax的密码`</br>
> `TWOCAPTCHA_TOKEN: 2Captcha的Token`</br>
> `APP_ID: 百度语音API的APP_ID`</br>
> `API_KEY: 百度语音API的API_KEY`</br>
> `SECRET_KEY: 百度语音API的SECRET_KEY`</br>
> `TELE_ID: telegram用户ID`</br>
> `TELE_TOKEN: telegrambot_token机器人Token`

## 支持方式
python script和docker运行需要稍微修改 (不能提醒最后续签日期 目前集成在github action)

- github action

> 将参数添加到Secret，执行 `/.github/workflows/renew.yml` </br>
> 默认手动+cron， `0 0,8,16 * * *` 每天早上 `0/8/16` 点执行，时区为UTC时间 </br>
> 可以调整为 `0 0,8,16 */3 * *` 每三天早上 `0/8/16` 点执行，降低解码平台费用 </br>

> 或者托管自己的服务器，ip大概率不会被ban  [参考教程](https://docs.github.com/cn/actions/hosting-your-own-runners/about-self-hosted-runners)
- python script

> `python3 main.py`
- docker

> `docker run -e USERNAME=xxx -e PASSWORD=xxx -e TWOCAPTCHA_TOKEN=xxx -e APP_ID=xxx -e API_KEY=xxx -e SECRET_KEY=xxx -e TELE_ID=xxx -e TELE_TOKEN=xxx -it --rm  [镜像]`
- 自己服务器 + crontab

> 将代码拉下来，构建docker镜像或者直接使用python脚本，把命令添加到crontab里面 </br>
> `python3 main.py` or `docker run -e USERNAME=xxx -e PASSWORD=xxx -e TWOCAPTCHA_TOKEN=xxx -e APP_ID=xxx -e API_KEY=xxx -e SECRET_KEY=xxx -e TELE_ID=xxx -e TELE_TOKEN=xxx -it --rm  [镜像]`

## 集成列表
- [x] `baidu语音识别 API` 用于音频验证 (新用户免费一年30000次)
- [ ] `讯飞语音识别 API` 用于音频验证 (每个月免费使用500次)
- [x] `2Captcha API` 用于图片验证 (收费，一次6分钱)
- [ ] `yescaptcha API` 用于图片验证 (新用户免费1500次 价格便宜)


<h1></h1>
HaxExtend文件是参考 https://github.com/lyj0309/HaxExtend 项目基础修改的，已经弃用
