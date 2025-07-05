"""
VESC Data Types and Constants

This module contains all the constants, enums, and data structures used by the VESC protocol.
Based on the VESC Tool datatypes and command definitions.
"""

from enum import IntEnum
from dataclasses import dataclass
from typing import List, Optional
import struct

# VESC Communication Commands (from COMM_PACKET_ID)
class VESCCommands(IntEnum):
    """VESC UART/CAN command packet IDs"""
    FW_VERSION = 0
    JUMP_TO_BOOTLOADER = 1
    ERASE_NEW_APP = 2
    WRITE_NEW_APP_DATA = 3
    GET_VALUES = 4
    SET_DUTY = 5
    SET_CURRENT = 6
    SET_CURRENT_BRAKE = 7
    SET_RPM = 8
    SET_POS = 9
    SET_HANDBRAKE = 10
    SET_DETECT = 11
    SET_SERVO_POS = 12
    SET_MCCONF = 13
    GET_MCCONF = 14
    GET_MCCONF_DEFAULT = 15
    SET_APPCONF = 16
    GET_APPCONF = 17
    GET_APPCONF_DEFAULT = 18
    SAMPLE_PRINT = 19
    TERMINAL_CMD = 20
    PRINT = 21
    ROTOR_POSITION = 22
    EXPERIMENT_SAMPLE = 23
    DETECT_MOTOR_PARAM = 24
    DETECT_MOTOR_R_L = 25
    DETECT_MOTOR_FLUX_LINKAGE = 26
    DETECT_ENCODER = 27
    DETECT_HALL_FOC = 28
    REBOOT = 29
    ALIVE = 30
    GET_DECODED_PPM = 31
    GET_DECODED_ADC = 32
    GET_DECODED_CHUK = 33
    FORWARD_CAN = 34
    SET_CHUCK_DATA = 35
    CUSTOM_APP_DATA = 36
    NRF_START_PAIRING = 37
    GPD_SET_FSW = 38
    GPD_BUFFER_NOTIFY = 39
    GPD_BUFFER_SIZE_LEFT = 40
    GPD_FILL_BUFFER = 41
    GPD_OUTPUT_SAMPLE = 42
    GPD_SET_MODE = 43
    GPD_FILL_BUFFER_INT8 = 44
    GPD_FILL_BUFFER_INT16 = 45
    GPD_SET_BUFFER_INT_SCALE = 46
    GET_VALUES_SETUP = 47
    SET_MCCONF_TEMP = 48
    SET_MCCONF_TEMP_SETUP = 49
    GET_VALUES_SELECTIVE = 50
    GET_VALUES_SETUP_SELECTIVE = 51
    EXT_NRF_PRESENT = 52
    EXT_NRF_ESB_SET_CH_ADDR = 53
    EXT_NRF_ESB_SEND_DATA = 54
    EXT_NRF_ESB_RX_DATA = 55
    EXT_NRF_SET_ENABLED = 56
    DETECT_MOTOR_FLUX_LINKAGE_OPENLOOP = 57
    DETECT_APPLY_ALL_FOC = 58
    JUMP_TO_BOOTLOADER_ALL_CAN = 59
    ERASE_NEW_APP_ALL_CAN = 60
    WRITE_NEW_APP_DATA_ALL_CAN = 61
    PING_CAN = 62
    APP_DISABLE_OUTPUT = 63
    TERMINAL_CMD_SYNC = 64
    GET_IMU_DATA = 65
    BM_CONNECT = 66
    BM_ERASE_FLASH_ALL = 67
    BM_WRITE_FLASH = 68
    BM_REBOOT = 69
    BM_DISCONNECT = 70
    BM_MAP_PINS_DEFAULT = 71
    BM_MAP_PINS_NRF5X = 72
    ERASE_BOOTLOADER = 73
    ERASE_BOOTLOADER_ALL_CAN = 74
    PLOT_INIT = 75
    PLOT_DATA = 76
    PLOT_ADD_GRAPH = 77
    PLOT_SET_GRAPH = 78
    GET_DECODED_BALANCE = 79
    BM_MEM_READ = 80
    WRITE_NEW_APP_DATA_LZO = 81
    WRITE_NEW_APP_DATA_ALL_CAN_LZO = 82
    BM_WRITE_FLASH_LZO = 83
    SET_CURRENT_REL = 84
    CAN_FWD_FRAME = 85
    SET_BATTERY_CUT = 86
    SET_BLE_NAME = 87
    SET_BLE_PIN = 88
    SET_CAN_MODE = 89
    GET_IMU_CALIBRATION = 90
    GET_MCCONF_TEMP = 91
    GET_CUSTOM_CONFIG_XML = 92
    GET_CUSTOM_CONFIG = 93
    GET_CUSTOM_CONFIG_DEFAULT = 94
    SET_CUSTOM_CONFIG = 95
    BMS_GET_VALUES = 96
    BMS_SET_CHARGE_ALLOWED = 97
    BMS_SET_BALANCE_OVERRIDE = 98
    BMS_RESET_COUNTERS = 99
    BMS_FORCE_BALANCE = 100
    BMS_ZERO_CURRENT_OFFSET = 101
    JUMP_TO_BOOTLOADER_HW = 102
    ERASE_NEW_APP_HW = 103
    WRITE_NEW_APP_DATA_HW = 104
    ERASE_BOOTLOADER_HW = 105
    JUMP_TO_BOOTLOADER_ALL_CAN_HW = 106
    ERASE_NEW_APP_ALL_CAN_HW = 107
    WRITE_NEW_APP_DATA_ALL_CAN_HW = 108
    ERASE_BOOTLOADER_ALL_CAN_HW = 109
    SET_ODOMETER = 110
    PSW_GET_STATUS = 111
    PSW_SWITCH = 112
    BMS_FWD_CAN_RX = 113
    BMS_HW_DATA = 114
    GET_BATTERY_CUT = 115
    BM_HALT_REQ = 116
    GET_QML_UI_HW = 117
    GET_QML_UI_APP = 118
    CUSTOM_HW_DATA = 119
    QMLUI_ERASE = 120
    QMLUI_WRITE = 121
    IO_BOARD_GET_ALL = 122
    IO_BOARD_SET_PWM = 123
    IO_BOARD_SET_DIGITAL = 124
    BM_MEM_WRITE = 125
    BMS_BLNC_SELFTEST = 126
    GET_EXT_HUM_TMP = 127
    GET_STATS = 128
    RESET_STATS = 129
    LISP_READ_CODE = 130
    LISP_WRITE_CODE = 131
    LISP_ERASE_CODE = 132
    LISP_SET_RUNNING = 133
    LISP_GET_STATS = 134
    LISP_PRINT = 135
    BMS_SET_BATT_TYPE = 136
    BMS_GET_BATT_TYPE = 137
    LISP_REPL_CMD = 138
    LISP_STREAM_CODE = 139
    FILE_LIST = 140
    FILE_READ = 141
    FILE_WRITE = 142
    FILE_MKDIR = 143
    FILE_REMOVE = 144
    LOG_START = 145
    LOG_STOP = 146
    LOG_CONFIG_FIELD = 147
    LOG_DATA_F32 = 148
    SET_APPCONF_NO_STORE = 149
    GET_GNSS = 150
    LOG_DATA_F64 = 151
    LISP_RMSG = 152
    SHUTDOWN = 156
    FW_INFO = 157
    CAN_UPDATE_BAUD_ALL = 158
    MOTOR_ESTOP = 159

# CAN Command IDs (from CAN_PACKET_ID)
class VESCCANCommands(IntEnum):
    """VESC CAN packet command IDs"""
    SET_DUTY = 0
    SET_CURRENT = 1
    SET_CURRENT_BRAKE = 2
    SET_RPM = 3
    SET_POS = 4
    FILL_RX_BUFFER = 5
    FILL_RX_BUFFER_LONG = 6
    PROCESS_RX_BUFFER = 7
    PROCESS_SHORT_BUFFER = 8
    STATUS = 9
    SET_CURRENT_REL = 10
    SET_CURRENT_BRAKE_REL = 11
    SET_CURRENT_HANDBRAKE = 12
    SET_CURRENT_HANDBRAKE_REL = 13
    STATUS_2 = 14
    STATUS_3 = 15
    STATUS_4 = 16
    PING = 17
    PONG = 18
    DETECT_APPLY_ALL_FOC = 19
    DETECT_APPLY_ALL_FOC_RES = 20
    CONF_CURRENT_LIMITS = 21
    CONF_STORE_CURRENT_LIMITS = 22
    CONF_CURRENT_LIMITS_IN = 23
    CONF_STORE_CURRENT_LIMITS_IN = 24
    CONF_FOC_ERPMS = 25
    CONF_STORE_FOC_ERPMS = 26
    STATUS_5 = 27
    POLL_TS5700N8501_STATUS = 28
    CONF_BATTERY_CUT = 29
    CONF_STORE_BATTERY_CUT = 30
    SHUTDOWN = 31
    IO_BOARD_ADC_1_TO_4 = 32
    IO_BOARD_ADC_5_TO_8 = 33
    IO_BOARD_ADC_9_TO_12 = 34
    IO_BOARD_DIGITAL_IN = 35
    IO_BOARD_SET_OUTPUT_DIGITAL = 36
    IO_BOARD_SET_OUTPUT_PWM = 37
    BMS_V_TOT = 38
    BMS_I = 39
    BMS_AH_WH = 40
    BMS_V_CELL = 41
    BMS_BAL = 42
    BMS_TEMPS = 43
    BMS_HUM = 44
    BMS_SOC_SOH_TEMP_STAT = 45
    PSW_STAT = 46
    PSW_SWITCH = 47
    BMS_HW_DATA_1 = 48
    BMS_HW_DATA_2 = 49
    BMS_HW_DATA_3 = 50
    BMS_HW_DATA_4 = 51
    BMS_HW_DATA_5 = 52
    BMS_AH_WH_CHG_TOTAL = 53
    BMS_AH_WH_DIS_TOTAL = 54
    UPDATE_PID_POS_OFFSET = 55
    POLL_ROTOR_POS = 56
    NOTIFY_BOOT = 57
    STATUS_6 = 58
    GNSS_TIME = 59
    GNSS_LAT = 60
    GNSS_LON = 61
    GNSS_ALT_SPEED_HDOP = 62
    UPDATE_BAUD = 63

# VESC Fault Codes (from mc_fault_code)
class VESCFaultCode(IntEnum):
    """VESC fault codes"""
    NONE = 0
    OVER_VOLTAGE = 1
    UNDER_VOLTAGE = 2
    DRV = 3
    ABS_OVER_CURRENT = 4
    OVER_TEMP_FET = 5
    OVER_TEMP_MOTOR = 6
    GATE_DRIVER_OVER_VOLTAGE = 7
    GATE_DRIVER_UNDER_VOLTAGE = 8
    MCU_UNDER_VOLTAGE = 9
    BOOTING_FROM_WATCHDOG_RESET = 10
    ENCODER_SPI = 11
    ENCODER_SINCOS_BELOW_MIN_AMPLITUDE = 12
    ENCODER_SINCOS_ABOVE_MAX_AMPLITUDE = 13
    FLASH_CORRUPTION = 14
    HIGH_OFFSET_CURRENT_SENSOR_1 = 15
    HIGH_OFFSET_CURRENT_SENSOR_2 = 16
    HIGH_OFFSET_CURRENT_SENSOR_3 = 17
    UNBALANCED_CURRENTS = 18
    BRK = 19
    RESOLVER_LOT = 20
    RESOLVER_DOS = 21
    RESOLVER_LOS = 22
    FLASH_CORRUPTION_APP_CFG = 23
    FLASH_CORRUPTION_MC_CFG = 24
    ENCODER_NO_MAGNET = 25
    ENCODER_MAGNET_TOO_STRONG = 26
    PHASE_FILTER = 27
    ENCODER_FAULT = 28

# Hardware Types
class VESCHardwareType(IntEnum):
    """VESC hardware types"""
    VESC = 0
    VESC_BMS = 1
    CUSTOM_MODULE = 2

# ADC Control Types
class VESCADCControlType(IntEnum):
    """ADC control types"""
    NONE = 0
    CURRENT = 1
    CURRENT_REV_CENTER = 2
    CURRENT_REV_BUTTON = 3
    CURRENT_REV_BUTTON_BRAKE_ADC = 4
    CURRENT_REV_BUTTON_BRAKE_CENTER = 5
    CURRENT_NOREV_BRAKE_CENTER = 6
    CURRENT_NOREV_BRAKE_BUTTON = 7
    CURRENT_NOREV_BRAKE_ADC = 8
    DUTY = 9
    DUTY_REV_CENTER = 10
    DUTY_REV_BUTTON = 11
    PID = 12
    PID_REV_CENTER = 13
    PID_REV_BUTTON = 14

# Display Position Mode
class VESCDisplayPositionMode(IntEnum):
    """Display position modes"""
    NONE = 0
    INDUCTANCE = 1
    OBSERVER = 2
    ENCODER = 3
    PID_POS = 4
    PID_POS_ERROR = 5
    ENCODER_OBSERVER_ERROR = 6
    HALL_OBSERVER_ERROR = 7

# Debug Sampling Mode
class VESCDebugSamplingMode(IntEnum):
    """Debug sampling modes"""
    OFF = 0
    NOW = 1
    START = 2
    TRIGGER_START = 3
    TRIGGER_FAULT = 4
    TRIGGER_START_NOSEND = 5
    TRIGGER_FAULT_NOSEND = 6
    SEND_LAST_SAMPLES = 7
    SEND_SINGLE_SAMPLE = 8

# GPD Output Mode
class VESCGPDOutputMode(IntEnum):
    """General purpose drive output modes"""
    NONE = 0
    MODULATION = 1
    VOLTAGE = 2
    CURRENT = 3

# Configuration Value Types
class VESCConfigType(IntEnum):
    """Configuration value types"""
    UNDEFINED = 0
    DOUBLE = 1
    INT = 2
    QSTRING = 3
    ENUM = 4
    BOOL = 5
    BITFIELD = 6

# VESC Transmission Types
class VESCTransmissionType(IntEnum):
    """VESC transmission types"""
    UNDEFINED = 0
    UINT8 = 1
    INT8 = 2
    UINT16 = 3
    INT16 = 4
    UINT32 = 5
    INT32 = 6
    DOUBLE16 = 7
    DOUBLE32 = 8
    DOUBLE32_AUTO = 9

# NRF Pairing Results
class VESCNRFPairResult(IntEnum):
    """NRF pairing results"""
    STARTED = 0
    OK = 1
    FAIL = 2

# Status message masks for selective reading
class VESCStatusMask:
    """Bit masks for selective status reading"""
    TEMP_MOS = 1 << 0
    TEMP_MOTOR = 1 << 1
    CURRENT_MOTOR = 1 << 2
    CURRENT_IN = 1 << 3
    ID = 1 << 4
    IQ = 1 << 5
    RPM = 1 << 6
    DUTY_NOW = 1 << 7
    AMP_HOURS = 1 << 8
    AMP_HOURS_CHARGED = 1 << 9
    WATT_HOURS = 1 << 10
    WATT_HOURS_CHARGED = 1 << 11
    TACHOMETER = 1 << 12
    TACHOMETER_ABS = 1 << 13
    POSITION = 1 << 14
    FAULT_CODE = 1 << 15
    VESC_ID = 1 << 16
    TEMP_MOS_1 = 1 << 17
    TEMP_MOS_2 = 1 << 18
    TEMP_MOS_3 = 1 << 19
    VD = 1 << 20
    VQ = 1 << 21
    HAS_TIMEOUT = 1 << 22
    KILL_SW_ACTIVE = 1 << 23
    V_IN = 1 << 24

# CAN message structure constants
CAN_PACKET_TIMEOUT = 0.1  # 100ms timeout for CAN responses
CAN_FORWARDED_FRAME_TIMEOUT = 0.5  # 500ms timeout for forwarded frames
CAN_STATUS_MSGS_TO_STORE = 10  # Number of status messages to store in cache

# Status message frequencies
STATUS_MSG_FREQUENCY = 50  # Hz - frequency of status messages from VESC
HEARTBEAT_FREQUENCY = 20   # Hz - frequency of heartbeat messages to send
PING_TIMEOUT = 1.0         # seconds - timeout for ping responses

# Node ID ranges
NODE_ID_MIN = 64          # Minimum node ID for Raspberry Pi devices
NODE_ID_MAX = 127         # Maximum node ID for Raspberry Pi devices

# Packet size constants
CAN_FRAME_MAX_SIZE = 8    # Maximum CAN frame data size
VESC_PACKET_MAX_SIZE = 512 # Maximum VESC packet size

@dataclass
class VESCValues:
    """VESC motor controller values (from MC_VALUES struct)"""
    v_in: float = 0.0                    # Input voltage
    temp_mos: float = 0.0                # MOSFET temperature
    temp_mos_1: float = 0.0              # MOSFET 1 temperature
    temp_mos_2: float = 0.0              # MOSFET 2 temperature
    temp_mos_3: float = 0.0              # MOSFET 3 temperature
    temp_motor: float = 0.0              # Motor temperature
    current_motor: float = 0.0           # Motor current
    current_in: float = 0.0              # Input current
    id: float = 0.0                      # Direct current
    iq: float = 0.0                      # Quadrature current
    rpm: float = 0.0                     # RPM
    duty_now: float = 0.0                # Current duty cycle
    amp_hours: float = 0.0               # Amp hours consumed
    amp_hours_charged: float = 0.0       # Amp hours charged
    watt_hours: float = 0.0              # Watt hours consumed
    watt_hours_charged: float = 0.0      # Watt hours charged
    tachometer: int = 0                  # Tachometer value
    tachometer_abs: int = 0              # Absolute tachometer value
    position: float = 0.0                # Motor position
    fault_code: VESCFaultCode = VESCFaultCode.NONE
    vesc_id: int = 0                     # VESC ID
    fault_str: str = ""                  # Fault string
    vd: float = 0.0                      # Direct voltage
    vq: float = 0.0                      # Quadrature voltage
    has_timeout: bool = False            # Communication timeout flag
    kill_sw_active: bool = False         # Kill switch active flag

@dataclass
class VESCSetupValues:
    """VESC setup values (from SETUP_VALUES struct)"""
    temp_mos: float = 0.0
    temp_motor: float = 0.0
    current_motor: float = 0.0
    current_in: float = 0.0
    duty_now: float = 0.0
    rpm: float = 0.0
    speed: float = 0.0
    v_in: float = 0.0
    battery_level: float = 0.0
    amp_hours: float = 0.0
    amp_hours_charged: float = 0.0
    watt_hours: float = 0.0
    watt_hours_charged: float = 0.0
    tachometer: float = 0.0
    tachometer_abs: float = 0.0
    position: float = 0.0
    fault_code: VESCFaultCode = VESCFaultCode.NONE
    vesc_id: int = 0
    num_vescs: int = 0
    battery_wh: float = 0.0
    fault_str: str = ""
    odometer: int = 0
    uptime_ms: int = 0

@dataclass
class VESCIMUValues:
    """VESC IMU values (from IMU_VALUES struct)"""
    roll: float = 0.0
    pitch: float = 0.0
    yaw: float = 0.0
    accX: float = 0.0
    accY: float = 0.0
    accZ: float = 0.0
    gyroX: float = 0.0
    gyroY: float = 0.0
    gyroZ: float = 0.0
    magX: float = 0.0
    magY: float = 0.0
    magZ: float = 0.0
    q0: float = 1.0
    q1: float = 0.0
    q2: float = 0.0
    q3: float = 0.0
    vesc_id: int = 0

@dataclass
class VESCStatValues:
    """VESC statistics values (from STAT_VALUES struct)"""
    speed_avg: float = 0.0
    speed_max: float = 0.0
    power_avg: float = 0.0
    power_max: float = 0.0
    temp_motor_avg: float = 0.0
    temp_motor_max: float = 0.0
    temp_mos_avg: float = 0.0
    temp_mos_max: float = 0.0
    current_avg: float = 0.0
    current_max: float = 0.0
    count_time: float = 0.0
    
    def distance(self) -> float:
        """Calculate distance in meters"""
        return self.speed_avg * self.count_time
    
    def energy(self) -> float:
        """Calculate energy consumption in Wh"""
        return self.power_avg * self.count_time / 3600.0
    
    def ah(self) -> float:
        """Calculate amp hours"""
        return self.current_avg * self.count_time / 3600.0
    
    def efficiency(self) -> float:
        """Calculate efficiency in Wh/km"""
        distance_km = self.distance() / 1000.0
        if distance_km > 0:
            return self.energy() / distance_km
        return 0.0

@dataclass
class VESCBMSValues:
    """VESC BMS values (from BMS_VALUES struct)"""
    v_tot: float = 0.0
    v_charge: float = 0.0
    i_in: float = 0.0
    i_in_ic: float = 0.0
    ah_cnt: float = 0.0
    wh_cnt: float = 0.0
    v_cells: List[float] = None
    temps: List[float] = None
    is_balancing: List[bool] = None
    temp_ic: float = 0.0
    humidity: float = 0.0
    pressure: float = 0.0
    temp_hum_sensor: float = 0.0
    temp_cells_highest: float = 0.0
    soc: float = 0.0
    soh: float = 0.0
    can_id: int = -1
    ah_cnt_chg_total: float = 0.0
    wh_cnt_chg_total: float = 0.0
    ah_cnt_dis_total: float = 0.0
    wh_cnt_dis_total: float = 0.0
    data_version: int = 0
    status: str = ""
    
    def __post_init__(self):
        if self.v_cells is None:
            self.v_cells = []
        if self.temps is None:
            self.temps = []
        if self.is_balancing is None:
            self.is_balancing = []

@dataclass
class VESCFirmwareParams:
    """VESC firmware parameters (from FW_RX_PARAMS struct)"""
    major: int = -1
    minor: int = -1
    fw_name: str = ""
    hw: str = ""
    uuid: bytes = b""
    is_paired: bool = False
    is_test_fw: int = 0
    hw_type: VESCHardwareType = VESCHardwareType.VESC
    custom_config_num: int = 0
    has_phase_filters: bool = False
    has_qml_hw: bool = False
    qml_hw_fullscreen: bool = False
    has_qml_app: bool = False
    qml_app_fullscreen: bool = False
    nrf_name_supported: bool = False
    nrf_pin_supported: bool = False
    hw_conf_crc: int = 0

@dataclass
class VESCEncoderDetectResult:
    """VESC encoder detection result (from ENCODER_DETECT_RES struct)"""
    offset: float = 0.0
    ratio: float = 0.0
    inverted: bool = False
    detect_rx: bool = False

@dataclass
class VESCBLDCDetectResult:
    """VESC BLDC detection result (from bldc_detect struct)"""
    cycle_int_limit: float = 0.0
    bemf_coupling_k: float = 0.0
    hall_table: List[int] = None
    hall_res: int = 0
    
    def __post_init__(self):
        if self.hall_table is None:
            self.hall_table = []

@dataclass
class VESCLispStats:
    """VESC Lisp statistics (from LISP_STATS struct)"""
    cpu_use: float = 0.0
    heap_use: float = 0.0
    mem_use: float = 0.0
    stack_use: float = 0.0
    done_ctx_r: str = ""
    number_bindings: List[tuple] = None
    
    def __post_init__(self):
        if self.number_bindings is None:
            self.number_bindings = []

@dataclass
class VESCIOBoardValues:
    """VESC IO board values (from IO_BOARD_VALUES struct)"""
    id: int = -1
    adc_1_4: List[float] = None
    adc_5_8: List[float] = None
    digital: List[bool] = None
    adc_1_4_age: float = -1.0
    adc_5_8_age: float = -1.0
    digital_age: float = -1.0
    
    def __post_init__(self):
        if self.adc_1_4 is None:
            self.adc_1_4 = []
        if self.adc_5_8 is None:
            self.adc_5_8 = []
        if self.digital is None:
            self.digital = []

@dataclass
class VESCGNSSData:
    """VESC GNSS data (from GNSS_DATA struct)"""
    lat: float = 0.0
    lon: float = 0.0
    height: float = 0.0
    speed: float = 0.0
    hdop: float = 0.0
    ms_today: int = 0
    yy: int = 0
    mo: int = 0
    dd: int = 0
    age_s: float = 0.0

@dataclass
class VESCChuckData:
    """VESC chuck (nunchuck) data (from chuck_data struct)"""
    js_x: int = 0
    js_y: int = 0
    acc_x: int = 0
    acc_y: int = 0
    acc_z: int = 0
    bt_c: bool = False
    bt_z: bool = False

class VESCError(Exception):
    """Base exception for VESC communication errors"""
    pass

class VESCTimeoutError(VESCError):
    """Exception raised when a VESC operation times out"""
    pass

class VESCProtocolError(VESCError):
    """Exception raised when there's a protocol error"""
    pass

class VESCCANError(VESCError):
    """Exception raised when there's a CAN bus error"""
    pass

# Fault code descriptions
FAULT_CODE_DESCRIPTIONS = {
    VESCFaultCode.NONE: "No fault",
    VESCFaultCode.OVER_VOLTAGE: "Over voltage",
    VESCFaultCode.UNDER_VOLTAGE: "Under voltage",
    VESCFaultCode.DRV: "DRV fault",
    VESCFaultCode.ABS_OVER_CURRENT: "Absolute over current",
    VESCFaultCode.OVER_TEMP_FET: "Over temperature FET",
    VESCFaultCode.OVER_TEMP_MOTOR: "Over temperature motor",
    VESCFaultCode.GATE_DRIVER_OVER_VOLTAGE: "Gate driver over voltage",
    VESCFaultCode.GATE_DRIVER_UNDER_VOLTAGE: "Gate driver under voltage",
    VESCFaultCode.MCU_UNDER_VOLTAGE: "MCU under voltage",
    VESCFaultCode.BOOTING_FROM_WATCHDOG_RESET: "Booting from watchdog reset",
    VESCFaultCode.ENCODER_SPI: "Encoder SPI fault",
    VESCFaultCode.ENCODER_SINCOS_BELOW_MIN_AMPLITUDE: "Encoder sin/cos below minimum amplitude",
    VESCFaultCode.ENCODER_SINCOS_ABOVE_MAX_AMPLITUDE: "Encoder sin/cos above maximum amplitude",
    VESCFaultCode.FLASH_CORRUPTION: "Flash corruption",
    VESCFaultCode.HIGH_OFFSET_CURRENT_SENSOR_1: "High offset current sensor 1",
    VESCFaultCode.HIGH_OFFSET_CURRENT_SENSOR_2: "High offset current sensor 2",
    VESCFaultCode.HIGH_OFFSET_CURRENT_SENSOR_3: "High offset current sensor 3",
    VESCFaultCode.UNBALANCED_CURRENTS: "Unbalanced currents",
    VESCFaultCode.BRK: "BRK fault",
    VESCFaultCode.RESOLVER_LOT: "Resolver LOT",
    VESCFaultCode.RESOLVER_DOS: "Resolver DOS",
    VESCFaultCode.RESOLVER_LOS: "Resolver LOS",
    VESCFaultCode.FLASH_CORRUPTION_APP_CFG: "Flash corruption app config",
    VESCFaultCode.FLASH_CORRUPTION_MC_CFG: "Flash corruption motor config",
    VESCFaultCode.ENCODER_NO_MAGNET: "Encoder no magnet",
    VESCFaultCode.ENCODER_MAGNET_TOO_STRONG: "Encoder magnet too strong",
    VESCFaultCode.PHASE_FILTER: "Phase filter fault",
    VESCFaultCode.ENCODER_FAULT: "Encoder fault",
}

def get_fault_string(fault_code: VESCFaultCode) -> str:
    """Get human-readable fault description"""
    return FAULT_CODE_DESCRIPTIONS.get(fault_code, f"Unknown fault code: {fault_code}")

# Status message commands that are cached automatically
STATUS_COMMANDS = {
    VESCCANCommands.STATUS,
    VESCCANCommands.STATUS_2,
    VESCCANCommands.STATUS_3,
    VESCCANCommands.STATUS_4,
    VESCCANCommands.STATUS_5,
    VESCCANCommands.STATUS_6,
}

# Commands that require immediate CAN requests (not cached)
REQUEST_COMMANDS = {
    VESCCommands.GET_MCCONF,
    VESCCommands.GET_APPCONF,
    VESCCommands.GET_DECODED_PPM,
    VESCCommands.GET_DECODED_ADC,
    VESCCommands.GET_DECODED_CHUK,
    VESCCommands.GET_IMU_DATA,
    VESCCommands.GET_STATS,
    VESCCommands.BMS_GET_VALUES,
    VESCCommands.GET_GNSS,
    VESCCommands.FW_VERSION,
    VESCCommands.GET_BATTERY_CUT,
    VESCCommands.GET_CUSTOM_CONFIG,
    VESCCommands.LISP_GET_STATS,
    VESCCommands.IO_BOARD_GET_ALL,
}