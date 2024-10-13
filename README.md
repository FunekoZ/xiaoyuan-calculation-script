# xiaoyuan-calculation-script

最泛用(?)的小猿口算答题脚本  
（虽然我慢了点，但是我在哪都能用啊~）

## 上手指南
使用`BlueStacks`模拟器运行Android虚拟机 </br>
使用`BlueStacks脚本管理器`手写录入`>` `<`的输入内容并调整至5倍速 </br>
![](https://github.com/ChaosJulien/XiaoYuanKouSuan_Auto/blob/main/image/example2.png) </br>
将其绑定热键至`,` `.`

## 配置要求

1. 本项目基于Python 3.12.5进行开发
2. 本项目使用了tesseract文本识别(OCR)引擎

## **安装步骤**

1. 在[Python](https://www.python.org/) 下载对应Python版本
2. 在[tesseract](https://github.com/tesseract-ocr/tesseract)下载Windows版本，并安装中文语言确保最佳兼容性
3. 下载[小猿搜题.py](https://github.com/ChaosJulien/XiaoYuanKouSuan_Auto/blob/main/%E5%B0%8F%E7%8C%BF%E6%90%9C%E9%A2%98.py)
4. 安装所需的Python库（有两种安装命令，第一种是安装速度更快的清华大学镜像源，第二种是官方镜像源）👇无论哪个都行，反正选一个

清华大学镜像源
```bash
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple opencv-python numpy pyautogui pytesseract keyboard
```
官方镜像源
```bash
pip install opencv-python numpy pyautogui pytesseract keyboard
```
5. 调整第9行代码路径为你的tesseract安装路径</br>
![](https://github.com/ChaosJulien/XiaoYuanKouSuan_Auto/blob/main/image/example3.png)
6. 本项目不再严格要求模拟器识别时的位置摆放。运行代码后，会出现左右两个识别框，  
只需分别拖动放置在左右两个数字上，即可开始识别。 </br>
![](https://github.com/FunekoZ/xiaoyuan-calculation-script/blob/main/exp.png)


## 使用到的框架

- [Python](https://www.python.org/)
- [tesseract][(https://github.com/tesseract-ocr/tesseract)

## 运行效果

请查看B站视频：https://www.bilibili.com/video/BV1wG2eYdED5

## 致谢

感谢ChaosJulien (chaosjulien@163.com) 提供的思路，本项目在其基础上进行开发改进。  
项目运行配置详见[ChaosJulien XiaoYuanKouSuan_Auto 项目](https://github.com/ChaosJulien/XiaoYuanKouSuan_Auto)。
