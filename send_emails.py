import json
import os
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

# 1. 配置 Brevo (自动从 GitHub Secret 获取 API Key)
configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = os.getenv('BREVO_API_KEY')
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

# 2. 读取用户数据库文件
with open('996yyds.json', 'r', encoding='utf-8') as f:
    users_data = json.load(f).get('data', [])

# 3. 读取发送进度 (确保每天发 100 封不重复)
PROGRESS_FILE = 'progress.txt'
start_index = 0
if os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, 'r') as f:
        try:
            content = f.read().strip()
            start_index = int(content) if content else 0
        except:
            start_index = 0

# 4. 筛选本次要发送的 100 个用户
batch_size = 100
end_index = start_index + batch_size
current_batch = users_data[start_index:end_index]

if not current_batch:
    print("所有用户已发送完毕！")
    exit()

# --- 花海定制内容 (hc@alhpool.com / huahai.wang) ---
SENDER_NAME = "花海运营中心"
SENDER_EMAIL = "hc@alhpool.com"  
SUBJECT = "【花海】全新 AnyTLS 跨境协议上线，诚邀开启全球研学体验"

HTML_CONTENT = """
<html>
<body style="font-family: 'Microsoft YaHei', sans-serif; line-height: 1.6; color: #333;">
    <div style="max-width: 600px; margin: 0 auto; border: 1px solid #f0f0f0; padding: 25px; border-radius: 12px; box-shadow: 0 4px 8px rgba(0,0,0,0.05);">
        <div style="text-align: center; margin-bottom: 20px;">
            <h2 style="color: #4a90e2; margin-top: 0;">🌸 花海 · 全球分布式加速</h2>
        </div>
        
        <p>尊敬的用户：</p>
        <p>为了应对日益复杂的网络环境，提供更极致的<b>跨境办公</b>与<b>全球资源访问</b>速度，“花海”技术团队现已完成架构重组，推出全新的 <b>AnyTLS 高性能加密协议</b>。</p>
        
        <div style="background: #fffbe6; border-left: 4px solid #ffe58f; padding: 15px; margin: 20px 0;">
            <p style="margin: 0; font-size: 14px; color: #856404;">
                <b>重要提示：</b> 本次为系统级升级，采用了全新底层协议。为保障链路纯净，原系统老数据不进行迁移。请老用户点击下方入口<b>重新注册</b>账号，即可立即开启全新体验。
            </p>
        </div>

        <div style="background: #eef7ff; padding: 15px; text-align: center; border-radius: 8px; margin: 20px 0;">
            <p style="font-size: 16px; margin-bottom: 10px;">点击下方链接，即刻注册加入：</p>
            <a href="https://huahai.wang" style="display: inline-block; background: #1890ff; color: #fff; padding: 12px 35px; text-decoration: none; border-radius: 5px; font-weight: bold; font-size: 18px;">立即访问 huahai.wang</a>
        </div>

        <p><b>AnyTLS 协议优势：</b></p>
        <ul style="color: #555; font-size: 14px;">
            <li><b>卓越兼容：</b> 深度模拟标准 TLS 流量，大幅提升复杂网络环境下的稳定性。</li>
            <li><b>无感加速：</b> 为 Google、Zoom、GitHub 等主流跨境平台提供专线级优化。</li>
            <li><b>多端覆盖：</b> 完美支持 Windows, macOS, Android 及 iOS 等全平台客户端。</li>
        </ul>

        <hr style="border: 0; border-top: 1px solid #eee; margin: 25px 0;">
        <p style="font-size: 12px; color: #999; text-align: center;">
            请将此域名 <b>huahai.wang</b> 妥善保存。若点击链接无效，请将其复制到浏览器地址栏手动访问。<br>
            <i>本邮件由系统发出，仅限受邀用户使用。</i>
        </p>
    </div>
</body>
</html>
"""
# 5. 执行发送循环
success_count = 0
for user in current_batch:
    email = user.get('email', '').strip()
    if "@" not in email or "admin" in email or "null" in email.lower():
        continue
    
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=[{"email": email}],
        sender={"name": SENDER_NAME, "email": SENDER_EMAIL},
        subject=SUBJECT,
        html_content=HTML_CONTENT
    )

    try:
        api_instance.send_transac_email(send_smtp_email)
        print(f"✅ 发送成功: {email}")
        success_count += 1
        time.sleep(2) # 延时2秒
    except ApiException as e:
        print(f"❌ 发送失败 {email}: {e}")

# 6. 更新进度
with open(PROGRESS_FILE, 'w') as f:
    f.write(str(end_index))

print(f"--- 任务完成: 成功 {success_count} 封，下个起点 {end_index} ---")
