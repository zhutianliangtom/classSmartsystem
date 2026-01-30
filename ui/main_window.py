#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主窗口界面
"""

from PyQt5.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QTableWidget, QTableWidgetItem,
    QDialog, QFormLayout, QComboBox, QTextEdit, QSplitter,
    QMessageBox, QListWidget, QListWidgetItem, QGroupBox
)
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal
import sys
import os
import json
import pandas as pd

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from student_manager import StudentManager
from education_analyzer import EducationAnalyzer

class StreamOutputThread(QThread):
    """流式输出线程"""
    update_signal = pyqtSignal(str)
    
    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
    
    def run(self):
        def callback(content):
            self.update_signal.emit(content)
        
        self.kwargs['callback'] = callback
        self.func(*self.args, **self.kwargs)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.student_manager = StudentManager()
        # 注意：这里需要替换为实际的API key
        self.analyzer = EducationAnalyzer(api_key="YOUR_DEEPSEEK_API_KEY")
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("班级智能管理系统")
        self.setGeometry(100, 100, 1200, 800)
        
        # 设置字体
        font = QFont("Microsoft YaHei", 10)
        self.setFont(font)
        
        # 创建中心部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        
        # 创建标签页
        self.tab_widget = QTabWidget()
        main_layout.addWidget(self.tab_widget)
        
        # 添加标签页
        self.student_tab = self.create_student_tab()
        self.analysis_tab = self.create_analysis_tab()
        self.thinking_tab = self.create_thinking_tab()
        self.class_tab = self.create_class_tab()
        
        self.tab_widget.addTab(self.student_tab, "学生管理")
        self.tab_widget.addTab(self.analysis_tab, "因材施教")
        self.tab_widget.addTab(self.thinking_tab, "思考过程")
        self.tab_widget.addTab(self.class_tab, "班级分析")
        
        # 状态栏
        self.statusBar().showMessage("就绪")
    
    def create_student_tab(self):
        """创建学生管理标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 工具栏
        toolbar = QHBoxLayout()
        self.add_student_btn = QPushButton("添加学生")
        self.edit_student_btn = QPushButton("编辑学生")
        self.delete_student_btn = QPushButton("删除学生")
        self.refresh_btn = QPushButton("刷新")
        
        toolbar.addWidget(self.add_student_btn)
        toolbar.addWidget(self.edit_student_btn)
        toolbar.addWidget(self.delete_student_btn)
        toolbar.addWidget(self.refresh_btn)
        
        layout.addLayout(toolbar)
        
        # 学生表格
        self.student_table = QTableWidget()
        self.student_table.setColumnCount(6)
        self.student_table.setHorizontalHeaderLabels(["ID", "姓名", "性别", "年龄", "班级", "操作"])
        layout.addWidget(self.student_table)
        
        # 绑定事件
        self.add_student_btn.clicked.connect(self.add_student_dialog)
        self.edit_student_btn.clicked.connect(self.edit_student_dialog)
        self.delete_student_btn.clicked.connect(self.delete_student)
        self.refresh_btn.clicked.connect(self.refresh_student_table)
        
        # 初始化表格
        self.refresh_student_table()
        
        return tab
    
    def create_analysis_tab(self):
        """创建因材施教标签页"""
        tab = QWidget()
        layout = QHBoxLayout(tab)
        
        # 左侧学生列表
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        self.student_list = QListWidget()
        left_layout.addWidget(QLabel("选择学生:"))
        left_layout.addWidget(self.student_list)
        
        # 右侧分析区域
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # 分析按钮
        analysis_buttons = QHBoxLayout()
        self.analyze_btn = QPushButton("分析学生")
        self.plan_btn = QPushButton("生成学习计划")
        analysis_buttons.addWidget(self.analyze_btn)
        analysis_buttons.addWidget(self.plan_btn)
        right_layout.addLayout(analysis_buttons)
        
        # 分析结果
        self.analysis_result = QTextEdit()
        self.analysis_result.setReadOnly(True)
        right_layout.addWidget(QLabel("分析结果:"))
        right_layout.addWidget(self.analysis_result)
        
        # 分割器
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([200, 800])
        layout.addWidget(splitter)
        
        # 绑定事件
        self.analyze_btn.clicked.connect(self.analyze_student)
        self.plan_btn.clicked.connect(self.generate_plan)
        
        # 初始化学生列表
        self.refresh_student_list()
        
        return tab
    
    def create_thinking_tab(self):
        """创建思考过程标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 输入区域
        input_group = QGroupBox("问题输入")
        input_layout = QVBoxLayout(input_group)
        self.question_input = QTextEdit()
        self.question_input.setPlaceholderText("请输入问题，系统将展示思考过程...")
        input_layout.addWidget(self.question_input)
        
        # 按钮
        btn_layout = QHBoxLayout()
        self.generate_thinking_btn = QPushButton("生成思考过程")
        self.clear_thinking_btn = QPushButton("清空")
        btn_layout.addWidget(self.generate_thinking_btn)
        btn_layout.addWidget(self.clear_thinking_btn)
        input_layout.addLayout(btn_layout)
        layout.addWidget(input_group)
        
        # 思考过程输出
        output_group = QGroupBox("思考过程")
        output_layout = QVBoxLayout(output_group)
        self.thinking_output = QTextEdit()
        self.thinking_output.setReadOnly(True)
        output_layout.addWidget(self.thinking_output)
        layout.addWidget(output_group)
        
        # 绑定事件
        self.generate_thinking_btn.clicked.connect(self.generate_thinking)
        self.clear_thinking_btn.clicked.connect(self.clear_thinking)
        
        return tab
    
    def create_class_tab(self):
        """创建班级分析标签页"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # 班级选择
        class_layout = QHBoxLayout()
        class_layout.addWidget(QLabel("选择班级:"))
        self.class_combo = QComboBox()
        class_layout.addWidget(self.class_combo)
        self.analyze_class_btn = QPushButton("分析班级")
        class_layout.addWidget(self.analyze_class_btn)
        layout.addLayout(class_layout)
        
        # 分析结果
        self.class_analysis_result = QTextEdit()
        self.class_analysis_result.setReadOnly(True)
        layout.addWidget(QLabel("班级分析结果:"))
        layout.addWidget(self.class_analysis_result)
        
        # 绑定事件
        self.analyze_class_btn.clicked.connect(self.analyze_class)
        
        # 初始化班级列表
        self.refresh_class_list()
        
        return tab
    
    def refresh_student_table(self):
        """刷新学生表格"""
        students = self.student_manager.get_all_students()
        self.student_table.setRowCount(len(students))
        
        for row, (_, student) in enumerate(students.iterrows()):
            self.student_table.setItem(row, 0, QTableWidgetItem(str(int(student['id'])) if not pd.isna(student['id']) else ''))
            self.student_table.setItem(row, 1, QTableWidgetItem(str(student['name']) if not pd.isna(student['name']) else ''))
            self.student_table.setItem(row, 2, QTableWidgetItem(str(student['gender']) if not pd.isna(student['gender']) else ''))
            self.student_table.setItem(row, 3, QTableWidgetItem(str(int(student['age'])) if not pd.isna(student['age']) else ''))
            self.student_table.setItem(row, 4, QTableWidgetItem(str(student['class']) if not pd.isna(student['class']) else ''))
            
            # 操作按钮
            btn = QPushButton("详情")
            btn.clicked.connect(lambda _, s=student: self.show_student_detail(s))
            self.student_table.setCellWidget(row, 5, btn)
    
    def refresh_student_list(self):
        """刷新学生列表"""
        self.student_list.clear()
        students = self.student_manager.get_all_students()
        for _, student in students.iterrows():
            item = QListWidgetItem(f"{student['name']} ({student['class']})")
            item.setData(Qt.UserRole, int(student['id']))
            self.student_list.addItem(item)
    
    def refresh_class_list(self):
        """刷新班级列表"""
        self.class_combo.clear()
        students = self.student_manager.get_all_students()
        classes = students['class'].unique()
        for cls in classes:
            if str(cls).strip():
                self.class_combo.addItem(str(cls))
    
    def add_student_dialog(self):
        """添加学生对话框"""
        dialog = QDialog(self)
        dialog.setWindowTitle("添加学生")
        layout = QFormLayout(dialog)
        
        # 表单
        name_input = QLineEdit()
        gender_combo = QComboBox()
        gender_combo.addItems(["男", "女"])
        age_input = QLineEdit()
        class_input = QLineEdit()
        learning_style_combo = QComboBox()
        learning_style_combo.addItems(["视觉型", "听觉型", "动手型", "混合型"])
        
        layout.addRow("姓名:", name_input)
        layout.addRow("性别:", gender_combo)
        layout.addRow("年龄:", age_input)
        layout.addRow("班级:", class_input)
        layout.addRow("学习风格:", learning_style_combo)
        
        # 按钮
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("确定")
        cancel_btn = QPushButton("取消")
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addRow(btn_layout)
        
        # 绑定事件
        ok_btn.clicked.connect(lambda: self.save_student(dialog, {
            'name': name_input.text(),
            'gender': gender_combo.currentText(),
            'age': int(age_input.text()) if age_input.text().isdigit() else 0,
            'class': class_input.text(),
            'learning_style': learning_style_combo.currentText()
        }))
        cancel_btn.clicked.connect(dialog.reject)
        
        dialog.exec_()
    
    def edit_student_dialog(self):
        """编辑学生对话框"""
        selected_items = self.student_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "警告", "请选择要编辑的学生")
            return
        
        row = selected_items[0].row()
        student_id = int(self.student_table.item(row, 0).text())
        student = self.student_manager.get_student(student_id)
        
        dialog = QDialog(self)
        dialog.setWindowTitle("编辑学生")
        layout = QFormLayout(dialog)
        
        # 表单
        name_input = QLineEdit(student['name'])
        gender_combo = QComboBox()
        gender_combo.addItems(["男", "女"])
        gender_combo.setCurrentText(student['gender'])
        age_input = QLineEdit(str(int(student['age'])))
        class_input = QLineEdit(student['class'])
        learning_style_combo = QComboBox()
        learning_style_combo.addItems(["视觉型", "听觉型", "动手型", "混合型"])
        learning_style_combo.setCurrentText(student.get('learning_style', '混合型'))
        
        layout.addRow("姓名:", name_input)
        layout.addRow("性别:", gender_combo)
        layout.addRow("年龄:", age_input)
        layout.addRow("班级:", class_input)
        layout.addRow("学习风格:", learning_style_combo)
        
        # 按钮
        btn_layout = QHBoxLayout()
        ok_btn = QPushButton("确定")
        cancel_btn = QPushButton("取消")
        btn_layout.addWidget(ok_btn)
        btn_layout.addWidget(cancel_btn)
        layout.addRow(btn_layout)
        
        # 绑定事件
        ok_btn.clicked.connect(lambda: self.update_student(dialog, student_id, {
            'name': name_input.text(),
            'gender': gender_combo.currentText(),
            'age': int(age_input.text()) if age_input.text().isdigit() else 0,
            'class': class_input.text(),
            'learning_style': learning_style_combo.currentText()
        }))
        cancel_btn.clicked.connect(dialog.reject)
        
        dialog.exec_()
    
    def save_student(self, dialog, student_data):
        """保存学生"""
        if not student_data['name'] or not student_data['class']:
            QMessageBox.warning(self, "警告", "姓名和班级不能为空")
            return
        
        self.student_manager.add_student(student_data)
        self.refresh_student_table()
        self.refresh_student_list()
        self.refresh_class_list()
        dialog.accept()
        QMessageBox.information(self, "成功", "学生添加成功")
    
    def update_student(self, dialog, student_id, student_data):
        """更新学生"""
        if not student_data['name'] or not student_data['class']:
            QMessageBox.warning(self, "警告", "姓名和班级不能为空")
            return
        
        self.student_manager.update_student(student_id, student_data)
        self.refresh_student_table()
        self.refresh_student_list()
        self.refresh_class_list()
        dialog.accept()
        QMessageBox.information(self, "成功", "学生更新成功")
    
    def delete_student(self):
        """删除学生"""
        selected_items = self.student_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "警告", "请选择要删除的学生")
            return
        
        row = selected_items[0].row()
        student_id = int(self.student_table.item(row, 0).text())
        student_name = self.student_table.item(row, 1).text()
        
        if QMessageBox.question(self, "确认", f"确定要删除学生 {student_name} 吗?", 
                               QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.student_manager.delete_student(student_id)
            self.refresh_student_table()
            self.refresh_student_list()
            self.refresh_class_list()
            QMessageBox.information(self, "成功", "学生删除成功")
    
    def show_student_detail(self, student):
        """显示学生详情"""
        dialog = QDialog(self)
        dialog.setWindowTitle(f"学生详情 - {student['name']}")
        layout = QVBoxLayout(dialog)
        
        # 详情文本
        detail_text = QTextEdit()
        detail_text.setReadOnly(True)
        
        # 构建详情内容
        content = f"""
        <h2>学生信息</h2>
        <p><strong>ID:</strong> {student['id']}</p>
        <p><strong>姓名:</strong> {student['name']}</p>
        <p><strong>性别:</strong> {student['gender']}</p>
        <p><strong>年龄:</strong> {student['age']}</p>
        <p><strong>班级:</strong> {student['class']}</p>
        <p><strong>学习风格:</strong> {student.get('learning_style', '未知')}</p>
        """
        
        detail_text.setHtml(content)
        layout.addWidget(detail_text)
        
        # 按钮
        ok_btn = QPushButton("确定")
        ok_btn.clicked.connect(dialog.accept)
        layout.addWidget(ok_btn)
        
        dialog.exec_()
    
    def analyze_student(self):
        """分析学生"""
        selected_item = self.student_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "警告", "请选择要分析的学生")
            return
        
        student_id = selected_item.data(Qt.UserRole)
        student = self.student_manager.get_student(student_id)
        
        # 清空结果
        self.analysis_result.clear()
        self.statusBar().showMessage("正在分析...")
        
        # 启动分析线程
        self.analysis_thread = StreamOutputThread(
            self.analyzer.analyze_student,
            student.to_dict()
        )
        self.analysis_thread.update_signal.connect(self.update_analysis_result)
        self.analysis_thread.finished.connect(lambda: self.statusBar().showMessage("分析完成"))
        self.analysis_thread.start()
    
    def generate_plan(self):
        """生成学习计划"""
        selected_item = self.student_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "警告", "请选择要生成计划的学生")
            return
        
        student_id = selected_item.data(Qt.UserRole)
        student = self.student_manager.get_student(student_id)
        
        # 清空结果
        self.analysis_result.clear()
        self.statusBar().showMessage("正在生成学习计划...")
        
        # 启动生成线程
        self.plan_thread = StreamOutputThread(
            self.analyzer.generate_learning_plan,
            student.to_dict()
        )
        self.plan_thread.update_signal.connect(self.update_analysis_result)
        self.plan_thread.finished.connect(lambda: self.statusBar().showMessage("学习计划生成完成"))
        self.plan_thread.start()
    
    def update_analysis_result(self, content):
        """更新分析结果"""
        self.analysis_result.insertPlainText(content)
        self.analysis_result.moveCursor(self.analysis_result.textCursor().End)
    
    def generate_thinking(self):
        """生成思考过程"""
        question = self.question_input.toPlainText()
        if not question.strip():
            QMessageBox.warning(self, "警告", "请输入问题")
            return
        
        # 清空结果
        self.thinking_output.clear()
        self.statusBar().showMessage("正在生成思考过程...")
        
        # 启动思考线程
        self.thinking_thread = StreamOutputThread(
            self.analyzer.generate_thinking_process,
            question
        )
        self.thinking_thread.update_signal.connect(self.update_thinking_output)
        self.thinking_thread.finished.connect(lambda: self.statusBar().showMessage("思考过程生成完成"))
        self.thinking_thread.start()
    
    def update_thinking_output(self, content):
        """更新思考过程输出"""
        self.thinking_output.insertPlainText(content)
        self.thinking_output.moveCursor(self.thinking_output.textCursor().End)
    
    def clear_thinking(self):
        """清空思考过程"""
        self.question_input.clear()
        self.thinking_output.clear()
    
    def analyze_class(self):
        """分析班级"""
        class_name = self.class_combo.currentText()
        if not class_name:
            QMessageBox.warning(self, "警告", "请选择班级")
            return
        
        # 获取班级学生
        class_students = self.student_manager.get_students_by_class(class_name)
        if len(class_students) == 0:
            QMessageBox.warning(self, "警告", "该班级没有学生")
            return
        
        # 转换为字典列表
        students_list = []
        for _, student in class_students.iterrows():
            students_list.append(student.to_dict())
        
        # 清空结果
        self.class_analysis_result.clear()
        self.statusBar().showMessage("正在分析班级...")
        
        # 启动分析线程
        self.class_analysis_thread = StreamOutputThread(
            self.analyzer.analyze_class,
            students_list
        )
        self.class_analysis_thread.update_signal.connect(self.update_class_analysis_result)
        self.class_analysis_thread.finished.connect(lambda: self.statusBar().showMessage("班级分析完成"))
        self.class_analysis_thread.start()
    
    def update_class_analysis_result(self, content):
        """更新班级分析结果"""
        self.class_analysis_result.insertPlainText(content)
        self.class_analysis_result.moveCursor(self.class_analysis_result.textCursor().End)

# 主函数
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
