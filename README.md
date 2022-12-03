
# Woiden And Hax Auto Extend <sup>💯</sup>  <img align="right" src="https://img.shields.io/badge/2022.12.03-activity-success"/>

**woiden.id 和 hax.co.id 自动续订**    

`activity` 徽章显示最后执行成功的日期，脚本是否稳定运行，`Github` 是 `UTC` 时区会有时差，一天误差属于正常

> **Note** `Github Action` 运行时所在的服务器IP可能被 `Google` ban 无法使用语音验证，因为公共的服务器被别人用过，IP被识别为机器人，可能上个人刚好也调用了 `Google reCaptcha` ，所以 `Google reCaptcha` 的语音验证调用能否成功随缘，使用 `2Captcha` 和 `YesCaptcha` 的图片验证不受此影响稳如老狗，甚至加载不出来图片也可以验证通过，建议语音图片两个同时使用即稳定也不费钱，或者[托管自己服务器](https://docs.github.com/cn/actions/hosting-your-own-runners/about-self-hosted-runners)，登陆时脚本是先执行语音验证，验证失败再执行图片验证，语音验证频繁调用会被ben ( 没几次就会被ben，不用担心应该就ben一两个小时左右 )，自己服务器使用语音验证最好时间间隔久点

## 参数 <a id='01' />

<kbd>**可选参数**</kbd> 选择平台默认 woiden.id
> `HOST: woiden.id 或 hax.co.id`</br>

<kbd>**必要参数**</kbd> 用户
> `USERNAME: Telegram ID`</br>
> `PASSWORD: 密码`

<kbd>**可选参数**</kbd> Telegram 推送参数 ( 都有服务器了会没有电报吗 )
> `TELE_ID: Telegram ID`</br>
> `TELE_TOKEN: 机器人Token`</br>

<kbd>**可选参数**</kbd> pushplus 推送参数 ( 微信推送 )
> `TENC_TOKEN: 你的Token`</br>

<kbd>**可选参数**</kbd> 图片和V3验证支持 `2Captcha`  ( 使用 `Yes Captcha` [参考⤵](#002) )
> `TWOCAPTCHA_TOKEN: 你的Token`</br>

<kbd>**可选参数**</kbd> 语音验证支持 `腾讯` `百度` `IBM` ~~`讯飞`~~，任选一个
> - 腾讯</br>
>     - `ASR_CHOICE: TENCENT`
>     - `SECRET_ID: 腾讯语音API的SECRET_ID`</br>
>     - `SECRET_KEY: 腾讯语音API的SECRET_KEY`</br>
> - 百度</br>
>     - `ASR_CHOICE: BAIDU`
>     - `APP_ID: 百度语音API的APP_ID`</br>
>     - `API_KEY: 百度语音API的API_KEY`</br>
>     - `SECRET_KEY: 百度语音API的SECRET_KEY`</br>
> - IBM</br>
>     - `ASR_CHOICE: IBM`
>     - `APP_ID: IBM API的IDkey`</br>
>     - `IBM_URL: IBM API的URL`</br>
> - ~~讯飞~~ ( 🚫不能使用 [详细⤵](#001) )</br>
>     - `ASR_CHOICE: XFYUN`
>     - `APP_ID: 讯飞语音API的APP_ID`</br>
>     - `API_KEY: 讯飞语音API的API_KEY`</br>
>     - `SECRET_KEY: 讯飞语音API的SECRET_KEY`</br>

**例如：** 
```shell
docker run \
-e HOST=woiden.id \ # 选择平台
-e USERNAME=123456 -e PASSWORD=123456 \ # 用户
-e TELE_ID=123456 -e TELE_TOKEN=123456\ # Telegram 推送
-e TWOCAPTCHA_TOKEN=123456 \ # 图片和V3验证
-e ASR_CHOICE=BAIDU -e APP_ID=123456 -e API_KEY=123456 -e SECRET_KEY=123456 \ # 语音验证
-it --rm  ghcr.io/zakkoree/woinden_extend:latest
```

>  **Warning** **至少有一项语音或者图片参数，建议语音图片两个同时使用**

## 使用

- **Github Action**
  - 1.初次使用需要修改 [renewTime](https://github.com/Zakkoree/woiden_extend/blob/main/renewTime#L1) 文件内日期，修改为你现在日期前六天内，之后会自动更新，不能是今日日期，不然今天不会执行脚本
  - 2.将 [参数⤴](#01) 添加到Secret [参考➡](https://docs.github.com/cn/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository)
  - 3.执行 `续订` 任务 [参考➡](https://docs.github.com/cn/actions/managing-workflow-runs/manually-running-a-workflow#running-a-workflow)，默认手动+cron， `0 0,8,16 * * *` 每天 `0/8/16` 点执行，你可以修改 [/.github/workflows/renew.yml](https://github.com/Zakkoree/woiden_extend/blob/main/.github/workflows/renew.yml#L6) 第 6 行来调整频率，每天只要成功续订一次后面任务就会跳过避免浪费解码平台额度
  - ⚠ 可能会有段时间无法使用(`UTC` 16点左右 | 北京时间0点左右)，原因是apt安装包时网络异常，影响不大仍可正常使用，使用docker镜像没影响只是少了更新 `README.md` 徽章时间的功能
- **Github Action With 自己服务器**</br>
  `托管自己服务器到 Github Action 中` [参考➡](https://docs.github.com/cn/actions/hosting-your-own-runners/about-self-hosted-runners)
- **自己服务器 + Crontab**</br>
  `把 Python Scrip 或 Docker 运行命令添加到 crontab 里面`
- **Python Script**
  ```shell
  pip3 install --no-cache-dir -r requirements.txt
  playwright install --with-deps
  HOST="woiden.id" USERNAME="xxx" PASSWORD="xxx" [可选参数...]
  python3 main.py
  ```
- **Docker**</br>
  ```shell
  docker run -e HOST=woiden.id -e USERNAME=xxx -e PASSWORD=xxx [可选参数...] \
  -it --rm  ghcr.io/zakkoree/woinden_extend:latest
  ```


<details>
 <summary><kbd>GitHub Actions 计划任务语法</kbd></summary>
    
---
    
计划任务语法有 5 个字段，中间用空格分隔，每个字段代表一个时间单位。</br>

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

## 结果

| ![成功](https://cdn.jsdelivr.net/gh/Zakkoree/FileDrive@main/images/picgo/2022/11/25/21-09-52-07e5c9-321ebc964e7c5daa5ca2057679a61d41-20221125210952.png "成功") | ![账户错误](https://cdn.jsdelivr.net/gh/Zakkoree/FileDrive@main/images/picgo/2022/11/25/23-48-16-f0cb04-2b6f4dfe72d24111df35310b81144e4b-20221125234815.png "账户错误") | ![终止](https://cdn.jsdelivr.net/gh/Zakkoree/FileDrive@main/images/picgo/2022/11/25/23-25-26-ec97d6-8efc47f259b881b1c49fb71e840a6207-20221125232525.png "终止") 
|  ----  | ----  | ----  |

## 集成<a id='1' />
<kbd>**语音识别**</kbd>
- [x] **`Tencent`** 每月 10 小时免费音频
- [x] **`BaiDu`** 新用户 30000 次一年期限免费音频
- [x] **`IBM`** 每月 500 分钟免费音频，但准确度不够，注册需外币卡</br>
    - 分享一个来自 [wx5ecc8c432b706](https://blog.51cto.com/u_14825502) 的密钥和URl</br>
    - `IDkey：nblnZuv5E5A_wo5j9eYC-nQVWHKyY5HxJXuEPnNpJgrr`</br>
    - `URL：https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/7e2f69e7-a5e8-4d56-91ae-f4dc7b4a1f0b`
- [x] ~~**`Xfyun`**~~ 每月 500 次免费音频流，注意是语音听写API，语音转写额度太少</br><a id='001' />
    - 🚫 `Github Action` 去除讯飞语音支持，偶尔能用简直莫名其妙，可能服务器环境不同导致，和 `Docker` 一样原因</br>
    - ❎ `Docker Build` 镜像不含讯飞，因为加讯飞构建会导致各种依赖冲突和系统依赖包</br>
    - ⚠ `Python Script` 我本地使用是可以的，运行需要安装 [xfyunAPI.py 的依赖项](https://github.com/Zakkoree/woiden_extend/blob/main/xfyunAPI.py#L4-L10) 和打开 `main.py` [22行](https://github.com/Zakkoree/woiden_extend/blob/main/main.py#L22) 和 [437~441行](https://github.com/Zakkoree/woiden_extend/blob/main/main.py#L437-L411) 的注释
- [ ] ~~`Aliyun`~~ 新用户三个月免费音频
- [ ] ~~`Azure`~~ 每月 5 小时免费音频，每小时音频 $1.543，注册需外币卡
- [ ] ~~`Google`~~ 国内要挂代理访问，需付费，注册需外币卡

<kbd>**图片识别**</kbd>  <kbd>**V3评分**</kbd>

> **Note** 目前是跳过v3验证，加上v3验证感觉没啥区别

- [x] **`2Captcha`** 1000次/1$，价格比下面便宜，并且识码还可以赚钱
- [x] ~~`Yes Captcha`~~ 66次/1¥，新用户可申请1500试用积分也就是100次 <a id='002' />
    - ⚠ 免费额度太少懒得配置环境参数了，API已经调试好了，如果想使用可以参考 [yescaptchaAPI.py L105-L121](https://github.com/Zakkoree/woiden_extend/blob/main/yescaptchaAPI.py#L105-L121) 和 [main.py L466-L473](https://github.com/Zakkoree/woiden_extend/blob/main/main.py#L466-L473)


## 分享
**woiden.id 和 hax.co.id 服务器使用小技巧**
 
hax 只有IPv6，并且 woiden 的 IPv4 也被墙了，网页的 ssh 太难用，我的宽带不支持 IPv6 ，都是开着 VPN 连上 woiden 再通过 woiden 跳到 hax ，使用起来非常不方便和不稳定</br>

于是想起 VPN 组网，然后就有了IP4地址，也不需要再挂VPN可以直连，使用的工具是 `zerotier` ，并不需要公网 IP，组成 p2p 的虚拟局域网

参照官网文档教程只配置 hax 就行了，woiden 有点麻烦没必要折腾，如果是 linux 大佬请随意

配合 `Squid` 工具使用，然后你就会发现原本需要挂 VPN 连接的 VPS 变成了一个免费的 VPN 了( 由于网络波动勉强4K 网速够用 可以开启BBR提速 )，嗯~  这反转 :)

---
