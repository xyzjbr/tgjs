[README.md](https://github.com/user-attachments/files/30120579/README.md)
# 体感键鼠服务端

Windows 端服务器，配合鸿蒙手表端收费软件《体感键鼠》使用，通过 WebSocket 接收手表指令控制电脑鼠标和键盘。

## 功能

- 鼠标移动（方向键 / 相对位移）
- 鼠标点击（左键 / 右键 / 按下 / 松开）
- 键盘按键（按下 / 松开 / 输入文本）
- 光标居中校准
- 自动获取本机 IP

## 快速开始

### 方式一：直接运行（推荐开发时）

```bash
pip install -r requirements.txt
python virtual_mouse_server.py
```

### 方式二：使用启动脚本

双击 `启动虚拟鼠标.bat`，会自动检查依赖并启动服务器。

### 方式三：打包为 exe

```bash
pip install pyinstaller
pyinstaller VirtualMouseServer.spec
```

打包产物位于 `dist/VirtualMouseServer.exe`。

## 依赖

- Python 3.8+
- websockets >= 12.0
- pynput >= 1.7.6

## 协议

MIT License
