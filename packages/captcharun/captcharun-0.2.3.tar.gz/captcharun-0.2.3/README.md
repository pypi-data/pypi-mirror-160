<div align="center">

<h1>CaptchaRun Python SDK</h1>

<p>
<a href="https://github.com/get-post-technology/captcha-run-python-sdk/actions?query=workflow%3ACI">
<img src="https://github.com/get-post-technology/captcha-run-python-sdk/workflows/CI/badge.svg" alt="Github Action Test" />
</a>

<a href="https://app.codecov.io/gh/get-post-technology/captcha-run-python-sdk">
<img alt="Codecov" src="https://codecov.io/gh/get-post-technology/captcha-run-python-sdk/branch/main/graph/badge.svg?token=NUIJJ4BK8H">
</a>
</p>

<a href="https://pypi.org/project/captcharun/">
<img src="https://img.shields.io/pypi/v/captcharun" alt="PyPI" />
</a>

</p>

<a href="https://captcha.run">CapthcaRun</a> 官方 Python 客户端

</div>

---

# 例子

## 查询余额
```python
from captcharun import Client, GetBalance, CreateTask
client = Client("你的 TOKEN")
result = client.invoke(GetBalance())

print(result)
# {'cumulativeRecharge': '1100', 'share': '0.0960', 'balance': '103.508', 'credit': '0', 'cumulativeShare': '0.0960'}

```

## 创建任务 & 获取状态
```python
from captcharun import Client, GetBalance, GetTask, CreateTask
from captcharun.task import ReCaptchaV2Task

client = Client("你的 TOKEN")

# 创建任务
result = client.invoke(
    CreateTask(
        ReCaptchaV2Task(
            "SITE KEY",
            "SITE REFERER",
        ),
        developer="开发者 ID"
    ),
)
print(result) 
# {'taskId': '492ca979-7559-4012-ac31-3134b9ce63f8'}

# 获取任务状态 (异步返回)
result = client.invoke(GetTask(result['taskId']))
print(result)

```
