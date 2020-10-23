# Celestron NexStar Serial Module for Python

A Python 3 module to communicate with Celestron NexStar hand controllers.

This was originally developed to provide a quick way to synchronize time on Celestron NexStar SE models which did not have an RTC.
 
## Connecting via USB to Serial

On newer Celestron NexStar models (after 2016), the hand controller has a
mini-USB port which is basically a Prolific PL2303 USB-to-serial device.

On Windows 10 machines, the driver is automatically installed after selecting
"Search automatically for updated driver software." A new COM port will
appear, e.g. `COM3`.

On most Linux machines, the device automatically detected and usually
presented as `/dev/ttyUSB{n}`.

## Connecting via RJ11 to DB9 Serial

On older Celestron NexStar models, the hand controller has an RJ1 port (a.k.a.
"telephone" port") which can be wired to a regular DB9 serial port. Reference
pinouts can be obtained from:
- https://www.nexstarsite.com/PCControl/RS232Cable.htm

## How to use

Refer to [test_nexstar.py](test_nexstar.py) on how to use.

## Serial command reference

The commands reference were taken from:
- [NexStar Communication Protocol v1.2](NexStar_Communication_Protocol_v1.2.pdf)

## Implementation completeness

| Command Set             | Commands    | Implemented? |
| ----------------------- | ----------- | ------------ |
| Get Position Commands   | E,e,Z,z     | No           |
| GOTO Commands           | R,r,B,b     | No           |
| Sync Commands           | S,s         | No           |
| Tracking Commands       | T,t         | No           |
| Slewing Commands        | P(16,17)    | No           |
| Time/Location Commands  | W,w,H,h     | Yes          |
| GPS Commands            | P(176)      | No           |
| RTC Commands            | P(178)      | No           |
| Miscellaneous Commands  | V,m,K,J,L,M | Yes          |

_Note: 'P' commands are pass-through commands, and the numbers in the bracket denote the device number(s)._

### Roadmap

The following command sets are expected to be implemented next:
- Get Position Commands
- GOTO Commands
- Sync Commands
- Tracking Commands

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Maintainers

- Justin Lee (2020) - https://github.com/detach8
 
## License

This project is licensed under the [GNU General Public License v3.0](LICENSE).
