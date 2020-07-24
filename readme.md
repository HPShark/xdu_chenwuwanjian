# 晨午晚检自动填报工具

#### 本代码缝合了https://github.com/abadfox233/ncov 和 https://github.com/ZimoLoveShuang/auto-submit 两位大佬的作品，仅供学习交流使用，请在下载2小时内删除

#### 本项目仅供学习交流使用，如作他用所承受的任何直接、间接法律责任一概与作者无关

#### 如果此项目侵犯了您或者您公司的权益，请立即联系我删除



# 注意

本脚本只内置了南校区的经纬度,**只适用于南校区在校的同学**



# 项目说明

- `data` 需要提交给网站的信息
- `AccountInfo.ini` 登录的配置文件，用来保存帐号密码以及收发邮箱信息和邮箱key（只支持QQ邮箱）
- `index.py` 完成自动提交的py脚本
- `utils` 帮助生成默认项配置的py脚本
- `requirements.txt` py依赖库以及版本说明文件
- `层文件.zip` 打包好的云函数依赖库文件



# 使用方式

### 配合腾讯云函数使用（免费）

1. clone 或者 下载 此仓库到本地

   ```
   git clone https://github.com/HPShark/xdu_chenwuwanjian.git
   ```

2. 打开本地仓库文件夹，配置`AccountInfo.ini`中对应的信息，**注意这里的学号和密码都是教务系统的学号和密码，key是邮箱的密码**

3. 打开百度搜索[腾讯云函数](https://console.cloud.tencent.com/scf/index?rid=1)，注册认证后，进入控制台，点击左边的层，然后点新建，名称随意，然后点击上传zip，选择项目中的`层文件.zip`上传，然后选择运行环境`python3.6`，然后点击确定，耐心等待一下，上传依赖包需要花费的时间比较长 [![新建腾讯云函数依赖](https://github.com/ZimoLoveShuang/auto-submit/raw/master/screenshots/ed6044e6.png)](https://github.com/ZimoLoveShuang/auto-submit/blob/master/screenshots/ed6044e6.png)

4. 点左边的函数服务，新建云函数，名称随意，运行环境选择`python3.6`，创建方式选择空白函数，然后点击下一步 [![新建腾讯云函数](https://github.com/ZimoLoveShuang/auto-submit/raw/master/screenshots/a971478e.png)](https://github.com/ZimoLoveShuang/auto-submit/blob/master/screenshots/a971478e.png)

5. 提交方法选择上传本地压缩包，把本地的/data，/utils，AccountInfo.ini，index.py，requirements.txt五个文件和文件夹打包上传，在点击下面的高级设置，设置内存为256M，超时时间为`30秒`，添加层为刚刚新建的函数依赖层，环境变量设置一个`TZ=Asia/Shanghai`，然后点击完成

6. 进入新建好的云函数，左边点击触发管理，点击创建触发器，名称随意，触发周期选择自定义，然后配置cron表达式。下面的表达式表示每天中午十二点整执行，可配置多个时间以便早中晚自动运行

   ```
   0 0 12 * * * *
   ```

7. 然后就可以测试云函数了，绿色代表云函数执行成功，红色代表云函数执行失败（失败的原因大部分是由于依赖造成的）。返回结果是`auto submit fail.`代表自动提交失败；返回结果是`auto submit success.`，代表自动提交成功，如遇到问题，请仔细查看日志

8. enjoy it!

9. 也可配合Windows计划任务或者使用linux定时任务，将脚本挂在自己的云服务器上，不会就搜索一下，过程不再赘述

#### 

