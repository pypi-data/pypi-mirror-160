# Sentry-DingDing-vibranium

Fork `https://github.com/jacksnowfuck/sentry-dingding-maxbon`

## fork原因
因为sentry用的是dockerhub上面的9.1.2版本，直接使用sentry-dingding-maxbon这个包会有报错
```
celery.task 会报: post_process() takes at least 4 arguments (3 given)
```


## 添加功能
告警内容添加tag环境信息

兼容系统自带告警策略配置

## 安装
因为我是docker镜像部署的，所以直接在dockerfile里面加上RUN pip install sentry-dingding-vibranium。就可以了，不用找requirement.txt.

## 告警效果

![image](https://user-images.githubusercontent.com/3078554/140253051-920f6518-8c47-44c1-9aed-84d5a533ddee.png)
