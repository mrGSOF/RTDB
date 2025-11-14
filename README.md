# RTDB
RTDB is a small, lightweight library that provides a minimal in-memory real-time database and a set of signal types used to store timestamped values.


## Installation
---

Clone the repository. The package is small and is intended to be used by importing modules directly from the repository root:

```pwsh
git clone https://github.com/mrGSOF/RTDB
cd RTDB
```

## Quick usage
---

The `RTDB` object holds named signal instances. Signals are appended with values; each append records a timestamp provided by RTDB's time source. Example:

```python
import time
from rtdb import RTDB
from signals import signalContinuous, signalDiscrete, signalMessage

rtdb = RTDB(time.time)
rtdb.addSignal("alt_m",       signalContinuous(maxHistorySize=48))
rtdb.addSignal("state_enum",  signalDiscrete(maxHistorySize=48))
rtdb.addSignal("message_str", signalMessage(maxHistorySize=48))

rtdb.resume()
rtdb["alt_m"].append(1000.0)
rtdb["state_enum"].append(1)
rtdb["message_str"].append("start")

print(rtdb.getJson())
```

## Primary types / API summary
---

RTDB
- RTDB(getTime=None) — constructor, pass a time source function (e.g., time.time).
- addSignal(name, signal) — attach a signal instance under `name`.
- getJson() / saveJson(filename) — export structure (signal names, types, sizes) to JSON.
- loadJson(filename) — create signals from a saved JSON structure.

Signals (common API)
- All signals expose `append(value)` to add a value at current time, `getAt(time_or_offset)` to query by absolute/relative time, `getJson()` for serialization helpers and `print()` for diagnostics.
- signalContinuous — adds linear interpolation between samples when querying at intermediate times.

## License
-------

This project is released under MIT license in the `LICENSE` file.