# Git上传指南

## 方法1：网页上传（最简单）

### 步骤1：上传 weather_push.py
1. 打开GitHub仓库页面
2. 点击 **"uploading an existing file"**
3. 拖拽文件：`c:\Users\Administrator\WorkBuddy\Claw\weather_push.py`
4. 点击 **"Commit changes"**

### 步骤2：上传 README_天气推送.md
1. 再次点击 **"uploading an existing file"**
2. 拖拽文件：`c:\Users\Administrator\WorkBuddy\Claw\README_天气推送.md`
3. 点击 **"Commit changes"**

### 步骤3：上传 .github/workflows/weather.yml（特殊）
1. 点击 **"Create new file"**
2. 在文件名输入框输入：`.github/workflows/weather.yml`
3. GitHub会自动创建文件夹
4. 复制以下内容粘贴：

```yaml
name: 重庆天气预报推送

on:
  schedule:
    # 每天 UTC 23:00 运行（北京时间早上7点）
    - cron: '0 23 * * *'
  workflow_dispatch: # 支持手动触发

jobs:
  weather-push:
    runs-on: ubuntu-latest
    
    steps:
    - name: 检出代码
      uses: actions/checkout@v4
    
    - name: 设置Python环境
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
    
    - name: 安装依赖
      run: |
        python -m pip install --upgrade pip
        pip install requests
    
    - name: 运行天气预报推送
      env:
        SERVERCHAN_SENDKEY: ${{ secrets.SERVERCHAN_SENDKEY }}
      run: python weather_push.py
    
    - name: 推送完成
      run: echo "天气预报推送完成 ✅"
```

5. 点击 **"Commit new file"**

---

## 方法2：Git命令上传（如果安装了Git）

### 步骤1：打开PowerShell
```powershell
cd c:\Users\Administrator\WorkBuddy\Claw
```

### 步骤2：初始化Git仓库
```powershell
git init
git add weather_push.py .github/workflows/weather.yml README_天气推送.md
git commit -m "添加天气预报推送功能"
git branch -M main
```

### 步骤3：关联远程仓库
```powershell
# 替换成你的GitHub用户名
git remote add origin https://github.com/你的用户名/weather-push.git
git push -u origin main
```

如果需要登录，GitHub会弹出登录窗口。

---

## 方法3：GitHub Desktop（如果安装了）

1. 打开GitHub Desktop
2. File → Add Local Repository
3. 选择 `c:\Users\Administrator\WorkBuddy\Claw`
4. 点击 **"Create a repository"**
5. 点击 **"Publish repository"**

---

## 配置完成后别忘了：

### 添加Secrets
1. 进入GitHub仓库
2. **Settings** → **Secrets and variables** → **Actions**
3. 点击 **"New repository secret"**
4. 填写：
   - Name: `SERVERCHAN_SENDKEY`
   - Secret: `SCT332103TDAYKrzFoOdR1LUbNQlEwEkns`
5. 点击 **"Add secret"**

### 测试推送
1. 点击 **Actions** 标签
2. 选择 **"重庆天气预报推送"**
3. 点击 **"Run workflow"** → **"Run workflow"**
4. 等待几秒钟，检查微信是否收到消息

---

## 推荐顺序：

**新手推荐：方法1（网页上传）**
- 不需要安装任何工具
- 操作直观简单

**有Git经验：方法2（Git命令）**
- 更专业
- 方便后续更新

**有GitHub Desktop：方法3**
- 图形化操作
- 最方便

选择最适合你的方法即可！
