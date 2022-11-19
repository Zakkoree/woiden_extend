
# ~~Woiden And Hax Auto Extend~~ (删库跑路) <img align="right" src="https://img.shields.io/badge/2022.11.19-activity-success" />

**woiden.id 和 hax.co.id 自动续订** 

`woiden.id` 和 `hax.co.id` 自动续订正常情况下只需一次就可以成功续订，成功率基本💯</br>
`Github Action` 默认每天执行3次任务，每天只要成功续订一次后面任务就会跳过，不增加解码平台多余费用</br>
`activity` 徽章显示最后成功执行的日期，脚本是否稳定运行，由于 Github 是 UTC 时区会有时差，一天误差属于正常

> **Warning** 
> 1. `Github Action` 上的有些IP都被 `Google` ban了，因为有的服务器被人用过了IP被识别为机器人，可能上个人也调用了 `Google reCaptcha` ，所以语音验证调用成功随缘，使用 `2Captcha` 和 `YesCaptcha` 图片验证不受影响稳如老狗，建议语音图片两个同时使用即稳定也不费钱，或者[托管自己服务器](https://docs.github.com/cn/actions/hosting-your-own-runners/about-self-hosted-runners)</br>
> 3. `Google reCaptcha v2` 登陆时脚本是先执行语音验证，验证失败再执行图片验证，语音验证频繁调用会被ben(没几次就会被ben，不用担心应该就ben一两个小时左右)，使用语音验证最好时间间隔久点<br/>
> 4. `Google reCaptcha v3` 续订时评分验证，代码有写v3验证方法，加与不加感觉没有区别，还没弄明白我这个方法到底有没有用呢还是我没找到入口呢，现在是忽略v3验证，成功率基本100%就没管v3了，有懂的朋友可以研究下
> 5. 只配置了 `woiden.id` 续订，`hax.co.id` 的续订没有配置，两个没什么差别

## 参数
<kbd>**必须参数**</kbd>
> `USERNAME: Woiden或Hax的用户名`</br>
> `PASSWORD: Woiden或Hax的密码`</br>

<kbd>**可选参数**</kbd> Telegram 推送参数
> `TELE_ID: telegram用户ID`</br>
> `TELE_TOKEN: telegrambot_token机器人Token`</br>

<kbd>**可选参数**</kbd> 图片验证和V3验证
> `TWOCAPTCHA_TOKEN: 2Captcha的Token`</br>

<kbd>**可选参数**</kbd> 语音验证API，支持 `百度` `讯飞` `IBM` ，三选一
> `ASR_CHOICE: BAIDU 、 XF 或 IBM`
> - 百度 API需要的参数</br>
>> `APP_ID: 百度语音API的APP_ID`</br>
>> `API_KEY: 百度语音API的API_KEY`</br>
>> `SECRET_KEY: 百度语音API的SECRET_KEY`</br>
> - 讯飞 API需要的参数 ( Docker不能使用讯飞 [详细➡](#001) )</br>
>> `APP_ID: 讯飞语音API的APP_ID`</br>
>> `API_KEY: 讯飞语音API的API_KEY`</br>
>> `SECRET_KEY: 讯飞语音API的SECRET_KEY`</br>
> - IBM API需要的参数</br>
>> `APP_ID: IBM API的IDkey`</br>
>> `IBM_URL: IBM API的URL`</br>

## 使用
初次使用需要修改 [renewTime](https://github.com/Zakkoree/woiden_extend/blob/main/renewTime#L1) 文件内日期，修改为你现在日期前六天内都行，不能是今日，不然今天就不会执行了，之后就不用管了</br>

- Github Action
> 将参数添加到Secret，执行续订任务</br>
> 默认手动+cron， `0 0,8,16 * * *` 每天 `0/8/16` 点执行，你可以通过修改 [/.github/workflows/renew.yml](https://github.com/Zakkoree/woiden_extend/blob/main/.github/workflows/renew.yml#L6) 文件的第 6 行来调整频率</br>
> 可调整为 `0 0,8,16 */3 * *` 每三天 `0/8/16` 点执行，降低解码平台费用
<details>
 <summary><kbd>计划任务语法</kbd></summary>
 
#
 
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
#
</details>

- Python Script
```
 configuration env ...
 pip install --no-cache-dir -r requirements.txt
 python3 main.py
```
- Docker
```
 docker run -e USERNAME=xxx -e PASSWORD=xxx [可选参数] -it --rm  zakkoree/woiden_extend
```
- 自己服务器 + Crontab
```
 将代码拉下来，构建docker镜像或者直接使用python脚本，把命令添加到crontab里面
```

## 集成
<kbd>**语音识别**</kbd>
- [x] `BaiDu API` 新用户免费一年30000次
- [x] `xfyun API` 每个月 500 次免费音频流</br><a id='001' />
 ✅ `Github Action` 正常使用</br>
 ❎ `Docker Build` 镜像不含讯飞语音识别，因为加讯飞构建会出现各种依赖冲突和需要的系统软件包，未解决</br>
 ⚠ `Python Script` 需要安装 [xfyunAPI.py 的依赖项](https://github.com/Zakkoree/woiden_extend/blob/main/xfyunAPI.py#L4-L10)，和打开 `main.py` [22行](https://github.com/Zakkoree/woiden_extend/blob/main/main.py#L22) 和 [382~386行](https://github.com/Zakkoree/woiden_extend/blob/main/main.py#L382-L386) 的注释
- [x] `IBM API` 每月 500 分钟免费音频，但准确度不够，注册需外币卡</br>
分享一个来自 [wx5ecc8c432b706](https://blog.51cto.com/u_14825502) 的密钥和URl，不要滥用毕竟就这么 500 分钟，或许已经没时间了🤷‍♂️</br>
`IDkey：nblnZuv5E5A_wo5j9eYC-nQVWHKyY5HxJXuEPnNpJgrr`</br>
`URL：https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/7e2f69e7-a5e8-4d56-91ae-f4dc7b4a1f0b`
- [ ] ~~`Azure API`~~ 每月 5 小时免费音频，每小时音频 $1.543，注册需外币卡
- [ ] ~~`Google API`~~ 要挂代理访问，需付费，注册需外币卡

<kbd>**图片识别**</kbd>
- [x] `2Captcha API` 1000次/1$，价格略微比下面便宜，并且识码还可以赚钱
- [ ] ~~`Yes Captcha API`~~ 100次/1¥，新用户免费1500次

#

HaxExtend文件是参考 https://github.com/lyj0309/HaxExtend 项目，在其基础上修改的，已经弃用
