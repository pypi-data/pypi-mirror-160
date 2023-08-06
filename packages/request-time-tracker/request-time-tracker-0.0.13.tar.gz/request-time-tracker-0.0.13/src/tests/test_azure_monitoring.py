import json
from datetime import datetime, timedelta
from functools import partial
from unittest.mock import patch

from django.test import TestCase

from freezegun import freeze_time

from request_time_tracker.notifiers.azure_monitoring import AzureMonitoringNotifier
from request_time_tracker.trackers.memory import InMemoryQueueTimeTracker
from tests.base import DummyWSGI, FakeThread, get_time_in_millis, noop


class FakeAuthResponse:
    status_code = 200

    @staticmethod
    def json():
        return json.loads('''
            {
                "access_token":"test_token","client_id":"test_client","expires_in":"86400","expires_on":"1658374517",
                "ext_expires_in":"86399","not_before":"1658287817","resource":"https://monitor.azure.com/",
                "token_type":"Bearer"
            }
        ''')


class TestAzureMonitoring(TestCase):
    def setUp(self):
        super().setUp()
        self.notifier = AzureMonitoringNotifier(
            namespace='namespace',
            region='region',
            subscription_id='subscription_id',
            resource_group_name='resource_group_name',
            provider_name='provider_name',
            resource_type='resource_type',
            resource_id='resource_id'
        )
        self.tracker = partial(InMemoryQueueTimeTracker, queue_time_header_name='time-header', notifier=self.notifier)
        self.wsgi = self.tracker(DummyWSGI())

    @patch('request_time_tracker.notifiers.cloudwatch.threading.Thread', side_effect=FakeThread)
    @patch('request_time_tracker.notifiers.azure_monitoring.requests.post')
    @patch('request_time_tracker.notifiers.azure_monitoring.requests.get', return_value=FakeAuthResponse)
    def test_functionality(self, _auth_mock, push_metrics_mock, _threading_mock):
        utcnow = datetime.utcnow()

        with freeze_time(utcnow + timedelta(minutes=1)):
            self.wsgi({'time-header': get_time_in_millis()}, noop)
            push_metrics_mock.assert_called()
            push_metrics_mock.reset_mock()

        with freeze_time(utcnow + timedelta(minutes=2)):
            self.wsgi({'time-header': get_time_in_millis()}, noop)
            push_metrics_mock.assert_called()

    @patch('request_time_tracker.notifiers.cloudwatch.threading.Thread', side_effect=FakeThread)
    @patch('request_time_tracker.notifiers.azure_monitoring.requests.post')
    @patch('request_time_tracker.notifiers.azure_monitoring.requests.get', return_value=FakeAuthResponse)
    def test_urls(self, auth_mock, push_metrics_mock, _threading_mock):
        self.wsgi({'time-header': get_time_in_millis()}, noop)
        self.assertIn('https://region.monitoring.azure.com', push_metrics_mock.call_args[0][0])
        self.assertEqual(push_metrics_mock.call_args[1]['headers']['Authorization'], 'Bearer test_token')
        self.assertIn('http://169.254.169.254/metadata/identity/oauth2/token', auth_mock.call_args[0][0])

    @patch('request_time_tracker.notifiers.cloudwatch.threading.Thread', side_effect=FakeThread)
    @patch('request_time_tracker.notifiers.azure_monitoring.requests.post')
    @patch('request_time_tracker.notifiers.azure_monitoring.requests.get', return_value=FakeAuthResponse)
    def test_auth_token_expiration(self, auth_mock, _push_metrics_mock, _threading_mock):
        utcnow = datetime.utcnow()

        self.wsgi({'time-header': get_time_in_millis()}, noop)
        auth_mock.assert_called()
        auth_mock.reset_mock()

        with freeze_time(utcnow + timedelta(seconds=80000)):
            self.wsgi({'time-header': get_time_in_millis()}, noop)
            auth_mock.assert_not_called()

        # auth token expired
        with freeze_time(utcnow + timedelta(seconds=90000)):
            self.wsgi({'time-header': get_time_in_millis()}, noop)
            auth_mock.assert_called()
