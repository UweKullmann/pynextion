import pytest
from .config import PORT_DEFAULT
import time
from pynextion import PySerialNex
from pynextion.widgets import NexPage, NexWaveform
from pynextion.color import NamedColor
import random
import datetime


@pytest.mark.parametrize("port", [PORT_DEFAULT])
@pytest.mark.parametrize("delay", [10])
def test_waveform(port, delay):
    nexSerial = PySerialNex(port)

    nexPage = NexPage(nexSerial, "pg_waveform", pid=12)

    nexWaveform = NexWaveform(nexSerial, "s0", cid=2)

    nexSerial.send("cls WHITE")
    nexPage.show()

    nexWaveform.grid.width = 20
    nexWaveform.grid.height = 20
    nexWaveform.grid.color = NamedColor.GRAY

    time.sleep(1)

    # send(nexSerial, "s0.pco0=65535")

    # nb_channels = len(nexWaveform.channels)
    # @test nb_channels == 4
    nb_channels = 4

    channel = nexWaveform.channels[2]  # 0, 1, 2, 3
    channel.color = NamedColor.RED

    # channel.append(123)  # values in 0:255 (add cid,chid,val)
    # channel.append(133)  # values in 0:255 (add)
    # channel.append(143)  # values in 0:255 (add)
    # channel.append(153)  # values in 0:255 (add)

    # channel.append([123, 133, 143, 153, 163, 173, 183])  # (addt)

    vals = [51 * x for x in range(1, 5)]
    dt_start = datetime.datetime.utcnow()
    while True:
        for ch in range(nb_channels):
            channel = nexWaveform.channels[ch]
            val = vals[ch]
            channel.append(val)
            vals[ch] = int(vals[ch] + 2 * random.uniform(-1, 1))
        if datetime.datetime.utcnow() - dt_start > datetime.timedelta(seconds=delay):
            break
        time.sleep(0.01)
