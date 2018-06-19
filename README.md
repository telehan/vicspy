<p align="center">
<img src="https://github.com/telehan/vicspy/logos/vi.png" alt="Vehinfo logo"/>
</p>

### Vehinfo ValueCAN python utilities and tools

This repository contains some python utilities for CAN network test and analysis with hardware from IntrepidCS hardware and api.

#### Basic tools to display, record, generate and CAN message

* candump.sh : display CAN messages
* diagdump.sh : display diagnostic related messages
* icscandump.py : display received CAN message with timestamp
* icscantx.py : transmit CAN message with ics hardware api
* icsdiagtx.py : transmit diagnostic CAN messages, SF support now.


### Additional Information
Python CLI utilities use following python packages besides of intrepidcs CAN hardware
* [python ics api](https://github.com/intrepidcs/python_ics)
