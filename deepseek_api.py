#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deepseek API集成模块
"""

import requests
import json
import time

class DeepseekAPI:
    def __init__(self, api_key, model='Deepseek-Reasoner'):
        """初始化Deepseek API"""
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.deepseek.com/v1/chat/completions"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
    
    def chat_completion(self, messages, stream=False, max_tokens=1024, temperature=0.7):
        """调用Deepseek API进行对话补全"""
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "top_p": 0.95
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=self.headers,
                json=payload,
                stream=stream
            )
            
            if stream:
                return response
            else:
                return response.json()
        except Exception as e:
            print(f"API调用错误: {e}")
            return None
    
    def stream_completion(self, messages, callback=None, max_tokens=1024, temperature=0.7):
        """流式输出完成"""
        response = self.chat_completion(
            messages=messages,
            stream=True,
            max_tokens=max_tokens,
            temperature=temperature
        )
        
        if not response:
            return None
        
        full_response = ""
        for chunk in response.iter_lines():
            if chunk:
                chunk = chunk.decode('utf-8')
                if chunk.startswith('data: '):
                    chunk_data = chunk[6:]
                    if chunk_data == '[DONE]':
                        break
                    try:
                        data = json.loads(chunk_data)
                        if 'choices' in data and data['choices']:
                            delta = data['choices'][0].get('delta', {})
                            if 'content' in delta:
                                content = delta['content']
                                full_response += content
                                if callback:
                                    callback(content)
                                # 添加小延迟以模拟真实的思考过程
                                time.sleep(0.05)
                    except json.JSONDecodeError:
                        continue
        
        return full_response
    
    def analyze_student(self, student_data):
        """分析学生数据，提供因材施教建议"""
        # 构建分析提示
        prompt = f"""
        你是一位专业的教育顾问，根据以下学生信息，提供详细的因材施教分析和建议：
        
        学生信息：
        - 姓名：{student_data.get('name', '未知')}
        - 性别：{student_data.get('gender', '未知')}
        - 年龄：{student_data.get('age', '未知')}
        - 班级：{student_data.get('class', '未知')}
        - 学习成绩：{student_data.get('grades', '{}')}
        - 兴趣爱好：{student_data.get('interests', '[]')}
        - 学习风格：{student_data.get('learning_style', '未知')}
        
        请从以下几个方面提供分析：
        1. 学生的学习优势和劣势
        2. 适合的学习方法和策略
        3. 推荐的学习资源和活动
        4. 个性化的学习计划建议
        5. 教师和家长的配合建议
        
        请提供详细、专业、实用的分析，帮助教师更好地因材施教。
        """
        
        messages = [
            {"role": "system", "content": "你是一位专业的教育顾问，擅长分析学生特点并提供个性化的教育建议。"},
            {"role": "user", "content": prompt}
        ]
        
        return messages
    
    def generate_thinking_process(self, question, callback=None):
        """生成思考过程"""
        prompt = f"""
        请详细展示你思考以下问题的过程，逐步分析，最后给出结论：
        {question}
        
        要求：
        1. 展示完整的思考步骤
        2. 分析要深入细致
        3. 逻辑要清晰连贯
        4. 最后给出明确的结论
        """
        
        messages = [
            {"role": "system", "content": "你是一位善于思考和分析的专家，能够清晰展示自己的思考过程。"},
            {"role": "user", "content": prompt}
        ]
        
        return self.stream_completion(messages, callback)
