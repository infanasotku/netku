from aiogram.utils.markdown import hbold

please_click_start = f"Hello! Use {hbold('/start')} to continue."


def generate_proxy_task_message(proxy_id: str) -> str:
    """Generates template message text by `proxy_id`"""
    return f"""{hbold("[Proxy subscription]:")}
New generated proxy id:
{hbold(proxy_id)}
"""


create_booking_account_text = "Add account"
