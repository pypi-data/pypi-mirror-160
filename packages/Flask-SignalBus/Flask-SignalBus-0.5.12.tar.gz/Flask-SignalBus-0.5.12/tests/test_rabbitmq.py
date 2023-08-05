import pytest
import time
from flask_signalbus import rabbitmq
from flask_signalbus.rabbitmq.publisher import DeliverySet


@pytest.fixture(params=['direct', 'init_app'])
def publisher(app, request):
    if request.param == 'direct':
        p = rabbitmq.Publisher(app)
    elif request.param == 'init_app':
        p = rabbitmq.Publisher()
        p.init_app(app)
    return p


def test_delivery_set():
    s = DeliverySet(20, 10)  # from 20 to 29
    assert(not s.all_confirmed)
    assert(s.confirm(23) is True)
    assert(s.confirm(23) is False)
    assert(not s.all_confirmed)
    assert(s.confirm(10) is False)
    assert(not s.all_confirmed)
    assert(s.confirm(28, multiple=True) is True)
    assert(s.confirm(24, multiple=False) is False)
    assert(not s.all_confirmed)
    assert(s.confirm(29) is True)
    assert(s.all_confirmed)


def test_publisher(publisher):
    message = rabbitmq.Message(
        body='test message',
        properties=rabbitmq.MessageProperties(),
        exchange='',
        routing_key='test',
    )
    publisher.publish_messages([])
    publisher.publish_messages([message])
    publisher.publish_messages([message, message])
    time.sleep(20)
    publisher.publish_messages([message], timeout=60)
