"""
Docked Documentation Viewer for OAS Generation Tool.
Uses multiprocessing for pywebview (stable) + pygetwindow for position control.
IPC via multiprocessing.Value for snap flag.
"""

import multiprocessing
from multiprocessing import Value
import os
import sys
import ctypes


def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def debug_log(msg):
    pass


class DocViewerAPI:
    """JavaScript API exposed to the webview for IPC."""

    def __init__(self, snap_flag, sync_queue=None):
        self._snap_flag = snap_flag
        self._sync_queue = sync_queue

    def toggle_snap(self):
        """Toggle snap state - called from JavaScript."""
        current = self._snap_flag.value
        self._snap_flag.value = 0 if current else 1
        debug_log(f"toggle_snap called by JS. New state: {self._snap_flag.value}")
        return bool(self._snap_flag.value)

    def get_snap_state(self):
        """Get current snap state - called from JavaScript."""
        return bool(self._snap_flag.value)

    def print_doc(self):
        pass

    def save_html(self):
        pass

    def sync_editor(self, info):
        """Called from JS to sync the YAML editor to the current documentation section."""
        debug_log(f"API sync_editor called with: {info}")
        if self._sync_queue:
            self._sync_queue.put(info)
        return True


def _run_webview_docked(
    html_path, title, x, y, width, height, snap_flag, sync_queue=None, cmd_queue=None
):
    """Run pywebview in a separate process with initial position and JS API."""
    try:
        import webview

        debug_log(f"Starting webview process for {title}")

        # Create API instance with shared snap flag and sync queue
        api = DocViewerAPI(snap_flag, sync_queue=sync_queue)

        window = webview.create_window(
            title,
            html_path,
            width=width,
            height=height,
            x=x,
            y=y,
            min_size=(400, 300),
            js_api=api,  # Expose Python API to JavaScript
        )

        def monitor_snap(window, snap_flag, cmd_queue=None):
            import time

            debug_log(f"Monitor started for {window.title}")
            last_state = None  # Force initial sync to the UI

            while True:
                try:
                    # 1. Process JS commands from Python
                    if cmd_queue and not cmd_queue.empty():
                        try:
                            while not cmd_queue.empty():
                                script = cmd_queue.get_nowait()
                                debug_log(f"Executing JS from queue: {script}")
                                window.evaluate_js(script)
                        except Exception as ce:
                            debug_log(f"JS Command error: {ce}")

                    # 2. Process Snap state
                    current = bool(snap_flag.value)
                    if last_state is None or current != last_state:
                        debug_log(
                            f"Syncing state to UI: {current} (last: {last_state})"
                        )

                        # Retry logic for evaluate_js
                        retries = 5  # More retries for initial sync
                        success = False
                        while retries > 0:
                            try:
                                window.evaluate_js(
                                    f"window.setSnapState({str(current).lower()})"
                                )
                                last_state = current
                                success = True
                                break
                            except Exception:
                                retries -= 1
                                time.sleep(0.2)

                        if not success:
                            debug_log(f"Failed to sync state to UI after retries")
                            # We don't update last_state so it tries again next iteration
                except Exception as e:
                    debug_log(f"Monitor loop error: {e}")

                time.sleep(0.2)  # Increased frequency (5Hz)

        webview.start(monitor_snap, args=(window, snap_flag, cmd_queue))
    except Exception as e:
        print(f"WebView error: {e}")


class DockedDocViewer:
    """
    Docked documentation viewer using multiprocessing.
    Position sync is handled by the main app via polling with debounce.
    Snap state is controlled via shared memory (multiprocessing.Value).
    """

    def __init__(
        self,
        parent,
        html_path: str,
        title: str = "API Documentation",
        snap_default: bool = True,
        file_name: str = "",
        on_snap_callback=None,
        on_focus_callback=None,
        on_sync_editor_callback=None,
    ):
        self.parent = parent
        self.html_path = html_path
        self.file_name = file_name  # Track which file this viewer is for
        self.process = None
        self._closed = False

        # Unique window title to avoid pygetwindow mismatches
        import time

        self.unique_id = int(time.time() * 1000) % 10000
        self._window_title = f"{title} [{self.unique_id}]"
        self.title = self._window_title

        self._on_snap_callback = (
            on_snap_callback  # Called when snap is enabled (for exclusive snap)
        )
        self._on_focus_callback = (
            on_focus_callback  # Called when window gains focus while snapped
        )
        self._on_sync_editor_callback = (
            on_sync_editor_callback  # Called when viewer requests sync
        )
        self._sync_queue = (
            multiprocessing.Queue()
        )  # Queue to receive sync requests from viewer processes
        self._cmd_queue = (
            multiprocessing.Queue()
        )  # Queue to send JS commands to viewer processes
        self._is_focused = False  # Track focus state

        # Shared memory for snap flag (1 = snapped, 0 = unsnapped)
        self._snap_flag = Value(ctypes.c_int, 1 if snap_default else 0)

        # Debounce state
        self._last_parent_x = None
        self._last_parent_y = None
        self._last_parent_width = None
        self._last_parent_height = None
        self._position_stable_count = 0
        self._STABLE_THRESHOLD = 2  # Reduced for responsiveness

        # Get initial position
        parent.update_idletasks()
        self.parent_x = parent.winfo_x()
        self.parent_y = parent.winfo_y()
        self.parent_width = parent.winfo_width()
        title_bar_height = parent.winfo_rooty() - parent.winfo_y()
        self.parent_height = parent.winfo_height() + title_bar_height + 8

        self.doc_x = self.parent_x + self.parent_width
        self.doc_y = self.parent_y
        self.doc_width = max(800, self.parent_width)
        self.doc_height = self.parent_height

        self._start_webview()
        self._start_sync_timer()

    def _start_webview(self):
        """Start pywebview in a separate process with shared snap flag and sync queue."""
        self.process = multiprocessing.Process(
            target=_run_webview_docked,
            args=(
                self.html_path,
                self._window_title,
                self.doc_x,
                self.doc_y,
                self.doc_width,
                self.doc_height,
                self._snap_flag,
                self._sync_queue,
                self._cmd_queue,
            ),
        )
        self.process.daemon = True
        self.process.start()

    def _start_sync_timer(self):
        """Start a timer to periodically sync window position."""
        self._sync_position()

    @property
    def is_snapped(self):
        """Check if snap is enabled (reads shared memory)."""
        return bool(self._snap_flag.value)

    def set_snap(self, snapped: bool):
        """Set snap state (writes to shared memory)."""
        self._snap_flag.value = 1 if snapped else 0
        debug_log(f"Backend set_bound to {snapped} for {self.file_name}")

    def _sync_position(self):
        """Sync doc window position with parent, process sync queue, with mouse-guard and stability check."""
        if self._closed:
            return

        # Process any sync requests from the viewer
        if not self._sync_queue.empty():
            try:
                while not self._sync_queue.empty():
                    item_info = self._sync_queue.get_nowait()
                    if self._on_sync_editor_callback:
                        self._on_sync_editor_callback(self, item_info)
            except Exception as e:
                debug_log(f"Sync queue error: {e}")

        # Check for mouse button state (Win32 API)
        # VK_LBUTTON = 0x01. If bit is set, mouse is down.
        is_mouse_down = ctypes.windll.user32.GetAsyncKeyState(0x01) & 0x8000
        if is_mouse_down:
            # Skip movement while dragging to avoid fighting the user
            self._position_stable_count = 0
            if not self._closed:
                self.parent.after(50, self._sync_position)
            return

        # Track snap state changes for exclusive snap callback
        current_snap = self.is_snapped
        if not hasattr(self, "_last_snap_state"):
            self._last_snap_state = current_snap

        if current_snap and not self._last_snap_state:
            if self._on_snap_callback:
                self._on_snap_callback(self)
        self._last_snap_state = current_snap

        if not current_snap:
            if not self._closed:
                self.parent.after(100, self._sync_position)
            return

        if self.process and not self.process.is_alive():
            self._closed = True
            return

        try:
            current_x = self.parent.winfo_x()
            current_y = self.parent.winfo_y()
            current_width = self.parent.winfo_width()
            current_height = self.parent.winfo_height()

            # Position stability check
            if (
                current_x == self._last_parent_x
                and current_y == self._last_parent_y
                and current_width == self._last_parent_width
                and current_height == self._last_parent_height
            ):
                self._position_stable_count += 1
            else:
                self._position_stable_count = 0
                self._last_parent_x = current_x
                self._last_parent_y = current_y
                self._last_parent_width = current_width
                self._last_parent_height = current_height

            if self._position_stable_count >= self._STABLE_THRESHOLD:
                import pygetwindow as gw

                windows = gw.getWindowsWithTitle(self._window_title)

                # Filter for exact match to avoid catching main window or other viewers
                target_window = None
                for w in windows:
                    if w.title == self._window_title:
                        target_window = w
                        break

                if target_window:
                    win = target_window
                    doc_x, doc_y = win.left, win.top

                    # Focus Detection: Check if this window is currently active
                    try:
                        active_win = gw.getActiveWindow()
                        is_currently_focused = (
                            active_win and active_win.title == self._window_title
                        )
                        if is_currently_focused and not self._is_focused:
                            # Gained focus!
                            debug_log(
                                f"Viewer (Bound) gained focus: {self._window_title}"
                            )
                            if self._on_focus_callback:
                                self._on_focus_callback(self)
                        self._is_focused = is_currently_focused
                    except Exception as fe:
                        debug_log(f"Focus check error: {fe}")

                    # Store current position to track dragging
                    self._last_real_doc_x = doc_x
                    self._last_real_doc_y = doc_y

                    title_bar_height = self.parent.winfo_rooty() - self.parent.winfo_y()
                    outer_height = current_height + title_bar_height + 8
                    target_x = current_x + current_width
                    target_y = current_y

                    if (
                        abs(doc_x - target_x) > 2
                        or abs(doc_y - target_y) > 2
                        or abs(win.height - outer_height) > 2
                    ):
                        win.moveTo(target_x, target_y)
                        win.resizeTo(win.width, outer_height)

        except Exception:
            pass

        if not self._closed:
            self.parent.after(100, self._sync_position)

    def evaluate_js(self, script: str):
        """Execute JavaScript in the viewer process via the command queue."""
        if not self._closed and self._cmd_queue:
            try:
                self._cmd_queue.put(script)
            except Exception as e:
                debug_log(f"Error queueing JS: {e}")

    def focus(self):
        """Bring the documentation window to the front. Returns True if successful, False if window is closed."""
        try:
            import pygetwindow as gw

            windows = gw.getWindowsWithTitle(self._window_title)
            if windows:
                win = windows[0]
                if not win.isActive:
                    win.activate()
                return True
            else:
                # Window not found - viewer is closed
                self._closed = True
                return False
        except Exception:
            return False

    def close(self):
        """Close the viewer."""
        self._closed = True
        if self.process and self.process.is_alive():
            self.process.terminate()
        # Clean up reference in parent list is handled by parent loop
        pass

    @property
    def is_closed(self):
        """Check if viewer is closed."""
        if self.process and not self.process.is_alive():
            self._closed = True
        return self._closed
