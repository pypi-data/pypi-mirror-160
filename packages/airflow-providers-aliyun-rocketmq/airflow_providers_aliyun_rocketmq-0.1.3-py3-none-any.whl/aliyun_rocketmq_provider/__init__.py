def get_provider_info():
    return {
        "package-name": "airflow-providers-aliyun-rocketmq",
        "name": "Aliyun RocketMQ Airflow Provider",
        "description": "Airflow provider for aliyun rocketmq",
        "hook-class-names": ["aliyun_rocketmq_provider.hooks.aliyun_rocketmq.AliyunRocketMQHook"],
        "versions": ["0.1.2"]
    }
