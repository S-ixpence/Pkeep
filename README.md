<div align=center>
    <h1>PKeep</h1>
</div>
<div align=center>
  Pkeep - 简单方便的linux权限维持脚本<br/><br/>
  <img src="https://img.shields.io/badge/Built%20with-Python-Blue"/>
  <img src="https://img.shields.io/github/stars/S-ixpence/Pkeep"/>
</div>
<h2>运行环境：</h2>
使用python3运行<br/>
<h2>支持的功能：</h2>
  添加后门账户<br/>
  为账户添加sudo权限<br/>
  隐藏bash命令<br/>
  软链sshd后门<br/>
  crontab反向Shell<br/>
  写入公钥<br/>
  持久化反向Shell<br/>
<h2>工具截图</h2>
<img src="https://github.com/user-attachments/assets/61fbd248-1cba-4441-9b2b-b782b89a4a07"/>
<h2>2025.3.4更新（通过deepseek进行重构）</h2>
    <div class="section">
        <h2>主要优化点</h2>
        <ul class="features">
            <li><strong>面向对象重构：</strong>使用类来组织代码，提高可维护性。</li>
            <li><strong>增强错误处理：</strong>使用subprocess代替os.system，完善错误检查。</li>
            <li><strong>隐蔽性提升：</strong>
                <ul>
                    <li>使用更隐蔽的文件名（如<code>systemd-network.service</code>）。</li>
                    <li>文件时间戳伪装。</li>
                    <li>文件属性锁定（<code>chattr +i</code>）。</li>
                </ul>
            </li>
            <li><strong>输入验证：</strong>增加端口有效性检查。</li>
            <li><strong>安全性改进：</strong>
                <ul>
                    <li>使用openssl生成安全密码哈希。</li>
                    <li>更安全的sudo权限配置方式（<code>/etc/sudoers.d/</code>）。</li>
                </ul>
            </li>
            <li><strong>功能增强：</strong>
                <ul>
                    <li>支持自定义用户名/密码。</li>
                    <li>更可靠的定时任务添加方式。</li>
                    <li>完善的SSH密钥注入流程。</li>
                </ul>
            </li>
            <li><strong>用户体验改进：</strong>
                <ul>
                    <li>退出清理功能。</li>
                    <li>更友好的交互提示。</li>
                    <li>操作确认提示。</li>
                </ul>
            </li>
            <li><strong>兼容性改进：</strong>
                <ul>
                    <li>支持更多Linux发行版。</li>
                    <li>自动处理依赖项检查。</li>
                </ul>
            </li>
        </ul>
    </div>

    <div class="section">
        <h2>使用说明</h2>
        <ul class="notes">
            <li>需要root权限运行。</li>
            <li>推荐在受控环境中使用。</li>
            <li>各功能模块已做隐蔽性处理。</li>
            <li>关键文件做了防删除保护。</li>
        </ul>
    </div>

    <div class="section">
        <h2>注意事项</h2>
        <p class="warning">本程序仅限合法授权测试使用，请遵守当地法律法规。</p>
    </div>
