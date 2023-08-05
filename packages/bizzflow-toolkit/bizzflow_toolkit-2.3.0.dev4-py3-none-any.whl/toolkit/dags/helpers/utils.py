import logging
import os
from typing import Optional

from airflow.utils.email import send_email

from toolkit import current_config

logger = logging.getLogger(__name__)


def get_notify_param(context: dict) -> bool:
    """Check whether we are supposed to send notification or not

    Arguments:

        context {dict} -- Airflow task context variable, but any dictionary will suffice
                            as long as it contains `dag_run`: `DagRun` and `params`: `dict` keys
    """
    external_notify: Optional[bool] = (context.get("dag_run").conf or {}).get("notify")
    # external override (using context configuration JSON in Trigger DAG function)
    if external_notify is not None:
        return external_notify
    # basic settings
    # this is set via DAG and both via Task, task setting suppresses DAG settings,
    # and so we can still have cases when only single task raises notification
    # or only a single task lets it fly
    task_notify: Optional[bool] = context.get("params", {}).get("notify")
    if task_notify is not None:
        return task_notify
    # if we missed anything, better send the notification
    return True


def get_notification_level(context: dict) -> str:
    """Guess whether current failure should raise warning or error notification

    Arguments:

        context {dict} -- Airflow task context variable, but any dictionary will suffice
                            as long as it contains `dag_run`: `DagRun` and `params`: `dict` keys
    """
    continue_on_error: bool = context.get("params", {}).get("continue_on_error", False)
    if continue_on_error:
        return "warning"
    return "error"


def notify_email(contextDict, **kwargs):
    """Send custom email alerts from airflow."""

    notification_emails = current_config.notification_emails
    notify = get_notify_param(contextDict)
    if not notify:
        logger.info("Not sending notification due to configuration")
        return
    if not notification_emails:
        logger.warning("Notification email is not specified, no notification will be sent.")
        return
    logger.info("Sending notification to %s", ", ".join(notification_emails))
    template_location = os.path.join(os.path.dirname(__file__), "template.html")
    with open(template_location, encoding="utf-8") as fid:
        template = fid.read()
    ti = contextDict["task_instance"]
    logs_path = ti.log_filepath[:-4]
    logs = os.listdir(logs_path)
    logs.sort()
    log_path = os.path.join(logs_path, logs[-1])
    notification_level = get_notification_level(contextDict)
    with open(log_path) as logfile:
        log = logfile.read()
    log_tail = "\n".join([line for line in log.split("\n")][-20:])

    # email title.
    title = "Bizzflow: {dag._dag_id} - {task.task_id} failed".format(**contextDict)

    # email contents
    body = template.format(**contextDict, log=log_tail, level=notification_level)
    for email in notification_emails:
        send_email(email, title, body, mime_charset="utf-8")
