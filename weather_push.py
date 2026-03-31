#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
重庆天气预报推送脚本
支持 PushPlus、企业微信机器人、Server酱 多种推送方式
"""

import requests
import os
import sys
import json
from datetime import datetime, timedelta

# 修复Windows控制台编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# PushPlus Token（推荐 - 直接推送到个人微信）
PUSHPLUS_TOKEN = os.environ.get('PUSHPLUS_TOKEN', '')

# 企业微信机器人 Webhook（备用方案）
QYWX_WEBHOOK = os.environ.get('QYWX_WEBHOOK', '')

# Server酱 SendKey（备用方案）
SERVERCHAN_SENDKEY = os.environ.get('SERVERCHAN_SENDKEY', '')

# 天气图标映射
WEATHER_ICONS = {
    '晴': '☀️',
    '晴朗': '☀️',
    '多云': '⛅',
    '阴': '☁️',
    '阴天': '☁️',
    '小雨': '🌧️',
    '中雨': '🌧️',
    '大雨': '🌧️',
    '暴雨': '⛈️',
    '雷阵雨': '⛈️',
    '小雪': '🌨️',
    '中雪': '🌨️',
    '大雪': '🌨️',
    '雨夹雪': '🌨️',
    '雾': '🌫️',
    '霾': '🌫️',
    '风': '💨',
}

def get_weather_icon(desc):
    """根据天气描述获取图标"""
    for key, icon in WEATHER_ICONS.items():
        if key in desc:
            return icon
    return '🌤️'

def get_clothing_advice(temp, desc, humidity, wind):
    """根据天气情况给出穿衣建议"""
    advice = []
    
    # 温度建议
    temp_int = int(temp)
    if temp_int >= 30:
        advice.append('天气炎热，建议穿短袖、短裤等清凉透气衣物')
    elif temp_int >= 25:
        advice.append('天气较热，适合穿短袖或薄长袖')
    elif temp_int >= 20:
        advice.append('温度适宜，建议穿长袖衬衫或薄外套')
    elif temp_int >= 15:
        advice.append('天气微凉，建议穿外套或卫衣')
    elif temp_int >= 10:
        advice.append('天气较冷，建议穿毛衣或厚外套')
    elif temp_int >= 5:
        advice.append('天气寒冷，建议穿棉衣或羽绒服')
    else:
        advice.append('天气严寒，务必穿羽绒服、戴围巾手套')
    
    # 特殊天气建议
    if '雨' in desc:
        advice.append('有降雨，记得带伞')
    if '雪' in desc:
        advice.append('有降雪，注意防滑保暖')
    if int(wind) > 20:
        advice.append('风力较大，注意防风')
    if int(humidity) > 80:
        advice.append('湿度较高，体感可能更闷热')
    if int(humidity) < 30:
        advice.append('空气干燥，注意补水保湿')
    
    return advice

def get_uv_advice(uv_index):
    """紫外线建议"""
    try:
        uv = int(uv_index)
        if uv <= 2:
            return '紫外线较弱，无需特别防护'
        elif uv <= 5:
            return '紫外线中等，建议涂防晒霜'
        elif uv <= 7:
            return '紫外线较强，外出需涂防晒霜、戴帽子'
        elif uv <= 10:
            return '紫外线很强，避免长时间户外活动'
        else:
            return '紫外线极强，务必做好防晒措施'
    except:
        return '紫外线中等，建议涂防晒霜'

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
        feels_like = current['FeelsLikeC']
        current_desc = current['lang_zh'][0]['value'] if 'lang_zh' in current else current['weatherDesc'][0]['value']
        humidity = current['humidity']
        wind_speed = current['windspeedKmph']
        wind_dir = current['winddir16Point']
        visibility = current['visibility']
        uv_index = current.get('uvIndex', '3')
        icon = get_weather_icon(current_desc)
        
        # 未来3天预报
        forecast_lines = []
        weekdays = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        
        for i in range(3):
            day = data['weather'][i]
            date_str = day['date']
            max_temp = day['maxtempC']
            min_temp = day['mintempC']
            
            # 计算星期几
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
                weekday = weekdays[date_obj.weekday()]
                if i == 0:
                    weekday = '今天'
                elif i == 1:
                    weekday = '明天'
            except:
                weekday = ''
            
            # 获取天气描述
            try:
                desc = day['hourly'][4]['lang_zh'][0]['value']
            except:
                desc = day['hourly'][4]['weatherDesc'][0]['value']
            
            day_icon = get_weather_icon(desc)
            forecast_lines.append(f"**{weekday} {date_str[5:]}**")
            forecast_lines.append(f"{day_icon} {desc} | {min_temp}°C ~ {max_temp}°C")
            forecast_lines.append("")
        
        # 获取穿衣建议
        clothing_tips = get_clothing_advice(current_temp, current_desc, humidity, wind_speed)
        uv_tip = get_uv_advice(uv_index)
        
        # 构建详细消息
        today = datetime.now().strftime('%Y年%m月%d日')
        weekday = weekdays[datetime.now().weekday()]
        
        title = f"{icon} 重庆天气预报 - {weekday}"
        
        content = f"""## {icon} {today} {weekday}

### 当前天气

{icon} **{current_desc}**

🌡️ **温度**: {current_temp}°C (体感 {feels_like}°C)
💧 **湿度**: {humidity}%
💨 **风速**: {wind_speed} km/h {wind_dir}
👁️ **能见度**: {visibility} km
☀️ **紫外线**: {uv_tip.split('，')[0]}

---

### 未来三天预报

{chr(10).join(forecast_lines[:-1])}

---

### 穿衣建议

"""
        
        # 添加穿衣建议
        for i, tip in enumerate(clothing_tips, 1):
            content += f"{i}. {tip}\n"
        
        content += f"\n**{uv_tip}**\n\n"
        content += "---\n\n*💡 数据来源: wttr.in | 祝您今天愉快！*"
        
        return title, content
        
    except Exception as e:
        # 如果JSON格式失败，尝试简单的文本格式
        try:
            url = "https://wttr.in/Chongqing?lang=zh&format=3"
            headers = {'User-Agent': 'curl/7.64.1'}
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            weather_text = response.text.strip()
            
            title = "🌤️ 重庆天气预报"
            content = f"""## {datetime.now().strftime('%Y年%m月%d日')}

### 当前天气

{weather_text}

---
*数据来源: wttr.in*"""
            return title, content
        except Exception as e2:
            return "天气预报获取失败", f"错误信息：{str(e)}\n备用方案也失败：{str(e2)}"

def send_to_pushplus(title, content):
    """通过 PushPlus 推送到个人微信（推荐）"""
    if not PUSHPLUS_TOKEN:
        print("错误：未配置 PUSHPLUS_TOKEN 环境变量")
        return False
    
    url = "http://www.pushplus.plus/send"
    
    # PushPlus 使用 Markdown 格式
    data = {
        "token": PUSHPLUS_TOKEN,
        "title": title,
        "content": content,
        "template": "markdown"
    }
    
    try:
        response = requests.post(
            url,
            data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        result = response.json()
        
        if result.get('code') == 200:
            print("PushPlus 推送成功")
            return True
        else:
            print(f"PushPlus 推送失败：{result.get('msg')}")
            return False
    except Exception as e:
        print(f"PushPlus 推送异常：{str(e)}")
        return False

def send_to_qywx(title, content):
    """通过企业微信机器人推送消息"""
    if not QYWX_WEBHOOK:
        print("错误：未配置 QYWX_WEBHOOK 环境变量")
        return False
    
    # 企业微信机器人使用 Markdown 格式
    data = {
        "msgtype": "markdown",
        "markdown": {
            "content": f"# {title}\n\n{content}"
        }
    }
    
    try:
        response = requests.post(
            QYWX_WEBHOOK,
            data=json.dumps(data, ensure_ascii=False).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        result = response.json()
        
        if result.get('errcode') == 0:
            print("企业微信推送成功")
            return True
        else:
            print(f"企业微信推送失败：{result.get('errmsg')}")
            return False
    except Exception as e:
        print(f"企业微信推送异常：{str(e)}")
        return False

def send_to_wechat(title, content):
    """通过Server酱推送到微信（备用方案）"""
    if not SERVERCHAN_SENDKEY:
        print("错误：未配置 SERVERCHAN_SENDKEY 环境变量")
        return False
    
    url = f"https://sctapi.ftqq.com/{SERVERCHAN_SENDKEY}.send"
    
    # 使用Markdown格式，确保正确显示
    data = {
        "title": title,
        "desp": content,
        "short": "重庆天气预报已送达"
    }
    
    try:
        # 直接发送，不额外编码
        response = requests.post(url, data=data, timeout=10)
        result = response.json()
        
        if result.get('code') == 0:
            print("推送成功")
            return True
        else:
            print(f"推送失败：{result.get('message')}")
            return False
    except Exception as e:
        print(f"推送异常：{str(e)}")
        return False

def main():
    """主函数"""
    print("开始获取重庆天气预报...")
    title, content = get_chongqing_weather()
    
    print("开始推送消息...")
    
    # 优先使用 PushPlus（直接推送到个人微信）
    if PUSHPLUS_TOKEN:
        print("使用 PushPlus 推送到个人微信...")
        success = send_to_pushplus(title, content)
        if success:
            print("任务完成")
            return
    
    # 备用方案1：企业微信
    if QYWX_WEBHOOK:
        print("使用企业微信机器人推送...")
        success = send_to_qywx(title, content)
        if success:
            print("任务完成")
            return
    
    # 备用方案2：Server酱
    if SERVERCHAN_SENDKEY:
        print("使用Server酱推送...")
        success = send_to_wechat(title, content)
        if success:
            print("任务完成")
            return
    
    print("错误：未配置任何推送方式")
    print("请配置以下环境变量之一：")
    print("  - PUSHPLUS_TOKEN（推荐，直接推送到个人微信）")
    print("  - QYWX_WEBHOOK（企业微信机器人）")
    print("  - SERVERCHAN_SENDKEY（Server酱）")

if __name__ == "__main__":
    main()
