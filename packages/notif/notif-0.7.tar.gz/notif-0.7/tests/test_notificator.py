# pylint: disable=attribute-defined-outside-init

import json
import unittest
from smtplib import SMTPRecipientsRefused
from typing import List
from unittest import TestCase
from unittest.mock import patch, call, MagicMock

import pymsteams
import requests

from notif.notificator import (
    SlackNotificator,
    EmailNotificator,
    ChannelNotificator,
    TeamsNotificator,
    DiscordNotificator,
    Notificator,
)
from tests.base import CaptureOutputTestCase


class PrintNotificator(Notificator):
    def _format_subject(self, subject_message: str) -> str:
        return f"*{subject_message}*\n"

    def send_notification(self, message, subject=None) -> None:
        subject = self._format_subject(subject) if subject is not None else ""
        print(f"{subject}{message}")


class PrintNotificatorTest(CaptureOutputTestCase):
    def setUp(self) -> None:
        self._capture_output()

    def test_send_notification(self):
        notificator = PrintNotificator(on_error_sleep_time=1)
        a_message = "a message is send"

        notificator.send_notification(a_message)

        expected_message = a_message
        actual = self.test_out.getvalue().strip()
        self.assertEqual(expected_message, actual)

    def test_send_notification_with_a_subject(self):
        notificator = PrintNotificator(on_error_sleep_time=1)
        a_message = "a message is send"
        a_subject = "Here is a subject"

        notificator.send_notification(a_message, a_subject)

        expected_message = f"*{a_subject}*\n{a_message}"
        actual = self.test_out.getvalue().strip()
        self.assertEqual(expected_message, actual)

    def test_send_notification_error(self):
        notificator = PrintNotificator(on_error_sleep_time=1)
        a_message_error = "a message error is send"
        a_error_type = ValueError
        an_error = a_error_type(a_message_error)

        notificator.send_notification_error(an_error)

        expected_message = f"An error of type {a_error_type} occurred. An the error message is {a_message_error}"
        actual = self.test_out.getvalue().strip()
        self.assertEqual(expected_message, actual)


class SlackNotificatorTest(TestCase):
    def setUp(self):
        self.a_fake_web_hook = "a_web_hook"
        self.a_notification = "A normal text."
        self.default_subject_message = "*Python script Slack notification*\n"
        self.headers = {"content-type": "application/json"}

    def _post_call(self, expected_payload_message) -> List:
        post_call = [
            call.post(
                url=self.a_fake_web_hook,
                data=json.dumps(expected_payload_message),
                headers=self.headers,
            )
        ]
        return post_call

    @patch("notif.notificator.requests")
    def test_givenASlackNotificator_whenSendNotification_thenSendMessageDefaultSubject(self, requests_mock):
        slack_notificator = SlackNotificator(self.a_fake_web_hook)
        slack_notificator.send_notification(self.a_notification)

        expected_payload_message = {"text": self.default_subject_message + self.a_notification}

        post_call = self._post_call(expected_payload_message)

        requests_mock.assert_has_calls(post_call)

    @patch("notif.notificator.requests")
    def test_givenASlackNotificator_whenSendNotificationWithSubject_thenSendMessageWithSubject(self, requests_mock):
        slack_notificator = SlackNotificator(self.a_fake_web_hook)

        a_user_formatted_subject = "Here a subject"
        slack_notificator.send_notification(self.a_notification, subject=a_user_formatted_subject)

        expected_payload_message = {"text": f"*{a_user_formatted_subject}*\n" + self.a_notification}

        post_call = self._post_call(expected_payload_message)

        requests_mock.assert_has_calls(post_call)

    @patch("notif.notificator.requests.post", side_effect=requests.exceptions.HTTPError)
    def test_givenASlackNotificator_whenSendNotificationDoesNotWork_thenWaitTimer(self, requests_mock):
        slack_notificator = SlackNotificator(self.a_fake_web_hook, on_error_sleep_time=1)

        with self.assertWarns(Warning):
            slack_notificator.send_notification(self.a_notification)

            expected_payload_message = {"text": self.default_subject_message + self.a_notification}
            post_call = [
                call.post(
                    url=self.a_fake_web_hook,
                    data=json.dumps(expected_payload_message),
                    headers=self.headers,
                ),
                call.post(
                    url=self.a_fake_web_hook,
                    data=json.dumps(expected_payload_message),
                    headers=self.headers,
                ),
            ]

            requests_mock.assert_has_calls(post_call)


class EmailNotificatorTest(unittest.TestCase):
    def setUp(self):
        self.a_fake_sender_email = "email@fake.com"
        self.a_fake_sender_login_credential = "fake_credential"
        self.a_fake_destination_email = self.a_fake_sender_email
        self.a_notification = "A normal text."
        self.default_subject_message = "Python script notification email"

    def _post_call(self, expected_content) -> List:
        post_call = [
            call.starttls(),
            call.login(self.a_fake_sender_email, self.a_fake_sender_login_credential),
            call.sendmail(
                from_addr=self.a_fake_sender_email,
                to_addrs=self.a_fake_destination_email,
                msg=expected_content,
            ),
        ]
        return post_call

    def test_givenAEmailNotificator_whenSendNotification_thenSendMessageDefaultSubject(
        self,
    ):
        a_mock_smtp_server = MagicMock()
        email_notificator = EmailNotificator(
            self.a_fake_sender_email,
            self.a_fake_sender_login_credential,
            self.a_fake_destination_email,
            a_mock_smtp_server,
        )

        email_notificator.send_notification(self.a_notification)

        expected_content = f"Subject: {self.default_subject_message}\n\n{self.a_notification}"

        post_call = self._post_call(expected_content)

        a_mock_smtp_server.assert_has_calls(post_call)

    def test_givenAEmailNotificator_whenSendNotificationWithSubject_thenSendMessageWithSubject(
        self,
    ):
        a_mock_smtp_server = MagicMock()
        email_notificator = EmailNotificator(
            self.a_fake_sender_email,
            self.a_fake_sender_login_credential,
            self.a_fake_destination_email,
            a_mock_smtp_server,
        )

        a_user_formatted_subject = "Here a subject"
        email_notificator.send_notification(self.a_notification, subject=a_user_formatted_subject)

        expected_content = f"Subject: {a_user_formatted_subject}\n\n{self.a_notification}"

        post_call = self._post_call(expected_content)

        a_mock_smtp_server.assert_has_calls(post_call)

    def test_givenAEmailNotificator_whenSendNotificationDoesNotWork_thenWaitTimer(self):
        a_mock_smtp_server = MagicMock()
        a_mock_smtp_server.sendmail.side_effect = SMTPRecipientsRefused("a_fake_recipients")

        email_notificator = EmailNotificator(
            self.a_fake_sender_email,
            self.a_fake_sender_login_credential,
            self.a_fake_destination_email,
            a_mock_smtp_server,
            on_error_sleep_time=1,
        )

        with self.assertWarns(Warning):
            email_notificator.send_notification(self.a_notification)

            expected_content = f"Subject: {self.default_subject_message}\n\n{self.a_notification}"
            post_call = [
                call.starttls(),
                call.login(self.a_fake_sender_email, self.a_fake_sender_login_credential),
                call.sendmail(
                    from_addr=self.a_fake_sender_email,
                    to_addrs=self.a_fake_destination_email,
                    msg=expected_content,
                ),
                call.sendmail(
                    from_addr=self.a_fake_sender_email,
                    to_addrs=self.a_fake_destination_email,
                    msg=expected_content,
                ),
            ]

            a_mock_smtp_server.assert_has_calls(post_call)


class ChannelNotificatorTest(unittest.TestCase):
    def setUp(self):
        self.a_fake_channel_url = "a_channel_url"
        self.a_notification = "A normal text."
        self.default_subject_message = "**Python script notification**\n"

    def _post_call(self, expected_message) -> List:
        post_call = [
            call(endpoint=self.a_fake_channel_url),
            call().send(message=expected_message),
        ]
        return post_call

    @patch("notif.notificator.ChannelNotify", None)
    def test_whenNoRequestsModule_thenRaiseImportError(self):
        with self.assertRaises(ImportError):
            ChannelNotificator(self.a_fake_channel_url)

    @patch("notif.notificator.ChannelNotify")
    def test_givenAChannelNotificator_whenSendNotification_thenSendMessageDefaultSubject(self, channel_notify_mock):
        channel_notificator = ChannelNotificator(self.a_fake_channel_url)

        channel_notificator.send_notification(self.a_notification)

        expected_message = self.default_subject_message + self.a_notification

        post_call = self._post_call(expected_message)

        channel_notify_mock.assert_has_calls(post_call)

    @patch("notif.notificator.ChannelNotify")
    def test_givenAChannelNotificator_whenSendNotificationWithSubject_thenSendMessageWithSubject(
        self, channel_notify_mock
    ):
        a_user_formatted_subject = "Here a subject"

        channel_notificator = ChannelNotificator(self.a_fake_channel_url)

        channel_notificator.send_notification(self.a_notification, subject=a_user_formatted_subject)

        expected_message = f"**{a_user_formatted_subject}**\n" + self.a_notification

        post_call = self._post_call(expected_message)

        channel_notify_mock.assert_has_calls(post_call)

    @patch("notif.notificator.ChannelNotify")
    def test_givenAChannelNotificator_whenSendNotificationDoesNotWork_thenWaitTimer(self, channel_notify_mock):
        channel_notify_mock().send.side_effect = requests.exceptions.HTTPError

        with self.assertWarns(Warning):
            channel_notificator = ChannelNotificator(self.a_fake_channel_url, on_error_sleep_time=1)

            channel_notificator.send_notification(self.a_notification)

            expected_message = self.default_subject_message + self.a_notification
            post_call = [
                call(endpoint=self.a_fake_channel_url),
                call().send(message=expected_message),
                call().send(message=expected_message),
            ]

            channel_notify_mock.assert_has_calls(post_call)


class TeamsNotificatorTest(unittest.TestCase):
    def setUp(self):
        self.a_fake_web_hook = "a_web_hook"
        self.a_notification = "A normal text."
        self.default_subject_message = "**Python script Teams notification**\n"
        self.headers = {"content-type": "application/json"}

    def _post_call(self, expected_message) -> List:
        post_call = [
            call(self.a_fake_web_hook),
            call().text(expected_message),
            call().send(),
        ]
        return post_call

    @patch("notif.notificator.pymsteams", None)
    def test_whenNoRequestsModule_thenRaiseImportError(self):
        with self.assertRaises(ImportError):
            TeamsNotificator(self.a_fake_web_hook, on_error_sleep_time=1)

    @patch("notif.pymsteams.connectorcard")
    def test_givenATeamsNotificator_whenSendNotification_thenSendMessageDefaultSubject(self, pymsteams_mock):
        self.teams_notificator = TeamsNotificator(
            self.a_fake_web_hook, on_error_sleep_time=1
        )  # 1 second since normal is 120
        self.teams_notificator.send_notification(self.a_notification)

        expected_message = self.default_subject_message + self.a_notification

        post_call = self._post_call(expected_message)

        pymsteams_mock.assert_has_calls(post_call)

    @patch("notif.pymsteams.connectorcard")
    def test_givenATeamsNotificator_whenSendNotificationWithSubject_thenSendMessageWithSubject(self, pymsteams_mock):
        self.teams_notificator = TeamsNotificator(
            self.a_fake_web_hook, on_error_sleep_time=1
        )  # 1 second since normal is 120

        a_user_formatted_subject = "Here a subject"
        self.teams_notificator.send_notification(self.a_notification, subject=a_user_formatted_subject)

        expected_message = f"**{a_user_formatted_subject}**\n" + self.a_notification

        post_call = self._post_call(expected_message)

        pymsteams_mock.assert_has_calls(post_call)

    @patch("notif.pymsteams.connectorcard")
    def test_givenATeamsNotificator_whenSendNotificationDoesNotWork_thenWaitTimer(self, pymsteams_mock):
        pymsteams_mock().send.side_effect = pymsteams.TeamsWebhookException

        self.teams_notificator = TeamsNotificator(self.a_fake_web_hook, on_error_sleep_time=1)

        with self.assertWarns(Warning):
            self.teams_notificator.send_notification(self.a_notification)

            expected_message = self.default_subject_message + self.a_notification
            post_call = [
                call(self.a_fake_web_hook),
                call().text(expected_message),
                call().send(),
                call().text(expected_message),
                call().send(),
            ]

            pymsteams_mock.assert_has_calls(post_call)


class DiscordNotificatorTest(unittest.TestCase):
    def setUp(self):
        self.a_fake_web_hook = "a_web_hook"
        self.a_notification = "A normal text."
        self.default_subject_message = "**Python script Discord notification**\n"
        self.headers = {"Content-Type": "application/json"}

    def _post_call(self, expected_payload_message) -> List:
        post_call = [
            call.post(
                url=self.a_fake_web_hook,
                data=json.dumps(expected_payload_message),
                headers=self.headers,
            )
        ]
        return post_call

    @patch("notif.notificator.requests")
    def test_givenADiscordNotificator_whenSendNotification_thenSendMessageDefaultSubject(self, requests_mock):
        discord_notificator = DiscordNotificator(self.a_fake_web_hook)

        discord_notificator.send_notification(self.a_notification)

        expected_payload_message = {"content": self.default_subject_message + self.a_notification}

        post_call = self._post_call(expected_payload_message)

        requests_mock.assert_has_calls(post_call)

    @patch("notif.notificator.requests")
    def test_givenADiscordNotificator_whenSendNotificationWithSubject_thenSendMessageWithSubject(self, requests_mock):
        discord_notificator = DiscordNotificator(self.a_fake_web_hook)

        a_user_formatted_subject = "Here a subject"
        discord_notificator.send_notification(self.a_notification, subject=a_user_formatted_subject)

        expected_payload_message = {"content": "**Here a subject**\n" + self.a_notification}

        post_call = self._post_call(expected_payload_message)

        requests_mock.assert_has_calls(post_call)

    @patch("notif.notificator.requests.post", side_effect=requests.exceptions.HTTPError)
    def test_givenADiscordNotificator_whenSendNotificationDoesNotWork_thenWaitTimer(self, requests_mock):
        discord_notificator = DiscordNotificator(self.a_fake_web_hook, on_error_sleep_time=1)

        with self.assertWarns(Warning):
            discord_notificator.send_notification(self.a_notification)

            expected_payload_message = {"content": self.default_subject_message + self.a_notification}
            post_call = [
                call.post(
                    url=self.a_fake_web_hook,
                    data=json.dumps(expected_payload_message),
                    headers=self.headers,
                ),
                call.post(
                    url=self.a_fake_web_hook,
                    data=json.dumps(expected_payload_message),
                    headers=self.headers,
                ),
            ]

            requests_mock.assert_has_calls(post_call)


if __name__ == "__main__":
    unittest.main()
