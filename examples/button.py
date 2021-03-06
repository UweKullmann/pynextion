import pytest
from .config import PORT_DEFAULT
import time
from pynextion import PySerialNex
from pynextion.widgets import NexPage, NexButton, NexNumber
from pynextion.color import NamedColor
import datetime


@pytest.mark.parametrize("port", [PORT_DEFAULT])
@pytest.mark.parametrize("delay", [20])
def test_button(port, delay):
    nexSerial = PySerialNex(port)
    nexSerial.init()

    nexPage = NexPage(nexSerial, "pg_but", pid=8)

    nexButtonPlus = NexButton(nexSerial, "b0", cid=1)
    nexNumber0 = NexNumber(nexSerial, "n0", cid=2)
    nexButtonMinus = NexButton(nexSerial, "b1", cid=3)
    nexButtonEnter = NexButton(nexSerial, "b2", cid=4)  # noqa: F841

    nexPage.show()

    nexButtonPlus.backcolor = NamedColor.GREEN
    nexButtonMinus.backcolor = NamedColor.RED

    # nexNumber0.value = value
    value = nexNumber0.value
    dt_start = datetime.datetime.utcnow()
    while True:
        time.sleep(0.2)
        new_value = nexNumber0.value
        if new_value != value:
            value = new_value
            print(value)
        if datetime.datetime.utcnow() - dt_start > datetime.timedelta(seconds=delay):
            break

    nexSerial.close()
