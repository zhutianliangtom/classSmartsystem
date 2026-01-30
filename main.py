#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
班级智能管理系统主程序
"""

import sys
import os
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

if __name__ == "__main__":
    # 创建应用程序实例
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = MainWindow()
    window.show()
    
    # 运行应用程序
    sys.exit(app.exec_())
