tango-gateway
=============

A Tango gateway server

Clients from other networks can connect to the gateway to access the tango
database transparently. It opens ports dynamically when an access to a device
is required and redirects the traffic to the corresponding device. The ZMQ
tango events are also supported.


Requirements
------------

- python >= 3.4
- zmq
- aiozmq
- pytango (optional)
- prometheus_client (optional)


Usage
-----

```
$ tango-gateway -h
usage: tango-gateway [-h] [--bind ADDRESS] [--port PORT] [--tango HOST] [--verbose]

Run a Tango gateway server

optional arguments:
  -h, --help            show this help message and exit
  --bind ADDRESS, -b ADDRESS
                        Specify the bind address (default is all interfaces)
  --port PORT, -p PORT  Port for the server (default is 10000)
  --tango HOST, -t HOST
                        Tango host (default is given by PyTango)
  --promfile PROMFILE   Name of file to write Prometheus metrics to. Requires prometeus_client.
  --verbose, -v
```


Contact
-------

KITS : kitscontrol@maxiv.lu.se
