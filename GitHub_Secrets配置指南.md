# GitHub Secrets 配置指南

## 需要配置的 Secrets

进入 GitHub 仓库：https://github.com/jierfr/weather-push/settings/secrets/actions

### 1. 添加 QYWX_WEBHOOK（企业微信机器人）

- **Name**: `QYWX_WEBHOOK`
- **Value**: `https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=42aeeb6e-e6bc-4b7d-9494-af291814ca2c`

### 2. 保留 SERVERCHAN_SENDKEY（可选，作为备用）

- **Name**: `SERVERCHAN_SENDKEY`
- **Value**: `SCT332103TDAYKrzFoOdR1LUbNQlEwEkns`

## 配置步骤

1. 打开 https://github.com/jierfr/weather-push/settings/secrets/actions
2. 点击 "New repository secret"
3. 输入 Name 和 Value
4. 点击 "Add secret"
5. 重复步骤 2-4 添加另一个 secret

## 推送优先级

脚本会按以下顺序尝试推送：
1. **企业微信机器人**（如果配置了 QYWX_WEBHOOK）
2. **Server酱**（如果配置了 SERVERCHAN_SENDKEY，作为备用）

配置好企业微信后，建议删除 SERVERCHAN_SENDKEY，只保留企业微信推送。
