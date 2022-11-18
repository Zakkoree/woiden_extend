
# ~~Woiden And Hax Auto Extend~~ (删库跑路) <img align="right" src="https://img.shields.io/badge/2022.11.18-activity-success" />

**Woiden和Hax自动续订** 

`woiden.id` 和 `hax.co.id` 自动续订正常情况下只需一次就可以成功续订，成功率基本💯</br>
`Github Action` 默认每天执行3次任务，每天只要成功续订一次后面任务就会跳过，不增加多余解码平台费用</br>
`activity` 徽章显示最后成功执行的日期，项目是否稳定运行，由于 `Github` 是 `UTC` 时区会有时差,一天误差属于正常现象

> **Warning** 
> 1. `Github Action` 上的 `Google reCaptcha` 验证基本触发不了， `Github Action` 服务器99%的IP都被 `Google` ban了，因为服务器被人滥用过IP被识别为机器人，所以只能使用 `2Captcha` 或 `YesCaptcha` 的API破解验证码，或者[托管自己服务器](https://docs.github.com/cn/actions/hosting-your-own-runners/about-self-hosted-runners)</br>
> 3. `Google reCaptcha v2` 登陆验证是先执行语音验证，语音验证失败再执行图片验证，语音验证频繁调用会被ben(没几次就会被ben，不用担心应该就ben一两个小时左右)<br/>
> 4. `Google reCaptcha v3` 续订时候评分验证，代码有写v3验证方法，加与不加感觉没有区别，我还没弄明白我这个方法到底有没有用还是我没找到入口，现在是忽略v3验证，成功率基本100%就没管v3了，有懂的朋友可以研究下
> 5. 只配置了 `woiden.id` 续订，`hax.co.id` 的续订没有配置，两个没什么差别

## 参数
> `USERNAME: Woiden或Hax的用户名`</br>
> `PASSWORD: Woiden或Hax的密码`</br>
> `TWOCAPTCHA_TOKEN: 2Captcha的Token`</br>
> `APP_ID: 百度语音API的APP_ID`</br>
> `API_KEY: 百度语音API的API_KEY`</br>
> `SECRET_KEY: 百度语音API的SECRET_KEY`</br>
> `TELE_ID: telegram用户ID`</br>
> `TELE_TOKEN: telegrambot_token机器人Token`

## 使用
初次使用需要修改 [renewTime](https://github.com/Zakkoree/woiden_extend/blob/main/renewTime) 文件内日期，修改为你现在日期前六天内都行，不能是今日，不然今天就不会执行了，之后就不用管了</br>
python script和docker运行需要稍微修改 (执行失败不能提醒最后续签日期)

- Github Action

> 将参数添加到Secret，执行 [/.github/workflows/renew.yml](https://github.com/Zakkoree/woiden_extend/blob/main/.github/workflows/renew.yml)</br>
> 默认手动+cron， `0 0,8,16 * * *` 每天早上 `0/8/16` 点执行，你可以通过修改 [/.github/workflows/renew.yml](https://github.com/Zakkoree/woiden_extend/blob/main/.github/workflows/renew.yml#L6) 文件的第 6 行来调整频率</br>
> 可调整为 `0 0,8,16 */3 * *` 每三天早上 `0/8/16` 点执行，降低解码平台费用</br>

<details>
 <summary>计划任务语法</summary>
计划任务语法有 5 个字段，中间用空格分隔，每个字段代表一个时间单位。</br>
<kbd>时区为UTC</kbd></br>

```plain
┌───────────── 分钟 (0 - 59)
│ ┌───────────── 小时 (0 - 23)
│ │ ┌───────────── 日 (1 - 31)
│ │ │ ┌───────────── 月 (1 - 12 或 JAN-DEC)
│ │ │ │ ┌───────────── 星期 (0 - 6 或 SUN-SAT)
│ │ │ │ │
│ │ │ │ │
│ │ │ │ │
* * * * *
```

每个时间字段的含义：

|符号   | 描述        | 举例                                        |
| ----- | -----------| -------------------------------------------|
| `*`   | 任意值      | `* * * * *` 每天每小时每分钟                  |
| `,`   | 值分隔符    | `1,3,4,7 * * * *` 每小时的 1 3 4 7 分钟       |
| `-`   | 范围       | `1-6 * * * *` 每小时的 1-6 分钟               |
| `/`   | 每         | `*/15 * * * *` 每隔 15 分钟                  |

**注**：由于 GitHub Actions 的限制，如果设置为 `* * * * *` 实际的执行频率为每 5 分执行一次。
</details>

- Python Script

> `python3 main.py`
- Docker

> `docker run -e USERNAME=xxx -e PASSWORD=xxx -e TWOCAPTCHA_TOKEN=xxx -e APP_ID=xxx -e API_KEY=xxx -e SECRET_KEY=xxx -e TELE_ID=xxx -e TELE_TOKEN=xxx -it --rm  [镜像]`
- 自己服务器 + Crontab

> 将代码拉下来，构建docker镜像或者直接使用python脚本，把命令添加到crontab里面 </br>
> `configuration env ... and run python3 main.py` or `docker build ... and docker run -e USERNAME=xxx -e PASSWORD=xxx -e TWOCAPTCHA_TOKEN=xxx -e APP_ID=xxx -e API_KEY=xxx -e SECRET_KEY=xxx -e TELE_ID=xxx -e TELE_TOKEN=xxx -it --rm  [镜像]`

> **Warning** <kbd>**注意**</kbd> 别使用我的镜像,有可能是旧的或测试用的





## 集成
- [x] `百度语音识别 API` 用于音频验证 (新用户免费一年30000次)
- [ ] `讯飞语音识别 API` 用于音频验证 (每个月免费使用500次)
- [x] `2Captcha API`    用于图片验证 (1000次/1$，价格略微比下面便宜，并且识码还可以赚钱)
- [ ] ~~`YesCaptcha API` 用于图片验证 (新用户免费1500次 100次/1¥)~~

#

HaxExtend文件是参考 https://github.com/lyj0309/HaxExtend 项目，在其基础上修改的，已经弃用
