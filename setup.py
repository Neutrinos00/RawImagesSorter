import sys

from cx_Freeze import setup, Executable

if sys.platform == "win32":
    base = "Win32GUI"
else:
    base = None

executables = [Executable("main.py", base=base, icon='Icons/icon.ico')]
includes_files = [
        "Icons\caca_.png",
        "Icons\caca.png",
        "Icons\check-mark_dark.png",
        "Icons\check-mark.png",
        "Icons\close-cross_dark.png",
        "Icons\close-cross.png",
        "Icons\move-to-next_dark.png",
        "Icons\move-to-next.png",
        "Icons\move-to-prev_dark.png",
        "Icons\move-to-prev.png",
        "Icons\icon.ico",
        "DEFAULT.json",
        ]

exclude_packages =[
    "tkinter",
    "matplotlib",
    "email",
    "PIL",
    "imageio",
    "skimage",
    "multiprocessing",
    "scipy",
    "unittest",
    "asyncio",
    "matplotlib",
    "http",
    "html",
    "xml",
]

packages = ["os", "sys", "PyQt5", "rawpy", "json"]
options = {
    'build_exe': {    
        'packages': packages,
        'include_files': includes_files,
        "excludes": exclude_packages,
    },
}

setup(
    name = "Trieur d'image RAW",
    options = options,
    version = "1.0",
    description = "Trieur d'image RAW pour la série SONY Alpha (fichier .ARW)\
        Version 1.0, écrit en Python 3.9.5, Modules : PyQt5, rawpy\
        Développé par LDB pour le poto FBV",
    executables = executables
)
