#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
学生信息管理模块
"""

import pandas as pd
import os
import json

class StudentManager:
    def __init__(self, data_file='students_data.csv'):
        """初始化学生管理模块"""
        self.data_file = data_file
        self.students = self.load_students()
    
    def load_students(self):
        """加载学生数据"""
        if os.path.exists(self.data_file):
            return pd.read_csv(self.data_file)
        else:
            # 创建空的学生数据表
            df = pd.DataFrame({
                'id': [],
                'name': [],
                'gender': [],
                'age': [],
                'class': [],
                'grades': [],
                'interests': [],
                'learning_style': []
            })
            df.to_csv(self.data_file, index=False)
            return df
    
    def save_students(self):
        """保存学生数据"""
        self.students.to_csv(self.data_file, index=False)
    
    def add_student(self, student_data):
        """添加学生"""
        # 生成唯一ID
        if len(self.students) == 0:
            new_id = 1
        else:
            new_id = self.students['id'].max() + 1
        
        # 创建新学生记录
        new_student = {
            'id': new_id,
            'name': student_data.get('name', ''),
            'gender': student_data.get('gender', ''),
            'age': student_data.get('age', 0),
            'class': student_data.get('class', ''),
            'grades': student_data.get('grades', '{}'),
            'interests': student_data.get('interests', '[]'),
            'learning_style': student_data.get('learning_style', '')
        }
        
        # 添加到数据表
        self.students = pd.concat([self.students, pd.DataFrame([new_student])], ignore_index=True)
        self.save_students()
        return new_id
    
    def update_student(self, student_id, student_data):
        """更新学生信息"""
        if student_id in self.students['id'].values:
            index = self.students[self.students['id'] == student_id].index[0]
            for key, value in student_data.items():
                if key in self.students.columns:
                    self.students.at[index, key] = value
            self.save_students()
            return True
        return False
    
    def delete_student(self, student_id):
        """删除学生"""
        if student_id in self.students['id'].values:
            self.students = self.students[self.students['id'] != student_id]
            self.save_students()
            return True
        return False
    
    def get_student(self, student_id):
        """获取单个学生信息"""
        if student_id in self.students['id'].values:
            return self.students[self.students['id'] == student_id].iloc[0].to_dict()
        return None
    
    def get_all_students(self):
        """获取所有学生信息"""
        return self.students
    
    def get_students_by_class(self, class_name):
        """按班级获取学生"""
        return self.students[self.students['class'] == class_name]
    
    def update_grades(self, student_id, subject, grade):
        """更新学生成绩"""
        if student_id in self.students['id'].values:
            index = self.students[self.students['id'] == student_id].index[0]
            grades_str = self.students.at[index, 'grades']
            try:
                grades = json.loads(grades_str)
            except:
                grades = {}
            
            grades[subject] = grade
            self.students.at[index, 'grades'] = json.dumps(grades)
            self.save_students()
            return True
        return False
    
    def update_interests(self, student_id, interests):
        """更新学生兴趣"""
        if student_id in self.students['id'].values:
            index = self.students[self.students['id'] == student_id].index[0]
            self.students.at[index, 'interests'] = json.dumps(interests)
            self.save_students()
            return True
        return False
