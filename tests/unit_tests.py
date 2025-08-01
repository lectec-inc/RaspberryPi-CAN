#!/usr/bin/env python3
"""
Unit Tests for VESC CAN System Components
"""

import unittest
import struct
from core.protocol import VESCProtocolParser, VESCStatus1, VESCStatus2, VESCStatus3, VESCStatus4, VESCStatus5, VESCStatus6
from core.commands import VESCCommandEncoder


class TestVESCProtocolParser(unittest.TestCase):
    """Test the protocol parser"""
    
    def setUp(self):
        self.parser = VESCProtocolParser()
    
    def test_controller_id_extraction(self):
        """Test controller ID extraction from CAN ID"""
        # Test case: CAN ID 0x0000094A (Status 1 from controller 74)
        can_id = 0x0000094A
        controller_id = self.parser.extract_controller_id(can_id)
        self.assertEqual(controller_id, 74)
        
        # Test case: CAN ID 0x0000014A (Command from controller 74)
        can_id = 0x0000014A
        controller_id = self.parser.extract_controller_id(can_id)
        self.assertEqual(controller_id, 74)
    
    def test_packet_type_extraction(self):
        """Test packet type extraction from CAN ID"""
        # Test case: CAN ID 0x0000094A (Status 1)
        can_id = 0x0000094A
        packet_type = self.parser.extract_packet_type(can_id)
        self.assertEqual(packet_type, 0x09)
        
        # Test case: CAN ID 0x00000E4A (Status 2)
        can_id = 0x00000E4A
        packet_type = self.parser.extract_packet_type(can_id)
        self.assertEqual(packet_type, 0x0E)
    
    def test_status1_parsing(self):
        """Test Status 1 parsing"""
        # Test data: RPM=1000, Current=5.5A, Duty=0.123
        data = struct.pack('>ihh', 1000, 55, 123)  # RPM, Current*10, Duty*1000
        
        status = self.parser.parse_status_1(data)
        
        self.assertEqual(status.rpm, 1000)
        self.assertEqual(status.current, 5.5)
        self.assertEqual(status.duty_cycle, 0.123)
    
    def test_status2_parsing(self):
        """Test Status 2 parsing"""
        # Test data: AmpHours=1.2345, AmpHoursCharged=0.5678
        data = struct.pack('>ii', 12345, 5678)  # Both scaled by 10000
        
        status = self.parser.parse_status_2(data)
        
        self.assertEqual(status.amp_hours, 1.2345)
        self.assertEqual(status.amp_hours_charged, 0.5678)
    
    def test_status3_parsing(self):
        """Test Status 3 parsing"""
        # Test data: WattHours=2.4689, WattHoursCharged=1.1357
        data = struct.pack('>ii', 24689, 11357)  # Both scaled by 10000
        
        status = self.parser.parse_status_3(data)
        
        self.assertEqual(status.watt_hours, 2.4689)
        self.assertEqual(status.watt_hours_charged, 1.1357)
    
    def test_status4_parsing(self):
        """Test Status 4 parsing"""
        # Test data: FETTemp=35.6°C, MotorTemp=42.1°C, InputCurrent=3.2A, PIDPos=1.5
        data = struct.pack('>hhhh', 356, 421, 32, 75)  # Scaled by 10, 10, 10, 50
        
        status = self.parser.parse_status_4(data)
        
        self.assertEqual(status.temp_fet, 35.6)
        self.assertEqual(status.temp_motor, 42.1)
        self.assertEqual(status.current_in, 3.2)
        self.assertEqual(status.pid_pos_now, 1.5)
    
    def test_status5_parsing(self):
        """Test Status 5 parsing"""
        # Test data: Tachometer=123456, Voltage=24.5V
        data = struct.pack('>ih', 123456, 245)  # Voltage scaled by 10
        
        status = self.parser.parse_status_5(data)
        
        self.assertEqual(status.tacho_value, 123456)
        self.assertEqual(status.v_in, 24.5)
    
    def test_status6_parsing(self):
        """Test Status 6 parsing"""
        # Test data: ADC1=1.234V, ADC2=2.345V, ADC3=3.456V, PPM=0.789
        data = struct.pack('>hhhh', 1234, 2345, 3456, 789)  # All scaled by 1000
        
        status = self.parser.parse_status_6(data)
        
        self.assertEqual(status.adc_1, 1.234)
        self.assertEqual(status.adc_2, 2.345)
        self.assertEqual(status.adc_3, 3.456)
        self.assertEqual(status.ppm, 0.789)
    
    def test_message_parsing(self):
        """Test complete message parsing"""
        # Test Status 1 message
        can_id = 0x0000094A  # Status 1 from controller 74
        data = struct.pack('>ihh', 1500, 75, 250)  # RPM=1500, Current=7.5A, Duty=0.25
        
        parsed = self.parser.parse_message(can_id, data)
        
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed['controller_id'], 74)
        self.assertEqual(parsed['type'], 'status_1')
        self.assertEqual(parsed['data'].rpm, 1500)
        self.assertEqual(parsed['data'].current, 7.5)
        self.assertEqual(parsed['data'].duty_cycle, 0.25)


class TestVESCCommandEncoder(unittest.TestCase):
    """Test the command encoder"""
    
    def setUp(self):
        self.encoder = VESCCommandEncoder()
    
    def test_duty_cycle_encoding(self):
        """Test duty cycle command encoding"""
        # Test case: Controller 74, Duty 0.5
        can_id, data = self.encoder.encode_set_duty_cycle(74, 0.5)
        
        self.assertEqual(can_id, 0x0000004A)  # Controller 74, packet type 0
        self.assertEqual(data, struct.pack('>i', 50000))  # 0.5 * 100000
        
        # Test case: Controller 74, Duty -0.25
        can_id, data = self.encoder.encode_set_duty_cycle(74, -0.25)
        
        self.assertEqual(can_id, 0x0000004A)
        self.assertEqual(data, struct.pack('>i', -25000))  # -0.25 * 100000
    
    def test_current_encoding(self):
        """Test current command encoding"""
        # Test case: Controller 74, Current 10.5A
        can_id, data = self.encoder.encode_set_current(74, 10.5)
        
        self.assertEqual(can_id, 0x0000014A)  # Controller 74, packet type 1
        self.assertEqual(data, struct.pack('>i', 10500))  # 10.5 * 1000
        
        # Test case: Controller 74, Current -5.0A
        can_id, data = self.encoder.encode_set_current(74, -5.0)
        
        self.assertEqual(can_id, 0x0000014A)
        self.assertEqual(data, struct.pack('>i', -5000))  # -5.0 * 1000
    
    def test_brake_current_encoding(self):
        """Test brake current command encoding"""
        # Test case: Controller 74, Brake 3.0A
        can_id, data = self.encoder.encode_set_current_brake(74, 3.0)
        
        self.assertEqual(can_id, 0x0000024A)  # Controller 74, packet type 2
        self.assertEqual(data, struct.pack('>i', 3000))  # 3.0 * 1000
    
    def test_imu_data_encoding(self):
        """Test IMU data command encoding"""
        # Test case: Controller 74, All IMU data
        can_id, data = self.encoder.encode_get_imu_data(74, 0xFFFF)
        
        self.assertEqual(can_id, 0x0000804A)  # Controller 74, custom packet type
        self.assertEqual(data, struct.pack('>BH', 65, 0xFFFF))  # Command 65, mask 0xFFFF
    
    def test_input_validation(self):
        """Test input validation"""
        # Test duty cycle limits
        with self.assertRaises(ValueError):
            self.encoder.encode_set_duty_cycle(74, 1.5)  # Too high
        
        with self.assertRaises(ValueError):
            self.encoder.encode_set_duty_cycle(74, -1.5)  # Too low
        
        # Test current limits
        with self.assertRaises(ValueError):
            self.encoder.encode_set_current(74, 150.0)  # Too high
        
        # Test brake current limits
        with self.assertRaises(ValueError):
            self.encoder.encode_set_current_brake(74, -1.0)  # Negative
        
        # Test controller ID limits
        with self.assertRaises(ValueError):
            self.encoder.encode_set_duty_cycle(300, 0.5)  # Too high
    
    def test_response_validation(self):
        """Test response validation"""
        # Test matching controller ID
        self.assertTrue(self.encoder.validate_command_response(0x0000004A, b'', 74))
        
        # Test non-matching controller ID
        self.assertFalse(self.encoder.validate_command_response(0x0000004A, b'', 75))


class TestDataStructures(unittest.TestCase):
    """Test data structures"""
    
    def test_status_structures(self):
        """Test status data structures"""
        # Test Status 1
        status1 = VESCStatus1(rpm=1000, current=5.5, duty_cycle=0.25)
        self.assertEqual(status1.rpm, 1000)
        self.assertEqual(status1.current, 5.5)
        self.assertEqual(status1.duty_cycle, 0.25)
        
        # Test Status 2
        status2 = VESCStatus2(amp_hours=1.23, amp_hours_charged=0.45)
        self.assertEqual(status2.amp_hours, 1.23)
        self.assertEqual(status2.amp_hours_charged, 0.45)
        
        # Test Status 3
        status3 = VESCStatus3(watt_hours=2.34, watt_hours_charged=0.56)
        self.assertEqual(status3.watt_hours, 2.34)
        self.assertEqual(status3.watt_hours_charged, 0.56)
        
        # Test Status 4
        status4 = VESCStatus4(temp_fet=35.6, temp_motor=42.1, current_in=3.2, pid_pos_now=1.5)
        self.assertEqual(status4.temp_fet, 35.6)
        self.assertEqual(status4.temp_motor, 42.1)
        self.assertEqual(status4.current_in, 3.2)
        self.assertEqual(status4.pid_pos_now, 1.5)
        
        # Test Status 5
        status5 = VESCStatus5(tacho_value=123456, v_in=24.5)
        self.assertEqual(status5.tacho_value, 123456)
        self.assertEqual(status5.v_in, 24.5)
        
        # Test Status 6
        status6 = VESCStatus6(adc_1=1.234, adc_2=2.345, adc_3=3.456, ppm=0.789)
        self.assertEqual(status6.adc_1, 1.234)
        self.assertEqual(status6.adc_2, 2.345)
        self.assertEqual(status6.adc_3, 3.456)
        self.assertEqual(status6.ppm, 0.789)


def run_tests():
    """Run all unit tests"""
    print("Running VESC CAN System Unit Tests")
    print("=" * 40)
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTest(unittest.makeSuite(TestVESCProtocolParser))
    suite.addTest(unittest.makeSuite(TestVESCCommandEncoder))
    suite.addTest(unittest.makeSuite(TestDataStructures))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\nTest Summary:")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.failures:
        print("\nFailures:")
        for test, trace in result.failures:
            print(f"  {test}: {trace}")
    
    if result.errors:
        print("\nErrors:")
        for test, trace in result.errors:
            print(f"  {test}: {trace}")
    
    return len(result.failures) == 0 and len(result.errors) == 0


if __name__ == "__main__":
    if run_tests():
        print("\n🎉 All unit tests PASSED!")
    else:
        print("\n❌ Some unit tests FAILED!")
        exit(1)