# 重庆天气预报微信推送 - 配置指南

## 功能说明

- ⏰ **定时推送**：每天早上7点自动推送重庆天气预报
- 🌡️ **天气内容**：当前天气 + 未来3天预报 + 温馨提示
- 📱 **推送方式**：通过Server酱推送到微信
- ☁️ **云端运行**：使用GitHub Actions，电脑关机也能收到

## 配置步骤

### 第1步：注册Server酱并获取SendKey

1. 访问 [Server酱官网](https://sct.ftqq.com/)
2. 使用微信扫码登录
3. 点击右上角头像 → 【SendKey】
4. 复制你的 SendKey（格式类似：`SCT123456xxxxxxxx`）

### 第2步：创建GitHub仓库

1. 访问 [GitHub](https://github.com/)
2. 创建新仓库：
   - 点击右上角 **+** → **New repository**
   - Repository name: `weather-push`
   - 选择 **Public** 或 **Private** 都可以
   - ✅ 勾选 **Add a README file**
   - 点击 **Create repository**

### 第3步：上传文件到GitHub

#### 方法A：使用Git命令行（推荐）

```bash
# 在本地仓库目录执行
cd c:\Users\Administrator\WorkBuddy\Claw
git init
git add weather_push.py .github/workflows/weather.yml
git commit -m "添加天气预报推送功能"
git branch -M main
git remote add origin https://github.com/你的用户名/weather-push.git
git push -u origin main
```

#### 方法B：使用GitHub网页上传

1. 在GitHub仓库页面点击 **uploading an existing file**
2. 拖拽以下文件：
   - `weather_push.py`
   - `.github/workflows/weather.yml`
3. 点击 **Commit changes**

### 第4步：配置GitHub Secrets

1. 进入你的GitHub仓库
2. 点击 **Settings** → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 填写：
   - **Name**: `SERVERCHAN_SENDKEY`
   - **Secret**: 你的Server酱 SendKey（如：`SCT123456xxxxxxxx`）
5. 点击 **Add secret**

### 第5步：测试推送

#### 手动触发测试

1. 进入GitHub仓库
2. 点击 **Actions** 标签
3. 选择 **重庆天气预报推送** workflow
4. 点击 **Run workflow** → **Run workflow**
5. 等待几秒钟，检查微信是否收到消息

#### 查看运行日志

- 点击具体的 workflow run
- 可以看到详细的执行日志

## 常见问题

### Q: 为什么还没收到推送？

**检查清单：**
1. ✅ Server酱SendKey配置正确
2. ✅ GitHub Secrets配置正确
3. ✅ 文件路径正确（`.github/workflows/weather.yml`）
4. ✅ GitHub Actions已启用（仓库Settings → Actions → General）

### Q: 如何修改推送时间？

编辑 `.github/workflows/weather.yml`：

```yaml
on:
  schedule:
    - cron: '0 23 * * *'  # UTC 23:00 = 北京时间 07:00
```

Cron表达式格式：`分 时 日 月 星期`

### Q: 免费额度够用吗？

- **Server酱免费版**：每天5条消息
- **GitHub Actions免费额度**：每月2000分钟
- 天气推送每天1条，完全够用 ✅

### Q: 如何查看推送历史？

1. 打开微信 → Server酱公众号
2. 可以查看所有推送历史

## 文件说明

```
weather-push/
├── weather_push.py           # 天气推送脚本
├── .github/
│   └── workflows/
│       └── weather.yml       # GitHub Actions工作流
└── README_天气推送.md        # 本说明文档
```

## 自定义修改

### 修改城市

编辑 `weather_push.py`：

```python
url = "https://wttr.in/你的城市?lang=zh&format=j1"
```

### 修改推送内容格式

编辑 `weather_push.py` 中的 `content` 变量。

## 技术支持

- **Server酱文档**: https://sct.ftqq.com/forward
- **GitHub Actions文档**: https://docs.github.com/cn/actions
- **wttr.in天气API**: https://github.com/chubin/wttr.in

---

配置完成后，每天早上7点你的微信就会自动收到天气预报啦！🎉
