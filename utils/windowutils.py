import win32gui
import win32con

def find_window_handle():
    try:
        return win32gui.FindWindow(None, "Dota Stats")
    except:
        return None
    
def minimize_window():
    hwnd = find_window_handle()
    win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)

        
def close_window():
    hwnd = find_window_handle()
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)