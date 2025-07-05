"""
VESC CAN Node ID Manager

This module handles automatic assignment of unique node IDs for Raspberry Pi devices
on the CAN network. It uses the MAC address as a base and provides conflict resolution.
"""

import uuid
import time
import json
import os
import hashlib
from typing import Set, Optional, Dict, Any
from pathlib import Path
from .datatypes import NODE_ID_MIN, NODE_ID_MAX, VESCCANCommands

class VESCNodeManager:
    """
    Manages unique node ID assignment for Raspberry Pi devices on VESC CAN networks
    
    This class ensures that each Raspberry Pi gets a unique node ID in the range
    64-127, handles conflict detection and resolution, and maintains a registry
    of active nodes on the network.
    """
    
    def __init__(self, config_dir: Optional[str] = None):
        """
        Initialize node manager
        
        Args:
            config_dir: Directory to store configuration files (default: ~/.vesc_can/)
        """
        if config_dir is None:
            config_dir = os.path.expanduser("~/.vesc_can/")
        
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_file = self.config_dir / "node_config.json"
        self.active_nodes_file = self.config_dir / "active_nodes.json"
        
        self._my_node_id: Optional[int] = None
        self._my_mac_address = self._get_mac_address()
        self._active_nodes: Set[int] = set()
        self._node_registry: Dict[int, Dict[str, Any]] = {}
        self._last_discovery_time = 0.0
        
        # Load existing configuration
        self._load_config()
        self._load_active_nodes()
    
    def _get_mac_address(self) -> str:
        """Get the MAC address of this device"""
        mac_int = uuid.getnode()
        mac_hex = f"{mac_int:012x}"
        return ":".join(mac_hex[i:i+2] for i in range(0, 12, 2))
    
    def _generate_node_id_from_mac(self) -> int:
        """Generate a node ID based on MAC address"""
        # Use SHA-256 hash of MAC address for better distribution
        mac_hash = hashlib.sha256(self._my_mac_address.encode()).digest()
        # Take first 4 bytes and map to our range
        hash_int = int.from_bytes(mac_hash[:4], 'big')
        return NODE_ID_MIN + (hash_int % (NODE_ID_MAX - NODE_ID_MIN + 1))
    
    def _load_config(self):
        """Load node configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                
                # Verify this config is for our MAC address
                if config.get('mac_address') == self._my_mac_address:
                    self._my_node_id = config.get('node_id')
                else:
                    # Config is for different device, regenerate
                    self._my_node_id = None
        except (json.JSONDecodeError, IOError):
            # Invalid or unreadable config file
            self._my_node_id = None
    
    def _save_config(self):
        """Save node configuration to file"""
        if self._my_node_id is None:
            return
        
        config = {
            'mac_address': self._my_mac_address,
            'node_id': self._my_node_id,
            'assigned_time': time.time(),
            'device_info': {
                'hostname': os.uname().nodename,
                'system': os.uname().sysname,
                'release': os.uname().release,
            }
        }
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except IOError:
            # Can't save config - not critical
            pass
    
    def _load_active_nodes(self):
        """Load active nodes registry from file"""
        try:
            if self.active_nodes_file.exists():
                with open(self.active_nodes_file, 'r') as f:
                    data = json.load(f)
                
                # Only load recent entries (last 5 minutes)
                current_time = time.time()
                cutoff_time = current_time - 300  # 5 minutes
                
                for node_id_str, node_info in data.items():
                    try:
                        node_id = int(node_id_str)
                        last_seen = node_info.get('last_seen', 0)
                        
                        if last_seen > cutoff_time:
                            self._active_nodes.add(node_id)
                            self._node_registry[node_id] = node_info
                    except (ValueError, TypeError):
                        continue
                        
        except (json.JSONDecodeError, IOError):
            # Invalid or unreadable file
            self._active_nodes.clear()
            self._node_registry.clear()
    
    def _save_active_nodes(self):
        """Save active nodes registry to file"""
        try:
            # Clean up old entries before saving
            current_time = time.time()
            cutoff_time = current_time - 300  # 5 minutes
            
            clean_registry = {}
            for node_id, node_info in self._node_registry.items():
                if node_info.get('last_seen', 0) > cutoff_time:
                    clean_registry[str(node_id)] = node_info
            
            with open(self.active_nodes_file, 'w') as f:
                json.dump(clean_registry, f, indent=2)
                
        except IOError:
            # Can't save registry - not critical
            pass
    
    def get_node_id(self) -> int:
        """
        Get the node ID for this device
        
        Returns:
            Node ID (64-127) for this device
        """
        if self._my_node_id is None:
            self._assign_node_id()
        
        return self._my_node_id
    
    def _assign_node_id(self):
        """Assign a node ID to this device"""
        # Start with MAC-based ID
        preferred_id = self._generate_node_id_from_mac()
        
        if preferred_id not in self._active_nodes:
            # Preferred ID is available
            self._my_node_id = preferred_id
        else:
            # Find next available ID
            for candidate_id in range(NODE_ID_MIN, NODE_ID_MAX + 1):
                if candidate_id not in self._active_nodes:
                    self._my_node_id = candidate_id
                    break
            
            if self._my_node_id is None:
                # All IDs taken - use preferred anyway and hope for the best
                self._my_node_id = preferred_id
        
        # Register ourselves
        self.register_node(self._my_node_id, {
            'mac_address': self._my_mac_address,
            'device_type': 'raspberry_pi',
            'hostname': os.uname().nodename,
            'is_self': True
        })
        
        # Save configuration
        self._save_config()
    
    def register_node(self, node_id: int, node_info: Dict[str, Any]):
        """
        Register a node as active on the network
        
        Args:
            node_id: Node ID that was seen
            node_info: Information about the node
        """
        current_time = time.time()
        
        self._active_nodes.add(node_id)
        
        # Update node registry
        existing_info = self._node_registry.get(node_id, {})
        existing_info.update(node_info)
        existing_info['last_seen'] = current_time
        existing_info['first_seen'] = existing_info.get('first_seen', current_time)
        
        self._node_registry[node_id] = existing_info
        
        # Save updated registry
        self._save_active_nodes()
    
    def handle_can_message(self, can_id: int, data: bytes) -> bool:
        """
        Process a CAN message for node discovery
        
        Args:
            can_id: CAN arbitration ID
            data: CAN frame data
            
        Returns:
            True if this was a ping that we should respond to
        """
        # Extract command and node ID from CAN ID
        command = (can_id >> 8) & 0xFF
        sender_node_id = can_id & 0xFF
        
        # Register any node we see activity from
        if sender_node_id != self.get_node_id():  # Don't register ourselves
            self.register_node(sender_node_id, {
                'device_type': 'vesc_or_other',
                'last_command': command
            })
        
        # Check if this is a ping directed at us
        if command == VESCCANCommands.PING:
            # If data is empty, it's a broadcast ping
            # If data contains node IDs, check if we're included
            if len(data) == 0:
                return True  # Broadcast ping - we should respond
            elif len(data) >= 1:
                # Check if our node ID is in the ping data
                target_nodes = list(data)
                return self.get_node_id() in target_nodes
        
        return False
    
    def detect_node_conflict(self) -> bool:
        """
        Detect if there's another device using our node ID
        
        Returns:
            True if a conflict is detected
        """
        my_id = self.get_node_id()
        
        if my_id in self._node_registry:
            node_info = self._node_registry[my_id]
            
            # Check if this entry is not ours
            if not node_info.get('is_self', False):
                # Another device is using our ID
                mac_address = node_info.get('mac_address')
                if mac_address and mac_address != self._my_mac_address:
                    return True
        
        return False
    
    def resolve_node_conflict(self):
        """Resolve node ID conflict by assigning a new ID"""
        old_id = self._my_node_id
        
        # Remove our current ID from active nodes
        if old_id in self._active_nodes:
            self._active_nodes.remove(old_id)
        
        # Remove from registry
        if old_id in self._node_registry:
            del self._node_registry[old_id]
        
        # Force reassignment
        self._my_node_id = None
        self._assign_node_id()
        
        print(f"Node ID conflict resolved: changed from {old_id} to {self._my_node_id}")
    
    def get_active_nodes(self) -> Dict[int, Dict[str, Any]]:
        """
        Get dictionary of all active nodes on the network
        
        Returns:
            Dictionary mapping node ID to node information
        """
        # Clean up old entries
        current_time = time.time()
        cutoff_time = current_time - 300  # 5 minutes
        
        active_registry = {}
        for node_id, node_info in self._node_registry.items():
            if node_info.get('last_seen', 0) > cutoff_time:
                active_registry[node_id] = node_info.copy()
        
        return active_registry
    
    def get_vesc_nodes(self) -> Dict[int, Dict[str, Any]]:
        """Get only the VESC nodes (exclude Raspberry Pi nodes)"""
        active_nodes = self.get_active_nodes()
        return {
            node_id: info for node_id, info in active_nodes.items()
            if info.get('device_type') != 'raspberry_pi'
        }
    
    def get_raspberry_pi_nodes(self) -> Dict[int, Dict[str, Any]]:
        """Get only the Raspberry Pi nodes"""
        active_nodes = self.get_active_nodes()
        return {
            node_id: info for node_id, info in active_nodes.items()
            if info.get('device_type') == 'raspberry_pi'
        }
    
    def perform_network_discovery(self, send_ping_callback):
        """
        Perform active network discovery by sending pings
        
        Args:
            send_ping_callback: Function to send ping CAN messages
        """
        current_time = time.time()
        
        # Only do discovery every 30 seconds
        if current_time - self._last_discovery_time < 30:
            return
        
        self._last_discovery_time = current_time
        
        # Send broadcast ping to discover all nodes
        try:
            send_ping_callback()
        except Exception:
            # Ignore ping send errors
            pass
    
    def cleanup_old_nodes(self):
        """Remove nodes that haven't been seen recently"""
        current_time = time.time()
        cutoff_time = current_time - 600  # 10 minutes
        
        nodes_to_remove = []
        for node_id, node_info in self._node_registry.items():
            if node_info.get('last_seen', 0) < cutoff_time:
                nodes_to_remove.append(node_id)
        
        for node_id in nodes_to_remove:
            if node_id in self._active_nodes:
                self._active_nodes.remove(node_id)
            if node_id in self._node_registry:
                del self._node_registry[node_id]
        
        if nodes_to_remove:
            self._save_active_nodes()
    
    def get_network_stats(self) -> Dict[str, Any]:
        """Get network statistics"""
        active_nodes = self.get_active_nodes()
        vesc_nodes = self.get_vesc_nodes()
        pi_nodes = self.get_raspberry_pi_nodes()
        
        return {
            'total_nodes': len(active_nodes),
            'vesc_nodes': len(vesc_nodes),
            'raspberry_pi_nodes': len(pi_nodes),
            'my_node_id': self.get_node_id(),
            'my_mac_address': self._my_mac_address,
            'available_ids': list(range(NODE_ID_MIN, NODE_ID_MAX + 1)),
            'used_ids': sorted(active_nodes.keys()),
            'free_ids': sorted(set(range(NODE_ID_MIN, NODE_ID_MAX + 1)) - set(active_nodes.keys()))
        }
    
    def force_node_id(self, node_id: int):
        """
        Force assignment of specific node ID (for testing/debugging)
        
        Args:
            node_id: Node ID to use (64-127)
        """
        if not NODE_ID_MIN <= node_id <= NODE_ID_MAX:
            raise ValueError(f"Node ID must be between {NODE_ID_MIN} and {NODE_ID_MAX}")
        
        old_id = self._my_node_id
        
        # Remove old ID from tracking
        if old_id is not None:
            if old_id in self._active_nodes:
                self._active_nodes.remove(old_id)
            if old_id in self._node_registry:
                del self._node_registry[old_id]
        
        # Set new ID
        self._my_node_id = node_id
        
        # Register new ID
        self.register_node(node_id, {
            'mac_address': self._my_mac_address,
            'device_type': 'raspberry_pi',
            'hostname': os.uname().nodename,
            'is_self': True
        })
        
        # Save configuration
        self._save_config()
        
        print(f"Node ID manually set to {node_id} (was {old_id})")

# Global instance for easy access
_node_manager_instance: Optional[VESCNodeManager] = None

def get_node_manager() -> VESCNodeManager:
    """Get the global node manager instance"""
    global _node_manager_instance
    if _node_manager_instance is None:
        _node_manager_instance = VESCNodeManager()
    return _node_manager_instance

def get_my_node_id() -> int:
    """Get the node ID for this device"""
    return get_node_manager().get_node_id()

def get_active_nodes() -> Dict[int, Dict[str, Any]]:
    """Get all active nodes on the network"""
    return get_node_manager().get_active_nodes()

def get_vesc_nodes() -> Dict[int, Dict[str, Any]]:
    """Get only the VESC nodes on the network"""
    return get_node_manager().get_vesc_nodes()

def get_network_stats() -> Dict[str, Any]:
    """Get network statistics"""
    return get_node_manager().get_network_stats()