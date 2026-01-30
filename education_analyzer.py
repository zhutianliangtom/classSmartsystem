#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
因材施教分析模块
"""

import json
from deepseek_api import DeepseekAPI

class EducationAnalyzer:
    def __init__(self, api_key):
        """初始化教育分析模块"""
        self.api = DeepseekAPI(api_key)
    
    def analyze_student(self, student_data, callback=None):
        """分析单个学生"""
        # 解析学生数据中的JSON字段
        if isinstance(student_data.get('grades'), str):
            try:
                student_data['grades'] = json.loads(student_data['grades'])
            except:
                student_data['grades'] = {}
        
        if isinstance(student_data.get('interests'), str):
            try:
                student_data['interests'] = json.loads(student_data['interests'])
            except:
                student_data['interests'] = []
        
        # 获取分析消息
        messages = self.api.analyze_student(student_data)
        # 执行流式分析
        return self.api.stream_completion(messages, callback)
    
    def generate_learning_plan(self, student_data, subject=None):
        """生成学习计划"""
        prompt = f"""
        你是一位专业的教育规划师，根据以下学生信息，为{subject if subject else '所有科目'}生成详细的学习计划：
        
        学生信息：
        - 姓名：{student_data.get('name', '未知')}
        - 年龄：{student_data.get('age', '未知')}
        - 班级：{student_data.get('class', '未知')}
        - 学习成绩：{student_data.get('grades', '{}')}
        - 兴趣爱好：{student_data.get('interests', '[]')}
        - 学习风格：{student_data.get('learning_style', '未知')}
        
        学习计划要求：
        1. 制定每周学习时间表
        2. 推荐适合的学习资源
        3. 设计针对性的练习和活动
        4. 设定合理的学习目标
        5. 提供学习方法和技巧指导
        
        请生成详细、实用、个性化的学习计划，帮助学生提高学习效果。
        """
        
        messages = [
            {"role": "system", "content": "你是一位专业的教育规划师，擅长制定个性化的学习计划。"},
            {"role": "user", "content": prompt}
        ]
        
        return self.api.stream_completion(messages)
    
    def analyze_class(self, class_students):
        """分析班级整体情况"""
        # 统计班级基本信息
        total_students = len(class_students)
        male_count = sum(1 for s in class_students if s.get('gender') == '男')
        female_count = total_students - male_count
        
        # 分析成绩分布
        grades_analysis = self._analyze_grades(class_students)
        
        # 分析学习风格分布
        learning_styles = self._analyze_learning_styles(class_students)
        
        # 分析兴趣分布
        interests = self._analyze_interests(class_students)
        
        # 生成班级分析报告
        prompt = f"""
        你是一位专业的教育分析师，根据以下班级分析数据，生成详细的班级整体分析报告：
        
        班级基本信息：
        - 总人数：{total_students}
        - 男生：{male_count}
        - 女生：{female_count}
        
        成绩分析：
        {grades_analysis}
        
        学习风格分布：
        {learning_styles}
        
        兴趣爱好分布：
        {interests}
        
        请从以下方面生成分析报告：
        1. 班级整体特点和优势
        2. 班级存在的问题和挑战
        3. 针对班级的教学建议
        4. 如何平衡不同学生的学习需求
        5. 班级活动和团队建设建议
        
        请提供专业、全面、实用的分析报告。
        """
        
        messages = [
            {"role": "system", "content": "你是一位专业的教育分析师，擅长分析班级整体情况并提供教学建议。"},
            {"role": "user", "content": prompt}
        ]
        
        return self.api.stream_completion(messages)
    
    def _analyze_grades(self, students):
        """分析成绩分布"""
        # 简单的成绩分析实现
        return "成绩数据分析结果"
    
    def _analyze_learning_styles(self, students):
        """分析学习风格分布"""
        styles = {}
        for student in students:
            style = student.get('learning_style', '未知')
            styles[style] = styles.get(style, 0) + 1
        return str(styles)
    
    def _analyze_interests(self, students):
        """分析兴趣分布"""
        interests = {}
        for student in students:
            student_interests = student.get('interests', '[]')
            if isinstance(student_interests, str):
                try:
                    student_interests = json.loads(student_interests)
                except:
                    student_interests = []
            
            for interest in student_interests:
                interests[interest] = interests.get(interest, 0) + 1
        return str(interests)
    
    def generate_thinking_process(self, question, callback=None):
        """生成思考过程"""
        return self.api.generate_thinking_process(question, callback)
