"""
VESC Protocol Implementation

This module handles encoding and decoding of VESC protocol packets for both
UART and CAN communication. It provides functions to create command packets
and parse response data without handling the actual communication layer.
"""

import struct
import time
from typing import Union, List, Optional, Dict, Any, Tuple
from .datatypes import *

class VESCProtocol:
    """
    VESC protocol encoder/decoder
    
    This class handles the conversion between Python data types and VESC protocol
    packets. It does not handle any actual communication - just data processing.
    """
    
    def __init__(self):
        self.crc16_tab = self._generate_crc16_table()
    
    def _generate_crc16_table(self) -> List[int]:
        """Generate CRC16 lookup table for VESC protocol"""
        table = []
        for i in range(256):
            crc = i << 8
            for _ in range(8):
                if crc & 0x8000:
                    crc = (crc << 1) ^ 0x1021
                else:
                    crc <<= 1
                crc &= 0xFFFF
            table.append(crc)
        return table
    
    def _crc16(self, data: bytes, initial_crc: int = 0) -> int:
        """Calculate CRC16 for VESC protocol"""
        crc = initial_crc
        for byte in data:
            crc = ((crc << 8) ^ self.crc16_tab[((crc >> 8) ^ byte) & 0xFF]) & 0xFFFF
        return crc
    
    def _pack_can_frame(self, command: VESCCANCommands, node_id: int, data: bytes = b'') -> Tuple[int, bytes]:
        """
        Pack data into CAN frame format
        
        Args:
            command: CAN command ID
            node_id: Target node ID (0-255)
            data: Command data payload
            
        Returns:
            Tuple of (CAN ID, CAN data)
        """
        if len(data) > 8:
            raise VESCProtocolError(f"CAN data too long: {len(data)} bytes (max 8)")
        
        # CAN ID format: [8 bits: command] [8 bits: node_id]
        can_id = (command.value << 8) | (node_id & 0xFF)
        return can_id, data
    
    def _unpack_can_frame(self, can_id: int, data: bytes) -> Tuple[int, int, bytes]:
        """
        Unpack CAN frame into command, node_id, and data
        
        Args:
            can_id: CAN arbitration ID
            data: CAN frame data
            
        Returns:
            Tuple of (command, node_id, data)
        """
        command = (can_id >> 8) & 0xFF
        node_id = can_id & 0xFF
        return command, node_id, data
    
    def create_can_set_duty(self, duty: float, node_id: int = 0) -> Tuple[int, bytes]:
        """Create CAN packet to set duty cycle"""
        if not -1.0 <= duty <= 1.0:
            raise VESCProtocolError(f"Duty cycle must be between -1.0 and 1.0, got {duty}")
        
        duty_fixed = int(duty * 100000)
        data = struct.pack('>i', duty_fixed)
        return self._pack_can_frame(VESCCANCommands.SET_DUTY, node_id, data)
    
    def create_can_set_current(self, current: float, node_id: int = 0) -> Tuple[int, bytes]:
        """Create CAN packet to set current in Amperes"""
        current_fixed = int(current * 1000)
        data = struct.pack('>i', current_fixed)
        return self._pack_can_frame(VESCCANCommands.SET_CURRENT, node_id, data)
    
    def create_can_set_current_brake(self, current: float, node_id: int = 0) -> Tuple[int, bytes]:
        """Create CAN packet to set brake current in Amperes"""
        current_fixed = int(abs(current) * 1000)
        data = struct.pack('>i', current_fixed)
        return self._pack_can_frame(VESCCANCommands.SET_CURRENT_BRAKE, node_id, data)
    
    def create_can_set_rpm(self, rpm: int, node_id: int = 0) -> Tuple[int, bytes]:
        """Create CAN packet to set RPM"""
        data = struct.pack('>i', rpm)
        return self._pack_can_frame(VESCCANCommands.SET_RPM, node_id, data)
    
    def create_can_set_position(self, position: float, node_id: int = 0) -> Tuple[int, bytes]:
        """Create CAN packet to set position in degrees"""
        position_fixed = int(position * 1000000)
        data = struct.pack('>i', position_fixed)
        return self._pack_can_frame(VESCCANCommands.SET_POS, node_id, data)
    
    def create_can_set_current_rel(self, current_rel: float, node_id: int = 0) -> Tuple[int, bytes]:
        """Create CAN packet to set relative current (0.0 to 1.0)"""
        if not 0.0 <= current_rel <= 1.0:
            raise VESCProtocolError(f"Relative current must be between 0.0 and 1.0, got {current_rel}")
        
        current_rel_fixed = int(current_rel * 100000)
        data = struct.pack('>i', current_rel_fixed)
        return self._pack_can_frame(VESCCANCommands.SET_CURRENT_REL, node_id, data)
    
    def create_can_set_current_brake_rel(self, current_rel: float, node_id: int = 0) -> Tuple[int, bytes]:
        """Create CAN packet to set relative brake current (0.0 to 1.0)"""
        if not 0.0 <= current_rel <= 1.0:
            raise VESCProtocolError(f"Relative brake current must be between 0.0 and 1.0, got {current_rel}")
        
        current_rel_fixed = int(current_rel * 100000)
        data = struct.pack('>i', current_rel_fixed)
        return self._pack_can_frame(VESCCANCommands.SET_CURRENT_BRAKE_REL, node_id, data)
    
    def create_can_set_handbrake(self, current: float, node_id: int = 0) -> Tuple[int, bytes]:
        """Create CAN packet to set handbrake current"""
        current_fixed = int(current * 1000)
        data = struct.pack('>i', current_fixed)
        return self._pack_can_frame(VESCCANCommands.SET_CURRENT_HANDBRAKE, node_id, data)
    
    def create_can_set_handbrake_rel(self, current_rel: float, node_id: int = 0) -> Tuple[int, bytes]:
        """Create CAN packet to set relative handbrake current"""
        if not 0.0 <= current_rel <= 1.0:
            raise VESCProtocolError(f"Relative handbrake current must be between 0.0 and 1.0, got {current_rel}")
        
        current_rel_fixed = int(current_rel * 100000)
        data = struct.pack('>i', current_rel_fixed)
        return self._pack_can_frame(VESCCANCommands.SET_CURRENT_HANDBRAKE_REL, node_id, data)
    
    def create_can_ping(self, node_id: int = 0) -> Tuple[int, bytes]:
        """Create CAN ping packet"""
        return self._pack_can_frame(VESCCANCommands.PING, node_id, b'')
    
    def create_can_pong(self, node_id: int = 0) -> Tuple[int, bytes]:
        """Create CAN pong packet (response to ping)"""
        return self._pack_can_frame(VESCCANCommands.PONG, node_id, b'')
    
    def create_can_status_request(self, status_type: int = 1, node_id: int = 0) -> Tuple[int, bytes]:
        """Create CAN status request packet"""
        status_commands = {
            1: VESCCANCommands.STATUS,
            2: VESCCANCommands.STATUS_2,
            3: VESCCANCommands.STATUS_3,
            4: VESCCANCommands.STATUS_4,
            5: VESCCANCommands.STATUS_5,
            6: VESCCANCommands.STATUS_6,
        }
        
        if status_type not in status_commands:
            raise VESCProtocolError(f"Invalid status type: {status_type}")
        
        return self._pack_can_frame(status_commands[status_type], node_id, b'')
    
    def parse_can_status_1(self, data: bytes) -> Dict[str, Any]:
        """Parse CAN status message 1 (9 bytes)"""
        if len(data) < 8:
            raise VESCProtocolError(f"Status 1 packet too short: {len(data)} bytes")
        
        # Parse based on VESC CAN protocol
        rpm = struct.unpack('>i', data[0:4])[0]
        current = struct.unpack('>h', data[4:6])[0] / 10.0  # 0.1A resolution
        duty = struct.unpack('>h', data[6:8])[0] / 1000.0   # 0.1% resolution
        
        return {
            'rpm': rpm,
            'current': current,
            'duty': duty,
            'timestamp': time.time()
        }
    
    def parse_can_status_2(self, data: bytes) -> Dict[str, Any]:
        """Parse CAN status message 2 (8 bytes)"""
        if len(data) < 8:
            raise VESCProtocolError(f"Status 2 packet too short: {len(data)} bytes")
        
        amp_hours = struct.unpack('>i', data[0:4])[0] / 10000.0    # 0.1mAh resolution
        amp_hours_charged = struct.unpack('>i', data[4:8])[0] / 10000.0
        
        return {
            'amp_hours': amp_hours,
            'amp_hours_charged': amp_hours_charged,
            'timestamp': time.time()
        }
    
    def parse_can_status_3(self, data: bytes) -> Dict[str, Any]:
        """Parse CAN status message 3 (8 bytes)"""
        if len(data) < 8:
            raise VESCProtocolError(f"Status 3 packet too short: {len(data)} bytes")
        
        watt_hours = struct.unpack('>i', data[0:4])[0] / 10000.0    # 0.1mWh resolution
        watt_hours_charged = struct.unpack('>i', data[4:8])[0] / 10000.0
        
        return {
            'watt_hours': watt_hours,
            'watt_hours_charged': watt_hours_charged,
            'timestamp': time.time()
        }
    
    def parse_can_status_4(self, data: bytes) -> Dict[str, Any]:
        """Parse CAN status message 4 (8 bytes)"""
        if len(data) < 8:
            raise VESCProtocolError(f"Status 4 packet too short: {len(data)} bytes")
        
        temp_fet = struct.unpack('>h', data[0:2])[0] / 10.0     # 0.1°C resolution
        temp_motor = struct.unpack('>h', data[2:4])[0] / 10.0   # 0.1°C resolution
        current_in = struct.unpack('>h', data[4:6])[0] / 10.0   # 0.1A resolution
        pid_pos = struct.unpack('>h', data[6:8])[0] / 50.0      # 0.02° resolution
        
        return {
            'temp_fet': temp_fet,
            'temp_motor': temp_motor,
            'current_in': current_in,
            'pid_pos': pid_pos,
            'timestamp': time.time()
        }
    
    def parse_can_status_5(self, data: bytes) -> Dict[str, Any]:
        """Parse CAN status message 5 (8 bytes)"""
        if len(data) < 8:
            raise VESCProtocolError(f"Status 5 packet too short: {len(data)} bytes")
        
        tachometer = struct.unpack('>i', data[0:4])[0]
        v_in = struct.unpack('>h', data[4:6])[0] / 10.0     # 0.1V resolution
        reserved = struct.unpack('>h', data[6:8])[0]
        
        return {
            'tachometer': tachometer,
            'v_in': v_in,
            'reserved': reserved,
            'timestamp': time.time()
        }
    
    def parse_can_status_6(self, data: bytes) -> Dict[str, Any]:
        """Parse CAN status message 6 (8 bytes)"""
        if len(data) < 8:
            raise VESCProtocolError(f"Status 6 packet too short: {len(data)} bytes")
        
        adc1 = struct.unpack('>h', data[0:2])[0] / 1000.0   # 1mV resolution
        adc2 = struct.unpack('>h', data[2:4])[0] / 1000.0   # 1mV resolution
        adc3 = struct.unpack('>h', data[4:6])[0] / 1000.0   # 1mV resolution
        ppm = struct.unpack('>h', data[6:8])[0] / 1000.0    # 0.1% resolution
        
        return {
            'adc1': adc1,
            'adc2': adc2,
            'adc3': adc3,
            'ppm': ppm,
            'timestamp': time.time()
        }
    
    def parse_can_message(self, can_id: int, data: bytes) -> Optional[Dict[str, Any]]:
        """
        Parse any CAN message and return decoded data
        
        Args:
            can_id: CAN arbitration ID
            data: CAN frame data
            
        Returns:
            Dictionary with parsed data or None if not a status message
        """
        command, node_id, frame_data = self._unpack_can_frame(can_id, data)
        
        try:
            command_enum = VESCCANCommands(command)
        except ValueError:
            # Unknown command
            return None
        
        result = {'command': command_enum, 'node_id': node_id}
        
        # Parse status messages
        if command_enum == VESCCANCommands.STATUS:
            result.update(self.parse_can_status_1(frame_data))
        elif command_enum == VESCCANCommands.STATUS_2:
            result.update(self.parse_can_status_2(frame_data))
        elif command_enum == VESCCANCommands.STATUS_3:
            result.update(self.parse_can_status_3(frame_data))
        elif command_enum == VESCCANCommands.STATUS_4:
            result.update(self.parse_can_status_4(frame_data))
        elif command_enum == VESCCANCommands.STATUS_5:
            result.update(self.parse_can_status_5(frame_data))
        elif command_enum == VESCCANCommands.STATUS_6:
            result.update(self.parse_can_status_6(frame_data))
        elif command_enum == VESCCANCommands.PING:
            result['ping'] = True
        elif command_enum == VESCCANCommands.PONG:
            result['pong'] = True
        else:
            # Other command types - just store raw data
            result['raw_data'] = frame_data
        
        return result
    
    def create_uart_packet(self, command: VESCCommands, data: bytes = b'') -> bytes:
        """
        Create UART packet for VESC communication
        
        Args:
            command: VESC command ID
            data: Command payload data
            
        Returns:
            Complete UART packet with headers and CRC
        """
        # Packet format: [START] [LENGTH] [COMMAND] [DATA] [CRC] [END]
        # START: 0x02 (short packet) or 0x03 (long packet)
        # LENGTH: 1 or 2 bytes depending on packet type
        # COMMAND: 1 byte
        # DATA: 0-N bytes
        # CRC: 2 bytes
        # END: 0x03
        
        payload = struct.pack('B', command.value) + data
        payload_len = len(payload)
        
        if payload_len <= 255:
            # Short packet
            packet = struct.pack('BB', 0x02, payload_len) + payload
        else:
            # Long packet
            packet = struct.pack('>BH', 0x03, payload_len) + payload
        
        # Calculate CRC
        crc = self._crc16(packet[1:])  # CRC of length + payload
        packet += struct.pack('>H', crc)
        packet += struct.pack('B', 0x03)  # End byte
        
        return packet
    
    def parse_uart_packet(self, packet: bytes) -> Optional[Tuple[VESCCommands, bytes]]:
        """
        Parse UART packet from VESC
        
        Args:
            packet: Complete UART packet
            
        Returns:
            Tuple of (command, data) or None if invalid packet
        """
        if len(packet) < 5:  # Minimum packet size
            return None
        
        try:
            start_byte = packet[0]
            
            if start_byte == 0x02:  # Short packet
                if len(packet) < 6:
                    return None
                payload_len = packet[1]
                payload_start = 2
            elif start_byte == 0x03:  # Long packet
                if len(packet) < 7:
                    return None
                payload_len = struct.unpack('>H', packet[1:3])[0]
                payload_start = 3
            else:
                return None
            
            if len(packet) < payload_start + payload_len + 3:  # payload + crc + end
                return None
            
            payload = packet[payload_start:payload_start + payload_len]
            crc_received = struct.unpack('>H', packet[payload_start + payload_len:payload_start + payload_len + 2])[0]
            end_byte = packet[payload_start + payload_len + 2]
            
            if end_byte != 0x03:
                return None
            
            # Verify CRC
            crc_calculated = self._crc16(packet[1:payload_start + payload_len])
            if crc_received != crc_calculated:
                return None
            
            if len(payload) < 1:
                return None
            
            command = VESCCommands(payload[0])
            data = payload[1:]
            
            return command, data
            
        except (struct.error, ValueError):
            return None
    
    def create_uart_get_values(self) -> bytes:
        """Create UART packet to get motor values"""
        return self.create_uart_packet(VESCCommands.GET_VALUES)
    
    def create_uart_get_setup_values(self) -> bytes:
        """Create UART packet to get setup values"""
        return self.create_uart_packet(VESCCommands.GET_VALUES_SETUP)
    
    def create_uart_get_mcconf(self) -> bytes:
        """Create UART packet to get motor configuration"""
        return self.create_uart_packet(VESCCommands.GET_MCCONF)
    
    def create_uart_get_appconf(self) -> bytes:
        """Create UART packet to get app configuration"""
        return self.create_uart_packet(VESCCommands.GET_APPCONF)
    
    def create_uart_get_decoded_ppm(self) -> bytes:
        """Create UART packet to get decoded PPM values"""
        return self.create_uart_packet(VESCCommands.GET_DECODED_PPM)
    
    def create_uart_get_decoded_adc(self) -> bytes:
        """Create UART packet to get decoded ADC values"""
        return self.create_uart_packet(VESCCommands.GET_DECODED_ADC)
    
    def create_uart_get_decoded_chuk(self) -> bytes:
        """Create UART packet to get decoded nunchuck values"""
        return self.create_uart_packet(VESCCommands.GET_DECODED_CHUK)
    
    def create_uart_get_imu_data(self, mask: int = 0xFFFFFFFF) -> bytes:
        """Create UART packet to get IMU data"""
        data = struct.pack('>I', mask)
        return self.create_uart_packet(VESCCommands.GET_IMU_DATA, data)
    
    def create_uart_get_stats(self, mask: int = 0xFFFFFFFF) -> bytes:
        """Create UART packet to get statistics"""
        data = struct.pack('>I', mask)
        return self.create_uart_packet(VESCCommands.GET_STATS, data)
    
    def create_uart_get_gnss(self, mask: int = 0xFFFFFFFF) -> bytes:
        """Create UART packet to get GNSS data"""
        data = struct.pack('>I', mask)
        return self.create_uart_packet(VESCCommands.GET_GNSS, data)
    
    def create_uart_fw_version(self) -> bytes:
        """Create UART packet to get firmware version"""
        return self.create_uart_packet(VESCCommands.FW_VERSION)
    
    def create_uart_terminal_cmd(self, cmd: str) -> bytes:
        """Create UART packet to send terminal command"""
        data = cmd.encode('utf-8') + b'\0'
        return self.create_uart_packet(VESCCommands.TERMINAL_CMD, data)
    
    def create_uart_set_duty(self, duty: float) -> bytes:
        """Create UART packet to set duty cycle"""
        if not -1.0 <= duty <= 1.0:
            raise VESCProtocolError(f"Duty cycle must be between -1.0 and 1.0, got {duty}")
        
        data = struct.pack('>f', duty)
        return self.create_uart_packet(VESCCommands.SET_DUTY, data)
    
    def create_uart_set_current(self, current: float) -> bytes:
        """Create UART packet to set current"""
        data = struct.pack('>f', current)
        return self.create_uart_packet(VESCCommands.SET_CURRENT, data)
    
    def create_uart_set_current_brake(self, current: float) -> bytes:
        """Create UART packet to set brake current"""
        data = struct.pack('>f', current)
        return self.create_uart_packet(VESCCommands.SET_CURRENT_BRAKE, data)
    
    def create_uart_set_rpm(self, rpm: int) -> bytes:
        """Create UART packet to set RPM"""
        data = struct.pack('>i', rpm)
        return self.create_uart_packet(VESCCommands.SET_RPM, data)
    
    def create_uart_set_position(self, position: float) -> bytes:
        """Create UART packet to set position"""
        data = struct.pack('>f', position)
        return self.create_uart_packet(VESCCommands.SET_POS, data)
    
    def create_uart_set_handbrake(self, current: float) -> bytes:
        """Create UART packet to set handbrake current"""
        data = struct.pack('>f', current)
        return self.create_uart_packet(VESCCommands.SET_HANDBRAKE, data)
    
    def parse_uart_values(self, data: bytes) -> VESCValues:
        """Parse UART values response into VESCValues object"""
        if len(data) < 60:  # Approximate minimum size for values packet
            raise VESCProtocolError(f"Values packet too short: {len(data)} bytes")
        
        try:
            offset = 0
            values = VESCValues()
            
            # Parse values according to VESC protocol
            values.temp_mos = struct.unpack('>f', data[offset:offset+4])[0]
            offset += 4
            values.temp_motor = struct.unpack('>f', data[offset:offset+4])[0]
            offset += 4
            values.current_motor = struct.unpack('>f', data[offset:offset+4])[0]
            offset += 4
            values.current_in = struct.unpack('>f', data[offset:offset+4])[0]
            offset += 4
            values.id = struct.unpack('>f', data[offset:offset+4])[0]
            offset += 4
            values.iq = struct.unpack('>f', data[offset:offset+4])[0]
            offset += 4
            values.rpm = struct.unpack('>f', data[offset:offset+4])[0]
            offset += 4
            values.duty_now = struct.unpack('>f', data[offset:offset+4])[0]
            offset += 4
            values.amp_hours = struct.unpack('>f', data[offset:offset+4])[0]
            offset += 4
            values.amp_hours_charged = struct.unpack('>f', data[offset:offset+4])[0]
            offset += 4
            values.watt_hours = struct.unpack('>f', data[offset:offset+4])[0]
            offset += 4
            values.watt_hours_charged = struct.unpack('>f', data[offset:offset+4])[0]
            offset += 4
            values.tachometer = struct.unpack('>i', data[offset:offset+4])[0]
            offset += 4
            values.tachometer_abs = struct.unpack('>i', data[offset:offset+4])[0]
            offset += 4
            values.position = struct.unpack('>f', data[offset:offset+4])[0]
            offset += 4
            
            if len(data) > offset:
                fault_code = struct.unpack('B', data[offset:offset+1])[0]
                values.fault_code = VESCFaultCode(fault_code)
                offset += 1
            
            if len(data) > offset + 4:
                values.v_in = struct.unpack('>f', data[offset:offset+4])[0]
                offset += 4
            
            return values
            
        except (struct.error, ValueError) as e:
            raise VESCProtocolError(f"Error parsing values packet: {e}")
    
    def parse_uart_decoded_ppm(self, data: bytes) -> Dict[str, float]:
        """Parse decoded PPM response"""
        if len(data) < 8:
            raise VESCProtocolError(f"PPM packet too short: {len(data)} bytes")
        
        ppm_value = struct.unpack('>f', data[0:4])[0]
        ppm_last_len = struct.unpack('>f', data[4:8])[0]
        
        return {
            'ppm_value': ppm_value,
            'ppm_last_len': ppm_last_len
        }
    
    def parse_uart_decoded_adc(self, data: bytes) -> Dict[str, float]:
        """Parse decoded ADC response"""
        if len(data) < 16:
            raise VESCProtocolError(f"ADC packet too short: {len(data)} bytes")
        
        adc_value = struct.unpack('>f', data[0:4])[0]
        adc_voltage = struct.unpack('>f', data[4:8])[0]
        adc_value2 = struct.unpack('>f', data[8:12])[0]
        adc_voltage2 = struct.unpack('>f', data[12:16])[0]
        
        return {
            'adc_value': adc_value,
            'adc_voltage': adc_voltage,
            'adc_value2': adc_value2,
            'adc_voltage2': adc_voltage2
        }
    
    def parse_uart_decoded_chuk(self, data: bytes) -> float:
        """Parse decoded nunchuck response"""
        if len(data) < 4:
            raise VESCProtocolError(f"Nunchuck packet too short: {len(data)} bytes")
        
        return struct.unpack('>f', data[0:4])[0]
    
    def parse_uart_fw_version(self, data: bytes) -> VESCFirmwareParams:
        """Parse firmware version response"""
        if len(data) < 6:
            raise VESCProtocolError(f"Firmware version packet too short: {len(data)} bytes")
        
        fw_params = VESCFirmwareParams()
        offset = 0
        
        fw_params.major = struct.unpack('B', data[offset:offset+1])[0]
        offset += 1
        fw_params.minor = struct.unpack('B', data[offset:offset+1])[0]
        offset += 1
        
        # Parse hardware name (null-terminated string)
        hw_name_end = data.find(b'\0', offset)
        if hw_name_end != -1:
            fw_params.hw = data[offset:hw_name_end].decode('utf-8', errors='ignore')
            offset = hw_name_end + 1
        
        # Parse UUID if present
        if len(data) >= offset + 12:
            fw_params.uuid = data[offset:offset+12]
            offset += 12
        
        # Parse additional parameters if present
        if len(data) >= offset + 1:
            flags = struct.unpack('B', data[offset:offset+1])[0]
            fw_params.is_paired = bool(flags & 0x01)
            fw_params.is_test_fw = (flags >> 1) & 0x01
            fw_params.hw_type = VESCHardwareType((flags >> 2) & 0x03)
            
        return fw_params
    
    def create_heartbeat_packet(self, node_id: int) -> Tuple[int, bytes]:
        """
        Create heartbeat packet for Raspberry Pi to announce presence
        
        Args:
            node_id: Our node ID
            
        Returns:
            CAN ID and data for heartbeat message
        """
        # Send a basic status message with dummy data
        # This makes the Pi appear as a VESC-like device on the network
        
        # Use STATUS_5 format: tachometer (4) + voltage (2) + reserved (2)
        tachometer = int(time.time()) % 0xFFFFFFFF  # Use timestamp as dummy tachometer
        voltage = int(3.3 * 10)  # Pi runs at 3.3V, scaled by 10 for VESC format
        reserved = 0x5250  # "RP" in hex for Raspberry Pi
        
        data = struct.pack('>IHH', tachometer, voltage, reserved)
        return self._pack_can_frame(VESCCANCommands.STATUS_5, node_id, data)
    
    def create_firmware_response(self, node_id: int) -> bytes:
        """
        Create firmware version response for Raspberry Pi
        
        Args:
            node_id: Our node ID
            
        Returns:
            UART packet with firmware version response
        """
        # Create firmware version response that identifies us as a Raspberry Pi
        fw_name = "RaspberryPi CAN Node"
        hw_name = "Raspberry Pi"
        
        data = struct.pack('BB', 1, 0)  # Version 1.0
        data += fw_name.encode('utf-8') + b'\0'
        data += hw_name.encode('utf-8') + b'\0'
        data += b'RPICAN' + bytes([node_id]) * 6  # 12-byte UUID-like identifier
        data += struct.pack('B', 0x04)  # Flags: custom module type
        
        return self.create_uart_packet(VESCCommands.FW_VERSION, data)