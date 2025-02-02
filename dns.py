import subprocess
import time

def set_dns(interface_name, dns1, dns2):
    try:
        print(f"Setting DNS to {dns1} for {interface_name}...")
        subprocess.run(['netsh', 'interface', 'ip', 'set', 'dns', f'name={interface_name}', 'source=static', 'addr=' + dns1], check=True)
        print(f"DNS set to {dns1} for {interface_name}.")

        print(f"Adding DNS {dns2} for {interface_name}...")
        subprocess.run(['netsh', 'interface', 'ip', 'add', 'dns', f'name={interface_name}', 'addr=' + dns2, 'index=2'], check=True)
        print(f"DNS set to {dns2} for {interface_name}.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to set DNS settings: {e}")

def reset_dns(interface_name):
    try:
        print(f"Resetting DNS to DHCP for {interface_name}...")
        subprocess.run(['netsh', 'interface', 'ip', 'set', 'dns', f'name={interface_name}', 'source=dhcp'], check=True)
        print(f"DNS reset to DHCP for {interface_name}.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to reset DNS settings: {e}")

def dns_thread(interface_name, dns1, dns2):
    set_dns(interface_name, dns1, dns2)
    time.sleep(300)
    reset_dns(interface_name)


dns_thread("Wi-Fi", "8.26.56.26", "8.20.247.20")
