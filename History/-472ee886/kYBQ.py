"""Test the send_mail function"""
import pytest
from pytest_mock import MockerFixture
from pythoncom import com_error  # pylint: disable=no-name-in-module
import logging
LOGGER = logging.getLogger(__name__)

import outlook_mail.Mail

def test_catch_no_outlook(mocker: MockerFixture) -> None:
    """test if the com_error raised by the win32.Dispatch,
        when calling with "outlook.application" (
        no installed outlook application ?)  results in a sys.exit()

    Args:
        mocker (MockerFixture): pytest MockerFixture
    """
    mock_dispatch = mocker.patch("outllok_mail.mail.win32.Dispatch")
    mock_dispatch.side_effect = com_error("Mocking stimulated win32com.client.Dispatch com_error")
    with pytest.raises(SystemExit):
        outllok_mail.Mail()


def test_catch_outlook_create_item_error(mocker: MockerFixture) -> None:
    """test if the com_error raised by the outlook application,
        when failing to create an item, is handled correct

    Args:
        mocker (MockerFixture): pytest MockerFixture
    """
    # [ ] HACK @KB, @AH workaround, when calling outlook.CreateItem(0)
    # this function helper is called with 0 input, which raises
    # the desired com_error
    def helper(_: int) -> None:
        raise com_error("Mocking stimulated CreateItem com_error")

    mock_dispatch = mocker.patch("outllok_mail.mail.win32.Dispatch")
    # mock_dispatch.configure_mock(return_value=mocker.MagicMock(name="Outlook"))
    # mock_dispatch.Outlook.CreateItem.configure_mock(side_effect=com_error)
    mock_dispatch.configure_mock(return_value=mocker.MagicMock(CreateItem=helper))
    # mock_dispatch.return_value = mocker.Mock(return_value=com_error)
    # mock_dispatch.side_effect = [
    #     [com_error("Mocking stimulated win32com.client.Dispatch com_error")]
    # ]
    with pytest.raises(SystemExit):
        outllok_mail.Mail()


def test_call_send_with_right_params(mocker: MockerFixture) -> None:
    """test if send is called and the parametrs pass the
        function as expected

    Args:
        mocker (MockerFixture): pytest MockerFixture
    """
    mocker.patch("outllok_mail.mail.win32.Dispatch")
    testmail = outllok_mail.Mail()
    to = "firstname.surname@test.de"
    subject = "Test subject"
    body = "Test text"
    is_html = False
    assert testmail.send_mail(to, subject, body, is_html)  # test if function output is True
    assert testmail.mail.Send.called
    assert testmail.mail.To == to
    assert testmail.mail.Subject == subject
    assert testmail.mail.Body == body


def test_catch_send_error(mocker: MockerFixture) -> None:
    """test if the com_error raised by the outlook application,
        when failing to send a mail, is handled correct

    Args:
        mocker (MockerFixture): pytest MockerFixture
    """
    # [ ] HACK @KB, @AH workaround, when calling self.mail.Send
    # this function helper is called, which raises the desired
    # com_error
    def helper() -> None:
        raise com_error("Mocking stimulated Send com_error")

    mock_dispatch = mocker.patch("outllok_mail.mail.win32.Dispatch")
    mock_dispatch.configure_mock(
        name="Level 0",
        return_value=mocker.MagicMock(
            name="Level1",
            CreateItem=mocker.MagicMock(name="Level2", return_value=mocker.MagicMock(name="Level3", Send=helper)),
        ),
    )  # [ ] HACK not configured mocks will also create magicMock objects,
    # with this nested structre it is possible to define what happens,
    # when at Level3 Send is called
    # [ ] TODO the names of the mock objects are only for easier understanding,
    #  possible to delete them
    testmail = outllok_mail.Mail()
    to = "firstname.surname@test.de"
    subject = "Test subject"
    body = "Test text"
    is_html = False
    assert (
        testmail.send_mail(to, subject, body, is_html) is False
    )  # test if function output is False, when com_error is triggered,
    # if send call fails


# [ ] TODO possible to get the mail adress of the test to send himself
# a mail, if desired
@pytest.mark.skip(reason="Really sends a mail to Sehnhui.")
def test_send_mail() -> None:
    """Test the send_mail with a normal body"""
    testmail = outllok_mail.Mail()
    assert testmail.send_mail(
        to="Shenhui.He@partner.bmw.de",
        subject="Test",
        body="This is a test email from pytest.",
        is_html=False,
    )


@pytest.mark.skip(reason="Really sends a mail to Sehnhui.")
def test_send_mail_html() -> None:
    """Test the send_mail with a HTMLbody"""
    testmail = outllok_mail.Mail()
    assert testmail.send_mail(
        to="Shenhui.He@partner.bmw.de",
        subject="Test",
        body="This is a test email with HTMLBody from pytest.",
        is_html=True,
    )


@pytest.mark.skip(reason="Only usefull when outlook is installed.")
def test_send_mail_fail() -> None:
    """Test the send_mail which should fail"""
    testmail = outllok_mail.Mail()
    assert (
        testmail.send_mail(
            to="xxxx",
            subject="Test",
            body="This is a test email with HTMLBody from pytest.",
            is_html=False,
        )
        is False
    )