import subprocess
import time


def run_cmd(cmd, timeout=30):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)


def check_internet(timeout=10):
    """Check internet connectivity"""
    success, _, _ = run_cmd(f"ping -c 2 -W {timeout} 8.8.8.8")
    return success


def get_hotspot_name():
    """Return the hotspot connection name"""
    return "lectec-ap"


def get_current_hostname():
    """Get current hostname (which matches the hotspot SSID)"""
    success, stdout, _ = run_cmd("hostname")
    if success and stdout.strip():
        return stdout.strip()
    return "ltpi-unknown"


def ensure_hotspot_active():
    """Ensure hotspot is active"""
    hotspot_name = get_hotspot_name()
    current_ssid = get_current_hostname()

    print(f"🔄 Ensuring hotspot is active (SSID: {current_ssid})...")

    # Check if hotspot is already active
    success, stdout, _ = run_cmd(f"sudo nmcli connection show --active | grep {hotspot_name}")
    if success:
        print(f"✅ Hotspot {current_ssid} already active")
        return True

    # Start hotspot
    success, _, stderr = run_cmd(f"sudo nmcli connection up {hotspot_name}")
    if success:
        print(f"✅ Hotspot {current_ssid} activated successfully")
        time.sleep(3)
        return True
    else:
        print(f"❌ Failed to start hotspot {current_ssid}: {stderr}")
        return False


def setup_wifi_connection(ssid, password):
    """Setup or update the main-wifi connection"""
    print(f"🔧 Setting up main-wifi connection for: {ssid}")

    # Check if main-wifi connection exists
    success, _, _ = run_cmd("sudo nmcli connection show main-wifi")
    if success:
        print("📝 Updating existing main-wifi connection...")
        # Delete existing connection to avoid conflicts
        run_cmd("sudo nmcli connection delete main-wifi", timeout=10)
        time.sleep(2)

    # Create new connection
    if password:
        cmd = f'sudo nmcli dev wifi connect "{ssid}" password "{password}" name main-wifi'
    else:
        cmd = f'sudo nmcli dev wifi connect "{ssid}" name main-wifi'

    return run_cmd(cmd, timeout=45)


def run_wifi_setup(ssid, password):
    """Run the WiFi setup flow with hotspot fallback."""
    WIFI_SSID = (ssid or "").strip()
    WIFI_PASSWORD = password or ""

    print("📶 WiFi Setup Starting...")
    print("=" * 60)

    # Show available networks
    print("🔍 Scanning for available WiFi networks...")
    success, stdout, _ = run_cmd("sudo nmcli dev wifi list", timeout=15)
    if success:
        print("\n📋 Available networks:")
        lines = stdout.strip().split('\n')[1:11]  # Show first 10
        for line in lines:
            if line.strip() and not line.startswith('--'):
                parts = line.split()
                if len(parts) >= 2:
                    ssid = parts[1] if parts[1] != '--' else 'Hidden Network'
                    signal = parts[7] if len(parts) > 7 else 'Unknown'
                    security = 'WPA' if 'WPA' in line else ('Open' if 'WEP' not in line else 'WEP')
                    print(f"  • {ssid:25} Signal: {signal:4} Security: {security}")
    else:
        print("⚠️  Could not scan networks - proceeding anyway...")

    print("\n" + "=" * 60)

    # Validate input
    if not WIFI_SSID:
        current_ssid = get_current_hostname()
        print("⚠️  Please enter a WiFi SSID above and click Connect")

        # Ensure hotspot is running
        ensure_hotspot_active()
        print(f"\n📡 Connect to hotspot: {current_ssid}")
        return

    current_ssid = get_current_hostname()
    hotspot_name = get_hotspot_name()

    print(f"🔗 Attempting to connect to WiFi: {WIFI_SSID}")

    # Step 1: Bring down hotspot
    print("📡 Bringing down hotspot...")
    print(f"\nYou will now lose connection to {current_ssid}. Connect to your main wifi and refresh the page in ~30 seconds.")
    print(f"If it does not connect, the {current_ssid} hotspot should reappear. Connect to it and ensure your SSID and Password are correct before trying again.")
    run_cmd(f"sudo nmcli connection down {hotspot_name}")

    # Step 2: Connect to WiFi with proper connection handling
    connection_successful = False
    wifi_error = None

    try:
        print(f"🔌 Connecting to {WIFI_SSID}...")

        success, stdout, stderr = setup_wifi_connection(WIFI_SSID, WIFI_PASSWORD)

        if success:
            print("✅ WiFi connection established!")

            # Wait and test internet
            print("⏳ Testing connection...")
            time.sleep(5)

            if check_internet():
                connection_successful = True
                print("✅ Internet access confirmed!")

                # Show IP
                success, stdout, _ = run_cmd("ip route get 8.8.8.8 | awk '{print $7; exit}'")
                if success and stdout.strip():
                    print(f"📍 WiFi IP: {stdout.strip()}")
            else:
                wifi_error = "Connected to WiFi but no internet access"
                print("⚠️  Connected to WiFi but no internet access")
        else:
            wifi_error = stderr
            print(f"❌ WiFi connection failed: {stderr}")

            if "Secrets were required" in stderr:
                print("💡 This usually means the password is incorrect")
            elif "No network with SSID" in stderr:
                print("💡 Network not found - check the SSID spelling")
            elif "already exists" in stderr:
                print("💡 Connection conflict - try running this again")

    except Exception as e:
        wifi_error = f"Unexpected error: {str(e)}"
        print(f"❌ Unexpected error: {str(e)}")

    # Step 3: Handle failure - restore hotspot
    if not connection_successful:
        print("\n🚨 WiFi connection failed - restoring hotspot")
        print("=" * 60)

        # Clean up any failed connection attempts
        run_cmd("sudo nmcli connection down main-wifi 2>/dev/null", timeout=10)

        # Restore hotspot
        hotspot_restored = ensure_hotspot_active()

        if hotspot_restored:
            print(f"\n📡 Hotspot {current_ssid} restored successfully")
            print("🔄 You can now:")
            print("   • Fix the credentials above and try again")
            print("   • Check that the network is available")
            print("   • Verify the password is correct")
            print(f"\n❌ Error: {wifi_error}")
        else:
            print(f"\n🚨 CRITICAL: Could not restore hotspot {current_ssid}!")
            print(f"   Try manually: sudo nmcli connection up {hotspot_name}")
    else:
        # Success!
        print("🎉 WiFi Setup Complete!")
