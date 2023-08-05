<p align="center">
  <a href="https://www.airflow.apache.org">
    <img alt="Airflow" src="https://cwiki.apache.org/confluence/download/attachments/145723561/airflow_transparent.png?api=v2" width="60" />
  </a>
</p>
<h1 align="center">
  Airflow Provider for Aliyun RocketMQ
</h1>
  <h3 align="center">
</h3>

![GitHub](https://img.shields.io/github/license/Ed-XCF/airflow-providers-aliyun-rocketmq)
[![Build Status](https://app.travis-ci.com/Ed-XCF/airflow-provider-aliyun-rocketmq.svg?branch=main)](https://app.travis-ci.com/Ed-XCF/airflow-provider-aliyun-rocketmq)
[![codecov](https://codecov.io/gh/Ed-XCF/airflow-provider-aliyun-rocketmq/branch/main/graph/badge.svg?token=RCI7A0MBOO)](https://codecov.io/gh/Ed-XCF/airflow-provider-aliyun-rocketmq)
![PyPI](https://img.shields.io/pypi/v/airflow-providers-aliyun-rocketmq)

Example
```python
from aliyun_rocketmq_provider.hooks.aliyun_rocketmq import AliyunRocketMQHook

message_push_topic = AliyunRocketMQHook(topic="message-push")
message_push_topic.run("helloWorld", fail_silently=True)
```
