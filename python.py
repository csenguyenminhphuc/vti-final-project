import requests
import subprocess
import sys
import time
from dotenv import load_dotenv
import os

load_dotenv() 
# Cấu hình của bạn
API_TOKEN = os.getenv("API_TOKEN")
ZONE_ID = os.getenv("ZONE_ID")
RECORD_ID = os.getenv("RECORD_ID")
SUBDOMAIN = os.getenv("SUBDOMAIN")

# IPs của 2 server
PRIMARY_IP = os.getenv("PRIMARY_IP")
BACKUP_IP = os.getenv("BACKUP_IP")

# Headers cho API
headers = {
    'Authorization': f'Bearer {API_TOKEN}',
    'Content-Type': 'application/json'
}

def check_server_health(ip, timeout=5):
    """Check nếu server sống bằng ping"""
    try:
        result = subprocess.run(['ping', '-c', '1', '-W', str(timeout), ip], 
                                capture_output=True, text=True)
        return result.returncode == 0  # True nếu ping thành công
    except Exception:
        return False

def get_dns_record():
    """Lấy thông tin bản ghi hiện tại để verify"""
    url = f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{RECORD_ID}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()['result']
        if data['name'] == SUBDOMAIN and data['type'] == 'A':
            return data['content']  # Trả về IP hiện tại
    print("Lỗi lấy record:", response.text)
    sys.exit(1)

def update_dns_record(new_ip):
    """Cập nhật IP mới cho bản ghi A"""
    url = f'https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{RECORD_ID}'
    data = {
        'type': 'A',
        'name': SUBDOMAIN,
        'content': new_ip,
        'ttl': 1,  # TTL thấp để propagate nhanh
        'proxied': True  # False nếu không dùng proxy Cloudflare
    }
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"Đã cập nhật DNS: {SUBDOMAIN} -> {new_ip} tại {time.ctime()}")
        return True
    else:
        print("Lỗi cập nhật:", response.text)
        return False

# Main logic
if __name__ == "__main__":
    while True:
        try:
            current_ip = get_dns_record()
            print(f"[{time.ctime()}] IP hiện tại: {current_ip}")

            # Nếu đang dùng server phụ và server chính sống lại, quay lại server chính
            if current_ip == BACKUP_IP and check_server_health(PRIMARY_IP):
                print("Server chính sống lại! Chuyển về server chính...")
                if update_dns_record(PRIMARY_IP):
                    print("Chuyển về server chính thành công.")
                else:
                    print("Chuyển về server chính thất bại.")
            # Nếu đang dùng server chính và nó chết, chuyển sang server phụ
            elif current_ip == PRIMARY_IP and not check_server_health(PRIMARY_IP):
                print("Server chính chết! Chuyển sang server phụ...")
                if update_dns_record(BACKUP_IP):
                    print("Chuyển sang server phụ thành công.")
                else:
                    print("Chuyển sang server phụ thất bại.")
            else:
                print("Server hiện tại vẫn ổn. Không cần thay đổi.")

        except Exception as e:
            print(f"Lỗi không mong muốn: {e}")

        # Chờ 15 giây trước khi kiểm tra lại
        time.sleep(40)