#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重庆天气预报推送脚本
使用Server酱推送到微信
"""

import requests
import os
import sys
from datetime import datetime

# 修复Windows控制台编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Server酱 SendKey（需要配置）
SERVERCHAN_SENDKEY = os.environ.get('SERVERCHAN_SENDKEY', '')

def get_chongqing_weather():
    """获取重庆天气预报"""
    try:
        # 尝试获取详细天气预报（JSON格式）
        url = "https://wttr.in/Chongqing?lang=zh&format=j1"
        headers = {'User-Agent': 'curl/7.64.1'}
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            raise Exception(f"API返回错误：{response.status_code}")
            
        data = response.json()
        
        # 当前天气
        current = data['current_condition'][0]
        current_temp = current['temp_C']
        current_desc = current['lang_zh'][0]['value'] if 'lang_zh' in current else current['weatherDesc'][0]['value']
        humidity = current['humidity']
        wind = current['windspeedKmph']
        
        # 未来3天预报
        forecast = []
        for i in range(1, 4):
            day = data['weather'][i]
            date = day['date']
            max_temp = day['maxtempC']
            min_temp = day['mintempC']
            # 尝试获取中文描述，如果没有则用英文
            try:
                desc = day['hourly'][4]['lang_zh'][0]['value']
            except:
                desc = day['hourly'][4]['weatherDesc'][0]['value']
            forecast.append(f"{date}: {desc} {min_temp}-{max_temp}°C")
        
        # 构建消息
        title = "【重庆天气预报】"
        content = f"""
📅 {datetime.now().strftime('%Y年%m月%d日')}

🌡️ 当前天气：
{current_desc} {current_temp}°C
湿度：{humidity}%
风速：{wind} km/h

📅 未来三天：
{chr(10).join(forecast)}

💡 温馨提示：
记得根据天气增减衣物哦！
"""
        return title, content
        
    except Exception as e:
        # 如果JSON格式失败，尝试简单的文本格式
        try:
            url = "https://wttr.in/Chongqing?lang=zh&format=3"
            headers = {'User-Agent': 'curl/7.64.1'}
            response = requests.get(url, headers=headers, timeout=10)
            weather_text = response.text.strip()
            
            title = "【重庆天气预报】"
            content = f"""
📅 {datetime.now().strftime('%Y年%m月%d日')}

🌡️ 当前天气：
{weather_text}

💡 温馨提示：
详细天气数据获取失败，仅显示简要信息
"""
            return title, content
        except Exception as e2:
            return "天气预报获取失败", f"错误信息：{str(e)}\n备用方案也失败：{str(e2)}"

def send_to_wechat(title, content):
    """通过Server酱推送到微信"""
    if not SERVERCHAN_SENDKEY:
        print("错误：未配置 SERVERCHAN_SENDKEY 环境变量")
        return False
    
    url = f"https://sctapi.ftqq.com/{SERVERCHAN_SENDKEY}.send"
    data = {
        "title": title,
        "desp": content
    }
    
    try:
        response = requests.post(url, data=data, timeout=10)
        result = response.json()
        
        if result.get('code') == 0:
            print("✅ 推送成功")
            return True
        else:
            print(f"❌ 推送失败：{result.get('message')}")
            return False
    except Exception as e:
        print(f"❌ 推送异常：{str(e)}")
        return False

def main():
    """主函数"""
    print("开始获取重庆天气预报...")
    title, content = get_chongqing_weather()
    
    print("开始推送到微信...")
    success = send_to_wechat(title, content)
    
    if success:
        print("任务完成")
    else:
        print("任务失败")

if __name__ == "__main__":
    main()
