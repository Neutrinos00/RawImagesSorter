# -*- coding: utf-8 -*-
""":::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
Projet perso : GUI Trieur d'image pour fichier raw.
Le programme permet d'afficher et de trier des images de type .ARW (Sony Alpha Serie)

Lucas DAL BOSCO - Phyton 3.9.4 - PyQt5 - rawpy
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::"""

import sys

from PyQt5.QtWidgets import QApplication

from view.main_window import GUI

def Main():
    app = QApplication.instance() 
    if not app:
        app = QApplication(sys.argv)

    app.setStyle('Fusion')

    gui = GUI()
    gui.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    Main()
