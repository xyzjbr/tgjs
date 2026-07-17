import asyncio
import json
import socket
import websockets
from pynput.mouse import Controller, Button
from pynput.keyboard import Controller as KbController, Key, KeyCode
import ctypes

mouse = Controller()
keyboard = KbController()
STEP = 20

user32 = ctypes.windll.user32
SCREEN_W = user32.GetSystemMetrics(0)
SCREEN_H = user32.GetSystemMetrics(1)

KEY_MAP = {
    "escape": Key.esc, "tab": Key.tab, "caps_lock": Key.caps_lock,
    "shift_left": Key.shift_l, "shift_right": Key.shift_r,
    "control_left": Key.ctrl_l, "control_right": Key.ctrl_r,
    "alt_left": Key.alt_l, "alt_right": Key.alt_r,
    "win_left": Key.cmd_l, "win_right": Key.cmd_r,
    "backspace": Key.backspace, "enter": Key.enter, "space": Key.space,
    "page_up": Key.page_up, "page_down": Key.page_down,
    "home": Key.home, "end": Key.end, "delete": Key.delete,
    "left": Key.left, "up": Key.up, "down": Key.down, "right": Key.right,
    "f1": Key.f1, "f2": Key.f2, "f3": Key.f3, "f4": Key.f4,
    "f5": Key.f5, "f6": Key.f6, "f7": Key.f7, "f8": Key.f8,
    "f9": Key.f9, "f10": Key.f10, "f11": Key.f11, "f12": Key.f12,
    "backquote": "`", "minus": "-", "equal": "=",
    "digit1": "1", "digit2": "2", "digit3": "3", "digit4": "4",
    "digit5": "5", "digit6": "6", "digit7": "7", "digit8": "8",
    "digit9": "9", "digit0": "0",
    "key_q": "q", "key_w": "w", "key_e": "e", "key_r": "r", "key_t": "t",
    "key_y": "y", "key_u": "u", "key_i": "i", "key_o": "o", "key_p": "p",
    "key_a": "a", "key_s": "s", "key_d": "d", "key_f": "f", "key_g": "g",
    "key_h": "h", "key_j": "j", "key_k": "k", "key_l": "l",
    "key_z": "z", "key_x": "x", "key_c": "c", "key_v": "v", "key_b": "b",
    "key_n": "n", "key_m": "m",
    "comma": ",", "period": ".", "slash": "/", "semicolon": ";",
    "quote": "'", "bracket_left": "[", "bracket_right": "]",
    "backslash": "\\",
}


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


async def handler(websocket):
    remote = websocket.remote_address
    print(f"[连接] 客户端已连接: {remote}")
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                action = data.get("action")

                if action == "move":
                    direction = data.get("direction")
                    step = data.get("step", STEP)
                    if direction:
                        pos = mouse.position
                        new_x, new_y = pos

                        if direction == "up":
                            new_y -= step
                        elif direction == "down":
                            new_y += step
                        elif direction == "left":
                            new_x -= step
                        elif direction == "right":
                            new_x += step

                        mouse.position = (new_x, new_y)
                        print(f"[移动] {direction} {step}px → ({new_x}, {new_y})")

                elif action == "move_rel":
                    dx = data.get("dx") or 0
                    dy = data.get("dy") or 0
                    pos = mouse.position
                    new_x = pos[0] + dx
                    new_y = pos[1] + dy
                    mouse.position = (new_x, new_y)

                elif action == "center":
                    mouse.position = (SCREEN_W // 2, SCREEN_H // 2)
                    print(f"[校准] 光标居中 → ({SCREEN_W // 2}, {SCREEN_H // 2})")

                elif action == "click":
                    button = data.get("button", "left")
                    if button == "right":
                        mouse.click(Button.right, 1)
                        print(f"[点击] 右键")
                    else:
                        mouse.click(Button.left, 1)
                        print(f"[点击] 左键")

                elif action == "mouse_down":
                    button = data.get("button", "left")
                    if button == "right":
                        mouse.press(Button.right)
                        print(f"[按下] 右键")
                    else:
                        mouse.press(Button.left)
                        print(f"[按下] 左键")

                elif action == "mouse_up":
                    button = data.get("button", "left")
                    if button == "right":
                        mouse.release(Button.right)
                        print(f"[松开] 右键")
                    else:
                        mouse.release(Button.left)
                        print(f"[松开] 左键")

                elif action == "key_press":
                    key_name = data.get("key", "")
                    mapped = KEY_MAP.get(key_name)
                    if mapped is not None:
                        keyboard.press(mapped)
                        keyboard.release(mapped)
                        print(f"[按键] {key_name}")
                    else:
                        print(f"[按键] 未知键: {key_name}")

                elif action == "key_down":
                    key_name = data.get("key", "")
                    mapped = KEY_MAP.get(key_name)
                    if mapped is not None:
                        keyboard.press(mapped)
                        print(f"[按下] {key_name}")
                    else:
                        print(f"[按下] 未知键: {key_name}")

                elif action == "key_up":
                    key_name = data.get("key", "")
                    mapped = KEY_MAP.get(key_name)
                    if mapped is not None:
                        keyboard.release(mapped)
                        print(f"[松开] {key_name}")
                    else:
                        print(f"[松开] 未知键: {key_name}")

                elif action == "type_text":
                    text = data.get("text", "")
                    if text:
                        keyboard.type(text)
                        print(f"[输入] {text}")

                elif action == "ping":
                    await websocket.send(json.dumps({"action": "pong"}))

            except json.JSONDecodeError:
                print(f"[错误] 无效JSON: {message}")
    except websockets.exceptions.ConnectionClosed:
        print(f"[断开] 客户端已断开: {remote}")


async def main():
    ip = get_local_ip()
    port = 8765
    print("=" * 40)
    print("  VirtualMouse Server")
    print(f"  本机IP: {ip}")
    print(f"  端口: {port}")
    print(f"  手表端请输入: {ip}")
    print("=" * 40)

    async with websockets.serve(handler, "0.0.0.0", port):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
