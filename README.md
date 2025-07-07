🧠 GOAL
Create a headless Python system that:

Continuously listens to CAN messages from a VESC.

Supports sending commands and receiving specific responses without blocking.

Exposes a simple, high-level Python API that students can use to interact with the ESC without understanding CAN.

🧱 SYSTEM OVERVIEW
Runtime Components
Main Event Loop (main.py)
Central controller that:

Initializes the CAN interface.

Continuously listens for incoming CAN messages.

Maintains a registry of pending commands and handles responses.

Routes incoming messages to the correct handler (live stream vs response).

Reads only from the six CAN status messages (Status 1–6) broadcast at 50Hz by the VESC for real-time data.

These messages are parsed using the definitions and logic found in the VESC reference files:

comm_can.c and comm_can.h

(These files will be provided and must be referenced to verify byte structure, scale factors, and offsets.)

VESC Interface Layer (vesc_interface.py)
Encapsulates:

Low-level CAN send/receive.

Command serialization/deserialization.

Pending command tracking (UUID or command ID + timestamp).

Response timeouts and retries.

Command Encoders (commands.py)
Only the following VESC commands require write support:

setDutyCycle

setCurrent

setCurrentBrake

getImuData

All other commands are ignored or unsupported.

Response Parsers (protocol.py)
Parses only:

Real-time Status 1–6 data packets

Responses from the four supported commands above

The structure of all data parsing must be validated against comm_can.c and comm_can.h

🔄 MAIN LOOP DESIGN
Use a non-blocking loop.

For each iteration:

Poll for new CAN messages.

Classify as:

Continuous stream → pass to telemetry handler.

This includes only Status messages 1–6.

Command response → match to pending registry.

Cleanup expired commands.

Telemetry messages should update a shared state object (e.g., live_data), always available to the student API.

No command-response flow should block this loop.

🚩 PENDING COMMAND REGISTRY
All commands that expect a response are stored with:

Timestamp

Expected response ID or parser function

Callback or future to resolve

On matching incoming message:

Call callback with decoded result

Remove from registry

On timeout:

Log failure

Optionally retry (one retry max)

Remove from registry

🧩 MESSAGE FILTERING
Only accept and process messages matching CAN Status 1–6.

All incoming packets must be matched against known ID ranges defined in the VESC firmware.

All other messages should be ignored unless they are known responses to one of the four supported commands:

setDutyCycle, setCurrent, setCurrentBrake, getImuData

Unknown or out-of-spec packets should be logged in debug mode.

🧑‍🎓 STUDENT-FACING API DESIGN (student_api.py)
Purpose:
Allow students to interact with the vehicle via safe, intuitive Python functions.

Guidelines:
No exposure to CAN, message encoding, or protocol IDs.

Return clean data types (e.g., floats, strings, bools).

Fail gracefully with helpful error messages.

Architecture:
All API functions must internally:

Call into the vesc_interface.py send function.

Optionally await a response.

Return the result synchronously or via callback/future.

Easily support individual read functions of  each of the following:

RPM
Motor current
Duty cycle
Amp-hours consumed
Amp-hours charged
Watt-hours consumed
Watt-hours charged
FET temp
Motor temp
Input current
PID position
Tachometer value
Input voltage
ADC voltages from channels EXT, EXT2, EXT3
Servo value



Easily support Write functions of each of the following along with any values that may be returned as a response:

setDutyCycle
setCurrent
setCurrentBrake
getImuData    (and display all of the individual axis data that is returned)


Optionally confirm success by parsing the matching response packet.

Advanced commands (e.g., file access, Lisp):

Not supported in this version.

May be added later with appropriate guards.

🧪 TESTING REQUIREMENTS
Unit tests for all student API methods.

Integration tests simulating CAN message streams.

Ensure runtime stability under:

Heavy live stream traffic

Concurrent command/response flows

Lost or malformed packets

📌 Runtime Environment Notes
You are currently running on a Raspberry Pi Zero 2W with access to a VESC connected via can0 interface (500k baud CAN network).
You can use this live hardware connection to automatically test your code via the CAN bus.

To initialize the CAN interface:

sudo ip link set can0 down
sudo ip link set can0 type can bitrate 500000
sudo ip link set can0 up

To validate it's live: candump can0

The VESC sends Status Messages 1–6 at 50Hz. You must decode them based on comm_can.c and comm_can.h.

There are two devices already on the CAN other than the Raspberry Pi

VESC ID: 74

VESC-Express (ESP32): 2

⚙️ AI Coding Agent Operational Guidelines
🧠 General Behavior
Do not make assumptions.
If you cannot confirm behavior or data structure from a reference file, ask.

Default to minimalism.

Prioritize compatibility. Must run efficiently on Pi Zero 2W.

🔍 Reference Handling
Always reference comm_can.c and comm_can.h for:

CAN packet format

Byte offsets

Unit scaling

Do not decode packets unless their structure is confirmed.

📬 Communication Protocol
Never invent or assume packet formats.

Implement only the confirmed CAN Status 1–6 messages and the four allowed commands.

Validate response decoding with clear error reporting and fallbacks.

🧪 Testing & Safety
Never send motor/movement commands by default.
Only allow when explicitly invoked.

Use candump can0 for safe passive testing.