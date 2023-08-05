from typing import Dict

from mq_http_sdk.mq_client import MQClient, MQProducer
from mq_http_sdk.mq_producer import TopicMessage

from airflow.hooks.base import BaseHook


class AliyunRocketMQHook(BaseHook):
    """Interact with Aliyun RocketMQ."""

    conn_name_attr = 'aliyun_rocketmq_conn_id'
    default_conn_name = 'aliyun_rocketmq_default'
    conn_type = 'aliyun_rocketmq'
    hook_name = 'AliyunRocketMQ'

    @staticmethod
    def get_ui_field_behaviour() -> Dict:
        return {
            "hidden_fields": ['port', 'extra'],
            "relabeling": {
                'login': 'Access ID',
                'password': 'Access Key',
                'schema': 'Instance ID'
            },
            "placeholders": {
                'login': 'access id',
                'password': 'access key',
                'schema': 'instance_id'
            },
        }

    def __init__(
        self,
        topic: str,
        aliyun_rocketmq_conn_id: str = default_conn_name
    ) -> None:
        super().__init__()
        self.topic = topic
        self.aliyun_rocketmq_conn_id = aliyun_rocketmq_conn_id

    def get_conn(self) -> MQProducer:
        """Returns mq producer."""
        conn = self.get_connection(self.aliyun_rocketmq_conn_id)
        client = MQClient(conn.host, conn.login, conn.password)
        return client.get_producer(conn.schema, self.topic)

    def run(
        self,
        message_body: str,
        message_tag: str = None,
        message_key: str = None,
        trans_check_immunity_time: int = None,
        start_deliver_time: int = None,
        sharding_key: str = None,
        fail_silently: bool = False
    ) -> TopicMessage:
        """Publish the data."""
        message = TopicMessage(message_body)

        if message_tag is not None:
            message.set_message_tag(message_tag.lower())
        if message_key is not None:
            message.set_message_key(message_key)
        if trans_check_immunity_time is not None:
            message.set_trans_check_immunity_time(trans_check_immunity_time)
        if start_deliver_time is not None:
            message.set_start_deliver_time(start_deliver_time)
        if sharding_key is not None:
            message.set_sharding_key(sharding_key)

        try:
            return self.get_conn().publish_message(message)
        except Exception as e:
            if not fail_silently:
                raise

            self.log.warning("Publish msg to {} failed: {}", self.topic, repr(e))
