
# Woiden And Hax Auto Extend  <sub><img align="right" src="https://img.shields.io/badge/2022.11.21-activity-success" /></sub>

**woiden.id 和 hax.co.id 自动续订**    成功率基本💯

`activity` 徽章显示最后成功执行的日期，脚本是否稳定运行，`Github` 是 `UTC` 时区会有时差，一天误差属于正常

> **Note** `Github Action` 运行时所在的服务器IP可能被 `Google` ban 无法使用语音验证，因为公共的服务器被别人用过，IP被识别为机器人，可能上个人刚好也调用了 `Google reCaptcha` ，所以 `Google reCaptcha` 的语音验证调用能否成功随缘，使用 `2Captcha` 和 `YesCaptcha` 的图片验证不受此影响稳如老狗，甚至加载不出来图片也可以验证通过，建议语音图片两个同时使用即稳定也不费钱，或者[托管自己服务器](https://docs.github.com/cn/actions/hosting-your-own-runners/about-self-hosted-runners)，登陆时脚本是先执行语音验证，验证失败再执行图片验证，语音验证频繁调用会被ben ( 没几次就会被ben，不用担心应该就ben一两个小时左右 )，自己服务器使用语音验证最好时间间隔久点

## 使用

- **Github Action**
  - 1.初次使用需要修改 [renewTime](https://github.com/Zakkoree/woiden_extend/blob/main/renewTime#L1) 文件内日期，修改为你现在日期前六天内，不能是今日日期，不然今天不会执行脚本，之后会自动更新
  - 2.将你自己的 [参数⤵](#01) 添加到Secret
  - 3.执行 `续订` 任务，默认手动+cron， `0 0,8,16 * * *` 每天 `0/8/16` 点执行，你可以修改 [/.github/workflows/renew.yml](https://github.com/Zakkoree/woiden_extend/blob/main/.github/workflows/renew.yml#L6) 第 6 行来调整频率，
    `0 0,8,16 */3 * *` 每三天 `0/8/16` 点执行，每天只要成功续订一次后面任务就会跳过避免浪费解码平台额度
- **Github Action With 自己服务器**
  - 把你自己的服务器托管到 `Github Action` 中 [参考➡](https://docs.github.com/cn/actions/hosting-your-own-runners/about-self-hosted-runners)
- **Python Script**
  - `configuration env ...`
  - `pip3 install --no-cache-dir -r requirements.txt`
  - `python3 main.py`
- **Docker**</br>
  - `docker run -e USERNAME=xxx -e PASSWORD=xxx [可选参数] -it --rm  ghcr.io/zakkoree/woinden_extend:latest`
- **自己服务器 + Crontab**
  - 把 `Python Scrip` 脚本或 `Docker Image` 运行命令添加到 `crontab` 里面

<details>
 <summary><kbd>GitHub Actions 计划任务语法</kbd></summary>
    
---
    
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

***

</details>

## 参数 <a id='01' />

<kbd>**可选参数**</kbd> 默认 woiden.id
> `HOST: woiden.id 或 hax.co.id`</br>

<kbd>**必要参数**</kbd> 用户信息
> `USERNAME: Telegram ID`</br>
> `PASSWORD: 密码`

<kbd>**可选参数**</kbd> Telegram 推送参数 ( 都有服务器了会没有电报吗 )
> `TELE_ID: Telegram ID`</br>
> `TELE_TOKEN: 机器人Token`</br>

<kbd>**可选参数**</kbd> 图片和V3验证支持 `2Captcha`
> `TWOCAPTCHA_TOKEN: 你的Token`</br>

<kbd>**可选参数**</kbd> 语音验证支持 `百度` `讯飞` `IBM` ，任选一个
> - 百度</br>
>     - `ASR_CHOICE: BAIDU`
>     - `APP_ID: 百度语音API的APP_ID`</br>
>     - `API_KEY: 百度语音API的API_KEY`</br>
>     - `SECRET_KEY: 百度语音API的SECRET_KEY`</br>
> - 讯飞 ( Docker不能使用讯飞 [详细⤵](#001) )</br>
>     - `ASR_CHOICE: XFYUN`
>     - `APP_ID: 讯飞语音API的APP_ID`</br>
>     - `API_KEY: 讯飞语音API的API_KEY`</br>
>     - `SECRET_KEY: 讯飞语音API的SECRET_KEY`</br>
> - IBM</br>
>     - `ASR_CHOICE: IBM`
>     - `APP_ID: IBM API的IDkey`</br>
>     - `IBM_URL: IBM API的URL`</br>

>  **Warning** **语音参数或图片参数至少有一项，建议语音图片两个同时使用**

## 集成
<kbd>**语音识别**</kbd>
- [x] **`BaiDu`** 新用户 30000 次一年期限免费音频
- [x] **`Xfyun`** 每月 500 次免费音频流</br><a id='001' />
    - ✅ `Github Action` 正常使用</br>
    - ❎ `Docker Build` 镜像不含讯飞，因为加讯飞构建会导致各种依赖冲突和系统依赖包</br>
    - ⚠ `Python Script` 直接运行需要安装 [xfyunAPI.py 的依赖项](https://github.com/Zakkoree/woiden_extend/blob/main/xfyunAPI.py#L4-L10) 和打开 `main.py` [22行](https://github.com/Zakkoree/woiden_extend/blob/main/main.py#L22) 和 [402~406行](https://github.com/Zakkoree/woiden_extend/blob/main/main.py#L402-L406) 的注释
- [x] **`IBM`** 每月 500 分钟免费音频，但准确度不够，注册需外币卡</br>
    - 分享一个来自 [wx5ecc8c432b706](https://blog.51cto.com/u_14825502) 的密钥和URl，不要滥用毕竟就这么 500 分钟，或许已经没时间了🤷‍♂️</br>
    - `IDkey：nblnZuv5E5A_wo5j9eYC-nQVWHKyY5HxJXuEPnNpJgrr`</br>
    - `URL：https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/7e2f69e7-a5e8-4d56-91ae-f4dc7b4a1f0b`
- [ ] ~~`Aliyun`~~ 新用户三个月免费音频
- [ ] ~~`Azure`~~ 每月 5 小时免费音频，每小时音频 $1.543，注册需外币卡
- [ ] ~~`Google`~~ 国内要挂代理访问，需付费，注册需外币卡

<kbd>**图片识别**</kbd>
- [x] **`2Captcha`** 1000次/1$，价格略微比下面便宜，并且识码还可以赚钱
- [ ] ~~`Yes Captcha`~~ 100次/1¥，新用户免费1500次

---


