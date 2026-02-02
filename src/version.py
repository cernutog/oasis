"""
OASIS Version Information.
This is the single source of truth for the application version.
"""

__version__ = "2.0"
BUILD_NUMBER = 36  # 0 = Stable Release. Auto-incremented by build_exe.bat for dev builds.
VERSION = __version__
FULL_VERSION = f"{__version__}.{BUILD_NUMBER}" if BUILD_NUMBER > 0 else __version__
