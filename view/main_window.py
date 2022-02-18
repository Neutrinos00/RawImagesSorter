import os

import json
import exifread
import pyperclip

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QImage, QPixmap, QTransform
import rawpy


class WQLineEdit(QLineEdit):
    pass


class WQSpinBox(QSpinBox):
    pass


class GUI(QMainWindow):
    """ Principal Main Windows GUI class """

    def __init__(self):

        QMainWindow.__init__(self)

        self.__filePath = None
        self.__folderPath = None
        self.__newFilename = None
        self.__filePathList = []

        self.__isOpen = False
        self.__i = 0

        self.__DEFAULT = {
            'DEFAULT_OPENPATH': "C:/Users/lucas/Desktop",
            'DEFAULT_SAVEPATH': "C:/Users/lucas/Desktop/Save",
            'DEFAULT_BINPATH': "C:/Users/lucas/Desktop/Bin",
            'use_bin': False,
            'use_toolbar': True,
            'use_darkmode': False,
            'n_val': 0,
            'n_del': 0,
            'n_next': 0, 
        }

        self._initDefaultParameters()
        self._initUI()
        self._initWidgetWithDefaultParameters()


    def _initDefaultParameters(self):
        self.TITLE = "Trieur d'image RAW"
        self.GEOMETRY = (300, 300, 640, 480)
        self.FILE_EXT = ".jpg"
        self.ABOUT1 = "Trieur d'image RAW pour la série SONY Alpha (fichier .ARW)"
        self.ABOUT2 = "Version 1.0, écrit en Python 3.9.5, Modules : PyQt5, rawpy"
        self.ABOUT3 = "Développé par LDB pour le poto FBV"

        self._getDefaultParameters()
        self._initLog()


    def _initUI(self):
        self.setWindowTitle(self.TITLE)
        self.setGeometry(*self.GEOMETRY)
        self.setWindowIcon(QIcon('Icons/caca.png'))
        
        self._createActions()
        self._createStatusBar()
        self._createMenuBar()
        self._createToolBar()
        self._createStatusBar()
        self._createImageLabel()

        self.setVisible(True)


    def _initWidgetWithDefaultParameters(self):
        if self.__DEFAULT['use_bin']:
            self.binCheckAction.setChecked(True)
        else:
            self.binCheckAction.setChecked(False)

        if self.__DEFAULT['use_toolbar']:
            self.dispToolBarAction.setChecked(True)
        else:
            self.dispToolBarAction.setChecked(False)
        
        if self.__DEFAULT['use_darkmode']:
            self.dispDarkModeAction.setChecked(True)
            self._setDarkMode()
        else:
            self.dispDarkModeAction.setChecked(False)
            self._setWhiteMode()


    def _initLog(self):
        try:
            with open("log.txt", 'w') as f:
                f.truncate()
        except:
            pass


    def _createActions(self):

        def fileActions():
            self.newAction = QAction(self)
            self.newAction.setText("&New")
            self.newAction.setStatusTip("Nouveau Tri")

        def editActions():
            self.cancelAction = QAction(self)
            self.copyAction = QAction(self)

            self.cancelAction.setText("&Annuler (Ctrl+Z)")
            self.copyAction.setText("&Copier le nom du fichier (Ctrl+C)")
            
            self.cancelAction.setStatusTip("Annuler la dernière action")
            self.copyAction.setStatusTip("Copier le nom du fichier")

            self.cancelAction.triggered.connect(self._cancelLog)
            self.copyAction.triggered.connect(self._copyFilename)


        def configActions():
            self.fullScreenAction = QAction(self)
            self.choosePathAction = QAction(self)
            self.binCheckAction = QAction(self)
            self.dispToolBarAction = QAction(self)
            self.dispDarkModeAction = QAction(self)
            self.dispStatsAction = QAction(self)
            self.dispAboutAction = QAction(self)

            self.fullScreenAction.setText("&Full screen (F11)")
            self.choosePathAction.setText("&Dossiers de sauvegarde")
            self.binCheckAction.setText("&Suppr auto")
            self.dispToolBarAction.setText("&Bar d'outils")
            self.dispDarkModeAction.setText("&Dark Mode")
            self.dispStatsAction.setText("&Afficher les stats")
            self.dispAboutAction.setText('&A propos du soft')
            
            self.fullScreenAction.setStatusTip("Full screen")
            self.choosePathAction.setStatusTip("Modifier les dossiers de sauvegarde")
            self.binCheckAction.setStatusTip("Supprime automatiquement (Attention non restaurable via la corbeille)")
            self.dispToolBarAction.setStatusTip("Afficher la bar d'outils")
            self.dispDarkModeAction.setStatusTip("Passer en mode nuit")
            self.dispStatsAction.setStatusTip("Afficher les stats de puis la dernière version")

            self.fullScreenAction.setCheckable(True)
            self.binCheckAction.setCheckable(True)
            self.dispToolBarAction.setCheckable(True)
            self.dispDarkModeAction.setCheckable(True)
           
            self.fullScreenAction.setChecked(False)
            
            self.fullScreenAction.triggered.connect(self._setFullScreen)
            self.newAction.triggered.connect(self._openFileDialog)
            self.choosePathAction.triggered.connect(self._openConfigPathDialog)
            self.binCheckAction.triggered.connect(self._setUseBin)
            self.dispToolBarAction.triggered.connect(self._actionCheckDispToolBar)
            self.dispDarkModeAction.triggered.connect(self._setStyleSheet)
            self.dispStatsAction.triggered.connect(self._openStatsDialog)
            self.dispAboutAction.triggered.connect(self._openAboutDialog)

        def toolbarActions():
            self.precAction = QAction(self)
            self.delAction = QAction(self)
            self.valAction = QAction(self)
            self.suivAction = QAction(self)

            self.precAction.setToolTip("Precedent (Left)")
            self.delAction.setToolTip("Jeter (Down)")
            self.valAction.setToolTip("Valider (Up)")
            self.suivAction.setToolTip("Suivant (Right)")

            self.precAction.triggered.connect(lambda: self._actionPrec(writeLog=True))
            self.delAction.triggered.connect(lambda: self._actionDel(writeLog=True))
            self.valAction.triggered.connect(lambda: self._actionVal(writeLog=True))
            self.suivAction.triggered.connect(lambda: self._actionNext(writeLog=True))

        fileActions()
        editActions()
        configActions()
        toolbarActions()


    def _createMenuBar(self):
        self.menuBar = QMenuBar()
        
        editMenu = QMenu("&Edit", self)
        editMenu.addAction(self.cancelAction)
        editMenu.addAction(self.copyAction)

        configMenu = QMenu("&Config", self)
        configMenu.addAction(self.fullScreenAction)
        configMenu.addAction(self.choosePathAction)
        configMenu.addAction(self.binCheckAction)
        configMenu.addAction(self.dispToolBarAction)
        configMenu.addAction(self.dispDarkModeAction)
        configMenu.addAction(self.dispStatsAction)
        configMenu.addAction(self.dispAboutAction)
        
        self.menuBar.addAction(self.newAction)
        self.menuBar.addMenu(editMenu)
        self.menuBar.addMenu(configMenu)
       
        self.setMenuBar(self.menuBar)


    def _createToolBar(self):
        self.toolbar = self.addToolBar("Traitement")
        self.toolbar.setFloatable(True)

        left_spacer = QWidget()
        mid_spacer = QWidget()
        right_spacer = QWidget()
        left_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        mid_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        right_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.textbox = WQLineEdit(self)
        self.textbox.setToolTip("nom du fichier")
        self.textbox.setFocus(False)

        self.spinbox = WQSpinBox(self)
        self.spinbox.valueChanged.connect(self._actionSpinBoxVal)
        self._setSpinBox()

        self.toolbar.addWidget(left_spacer) 
        self.toolbar.addWidget(self.textbox)
        self.toolbar.addWidget(self.spinbox)
        self.toolbar.addWidget(mid_spacer)
        self.toolbar.addAction(self.precAction)
        self.toolbar.addAction(self.delAction)
        self.toolbar.addAction(self.valAction)
        self.toolbar.addAction(self.suivAction)
        self.toolbar.addWidget(right_spacer)

        self.toolbar.setVisible(False)


    def _createStatusBar(self):
        self.statusBar = QStatusBar(self)
        self.setStatusBar(self.statusBar)
        self.statusBar.setVisible(True)


    def _createImageLabel(self):
        self.imageLabel = QLabel(self)
        #self.imageLabel.setMinimumSize(1080, 1697)
        self.imageLabel.setScaledContents(False)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.imageLabel)


    def _createPath(self, path):
        if not os.path.exists(path):
            os.mkdir(path)


    def _actionPrec(self, writeLog=True):
        if len(self.__filePathList) != 0:
            self.__i -= 1
            if self.__i < 0:
                self.__i = len(self.__filePathList) - 1

            self._setTextBox()
            self._setSpinBox()
            self._setImage()
            #if writeLog:
            #    self._setLog('Précédent')


    def _actionDel(self, writeLog=True):
        if len(self.__filePathList) != 0:
            self._createPath(self.__DEFAULT['DEFAULT_BINPATH'])
            self._removeFile()
            self.statusBar.showMessage("Supprimé", 1000)

            del self.__filePathList[self.__i]
            if self.__i == len(self.__filePathList):
                self.__i -= 1

            if len(self.__filePathList) == 0:
                self._setEndWidget()
            else:
                self._setTextBox()
                self._setSpinBox()
                self._setImage()
            
            self.__DEFAULT['n_del'] += 1
            self._setDefaultParameters()
            #if writeLog:
            #    self._setLog('Supprimer')
        

    def _actionVal(self, writeLog=True):
        if len(self.__filePathList) != 0:
            self.__newFilename = self.textbox.text()
            if self.FILE_EXT in self.__newFilename:
                self._createPath(self.__DEFAULT['DEFAULT_SAVEPATH'])
                self._moveFile(self.__DEFAULT['DEFAULT_SAVEPATH'])
                self.statusBar.showMessage("Validé", 1000)

            #
            if writeLog:
                self._setLog(self.__filePathList[self.__i])
            #

            del self.__filePathList[self.__i]
            if self.__i == len(self.__filePathList):
                self.__i -= 1

            if len(self.__filePathList) == 0:
                self._setEndWidget()
            else:
                self._setTextBox()
                self._setSpinBox()
                self._setImage()
            
            self.__DEFAULT['n_val'] += 1
            self._setDefaultParameters()
            if writeLog:
                self._setLog(self.__filePathList[self.__i])

        else:
            pass


    def _actionValReverse(self):
        self.__newFilename = self.textbox.text()
        if self.FILE_EXT in self.__newFilename:
            self._moveFile(self.__DEFAULT['DEFAULT_SAVEPATH'])
            self.statusBar.showMessage("Validé", 1000)

            del self.__filePathList[self.__i]
            if self.__i == len(self.__filePathList):
                self.__i -= 1

            if len(self.__filePathList) == 0:
                self._setEndWidget()
            else:
                self._setTextBox()
                self._setSpinBox()
                self._setImage()
            
            self.__DEFAULT['n_val'] -= 1
            self._setDefaultParameters()
        else:
            pass

        

    def _actionNext(self, writeLog=True):
        if len(self.__filePathList) != 0:
            self.__i += 1
            if self.__i > len(self.__filePathList) - 1:
                self.__i = 0

            self._setTextBox()
            self._setSpinBox()
            self._setImage()

            self.__DEFAULT['n_next'] += 1
            self._setDefaultParameters()
            #if writeLog:
            #    self._setLog('Suivant')


    def _actionSpinBoxVal(self):
        if self.__isOpen:
            self.__i = self.spinbox.value() - 1
            self._setTextBox()
            #self._setImage() #bug doublage de setImage lorsque emploi de la toolbar
        

    def _actionCheckDispToolBar(self):
        if self.dispToolBarAction.isChecked():
            self.__DEFAULT['use_toolbar'] = True
            if self.__isOpen:
                self.toolbar.setVisible(True)
        else:
            self.__DEFAULT['use_toolbar'] = False
            self.toolbar.setVisible(False)
        
        self._setDefaultParameters()


    def _actionAcceptedPathDialog(self):
        self.__DEFAULT['DEFAULT_SAVEPATH'] = self.savePathEditLine.text()
        self.__DEFAULT['DEFAULT_BINPATH'] = self.binPathEditLine.text()
        
        self._setDefaultParameters()

        self.dialogConfigPath.reject()


    def _removeFile(self):
        if self.__DEFAULT['use_bin']:
            os.remove(self.__filePathList[self.__i])
        else:
            self.__newFilename = self.textbox.text()
            self._moveFile(self.__DEFAULT['DEFAULT_BINPATH'])


    def _moveFile(self, MOVEPATH: str):
        filepath = os.path.join(MOVEPATH, self.__newFilename)
        os.rename(self.__filePathList[self.__i], filepath)

  
    def _openFileDialog(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.ExistingFile)
        dialog.setViewMode(QFileDialog.Detail)
        self.__filePath, _ = dialog.getOpenFileName(
            self,
            'Selection du fichier RAW',
            self.__DEFAULT['DEFAULT_OPENPATH'],
            'Image File (*{})'.format(self.FILE_EXT),
        )

        if self.__filePath != '':
            self._setPathFileList()
            self._setChooseIndex()

            self._setImage()
            self._setTextBox()
            self._setSpinBox()

            self.toolbar.setVisible(True)
            self.toolbar.setFocus(False)

            self.showMaximized()

            self.__isOpen = True


    def _openConfigPathDialog(self):
        self.dialogConfigPath = QDialog(self)
        self.dialogConfigPath.setWindowTitle("Chemins d'accès")
        self.dialogConfigPath.setGeometry(300, 300, 300, 100)

        self.savePathEditLine = QLineEdit(self.__DEFAULT['DEFAULT_SAVEPATH'])
        self.binPathEditLine = QLineEdit(self.__DEFAULT['DEFAULT_BINPATH'])
        
        if self.__DEFAULT['use_bin']:
            self.binPathEditLine.setEnabled(True)
        else:
            self.binPathEditLine.setEnabled(False)

        formLayout = QFormLayout()
        formLayout.addRow("Sauvegarde:", self.savePathEditLine)
        formLayout.addRow("Corbeille:", self.binPathEditLine)

        btnBox = QDialogButtonBox()
        btnBox.setStandardButtons(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )

        btnBox.accepted.connect(self._actionAcceptedPathDialog)
        btnBox.rejected.connect(self.dialogConfigPath.reject)

        formLayout.addWidget(btnBox)
        self.dialogConfigPath.setLayout(formLayout)
        self.dialogConfigPath.exec_()


    def _openStatsDialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Statistiques")

        formLayout = QFormLayout()
        textLabel1 = QLabel()
        textLabel2 = QLabel()
        textLabel3 = QLabel()
        textLabel1.setText('total images validées = '+str(self.__DEFAULT['n_val']))
        textLabel2.setText('total images supprimées = '+str(self.__DEFAULT['n_del']))
        textLabel3.setText('total images skipped = '+str(self.__DEFAULT['n_next']))

        textLabel1.setAlignment(Qt.AlignLeft)
        textLabel2.setAlignment(Qt.AlignLeft)
        textLabel3.setAlignment(Qt.AlignLeft)

        formLayout.addRow(textLabel1)
        formLayout.addRow(textLabel2)
        formLayout.addRow(textLabel3)
        
        dialog.setLayout(formLayout)
        dialog.exec_()


    def _openAboutDialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("A propos")
        
        formLayout = QFormLayout()
        textLabel1 = QLabel()
        textLabel2 = QLabel()
        textLabel3 = QLabel()
        textLabel1.setText(self.ABOUT1)
        textLabel2.setText(self.ABOUT2)
        textLabel3.setText(self.ABOUT3)

        textLabel1.setAlignment(Qt.AlignCenter)
        textLabel2.setAlignment(Qt.AlignCenter)
        textLabel3.setAlignment(Qt.AlignCenter)

        formLayout.addRow(textLabel1)
        formLayout.addRow(textLabel2)
        formLayout.addRow(textLabel3)
        
        dialog.setLayout(formLayout)
        dialog.exec_()


    def _setImage(self):
        path = self.__filePathList[self.__i]
        rot = self._getImageOrientation(path) 

        mat = QPixmap(path)
        #mat.loadFromData(self._getBytesImage(path))

        #if rot:
        #    mat = mat.transformed(QTransform().rotate(-90), Qt.SmoothTransformation) #bug orientation de l'image, modification de la position des images en paysages après une rotation

        #mat=mat.scaled(1096, 1736, Qt.KeepAspectRatio)
        self.imageLabel.setPixmap(mat)
        #self.imageLabel.move(100, 100)
        #self.imageLabel.setAlignment(Qt.AlignCenter)


    def _setTextBox(self):
        self.textbox.setText(os.path.basename(self.__filePathList[self.__i]))


    def _setPathFileList(self):
        if os.path.isfile(self.__filePath):
            self.__folderPath = os.path.dirname(self.__filePath)
            for filename in sorted(os.listdir(self.__folderPath)):
                if self.FILE_EXT in filename:
                    self.__filePathList.append('/'.join([self.__folderPath, filename]))
        else:
            pass


    def _setChooseIndex(self):
        self.__i = self.__filePathList.index(self.__filePath)


    def _setSpinBox(self):
        self.spinbox.setRange(1, len(self.__filePathList))
        self.spinbox.setPrefix("{} / ".format(len(self.__filePathList)))
        self.spinbox.setValue(self.__i + 1)


    def _setEndWidget(self):
        mat = QPixmap()
        mat.load("Icons/caca_.png")
        self.imageLabel.setPixmap(mat)

        self.__isOpen = False
        self.toolbar.setVisible(False)


    def _setStyleSheet(self):
        if self.dispDarkModeAction.isChecked():
            self._setDarkMode()
            self.__DEFAULT['use_darkmode'] = True
        else:
            self._setWhiteMode()
            self.__DEFAULT['use_darkmode'] = False
        
        self._setDefaultParameters()


    def _setDarkMode(self):
        self.setStyleSheet("color:rgb(37,150,190); background:rgb(30,30,30);")
        self.toolbar.setStyleSheet("color:rgb(37,150,190); background:rgb(51,51,51);") #color:rgb(37,150,190)
        self.menuBar.setStyleSheet("background:rgb(60,60,60);")
        self.textbox.setStyleSheet("background:rgb(30,30,30);")
        self.spinbox.setStyleSheet("background:rgb(30,30,30);")

        self.precAction.setIcon(QIcon('Icons/move-to-prev_dark.png'))
        self.delAction.setIcon(QIcon('Icons/close-cross_dark.png'))
        self.valAction.setIcon(QIcon('Icons/check-mark_dark.png'))
        self.suivAction.setIcon(QIcon('Icons/move-to-next_dark.png'))


    def _setWhiteMode(self):
        self.setStyleSheet("color:rgb(30,30,30); background:white;")
        self.toolbar.setStyleSheet("background:white;")
        self.menuBar.setStyleSheet("background:rgb(230,230,230); selection-color:rgb(250,250,250);")
        self.textbox.setStyleSheet("background:rgb(230,230,230);")
        self.spinbox.setStyleSheet("background:rgb(230,230,230);")

        self.precAction.setIcon(QIcon('Icons/move-to-prev.png'))
        self.delAction.setIcon(QIcon('Icons/close-cross.png'))
        self.valAction.setIcon(QIcon('Icons/check-mark.png'))
        self.suivAction.setIcon(QIcon('Icons/move-to-next.png'))


    def _setUseBin(self):
        if self.binCheckAction.isChecked():
            self.__DEFAULT['use_bin'] = True
        else:
            self.__DEFAULT['use_bin'] = False
        
        self._setDefaultParameters()


    def _setFullScreen(self):
        if self.fullScreenAction.isChecked():
            self.showFullScreen()
        else:
            self.showMaximized()


    def _setDefaultParameters(self):
        try:
            with open("DEFAULT.json", "w") as f: 
                json.dump(self.__DEFAULT, f)
        except:
            self.statusBar.showMessage("Error with loading json")


    def _setLog(self, action: str):
        try:
            with open('log.txt', 'a') as f:
                f.write(action+'\n')
            self.cancelAction.setText("&Annuler (Ctrl+Z)        {}".format(action))
        except:
            pass


    def _getBytesImage(self, path: str): #-> np.array:
        with rawpy.imread(path) as raw:
            try:
                thumb = raw.extract_thumb()
            except rawpy.LibRawNoThumbnailError:
                print('no thumbnail found')
            except rawpy.LibRawUnsupportedThumbnailError:
                print('unsupported thumbnail')
            else:
                return thumb.data   


    def _getImageOrientation(self, path: str) -> bool:
        with open(path, 'rb') as f:
            tags = exifread.process_file(f)
            for key, val in tags.items():
                if 'Image Orientation' in key:
                    if 'Rotated 90 CCW' in str(val):
                        return True
                    else:
                        return False


    def _getDefaultParameters(self):
        try:
            with open("DEFAULT.json", "r") as f: 
                self.__DEFAULT = json.load(f)
        except:
            pass


    def _getLog(self) -> str:
        try:
            with open("log.txt", 'r') as f:
                lines = f.readlines()
                return lines[-1]
        except:
            pass


    def _copyFilename(self):
        try:
            pyperclip.copy(os.path.basename(self.__filePathList[self.__i]))
        except:
            pass


    def _cancelLog(self):
        last_action = self._getLog()
        if last_action is not None:
            if 'Suivant' in last_action:
                self._actionPrec(writeLog=False)
            elif 'Précédent' in last_action:
                self._actionNext(writeLog=False)
            else:
                pass


    def mousePressEvent(self, event):
        focused_widget = QApplication.focusWidget()
        if isinstance(focused_widget, WQLineEdit):
            focused_widget.clearFocus()
        if isinstance(focused_widget, WQSpinBox):
            focused_widget.clearFocus()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            if self.__isOpen:
                self._actionPrec(writeLog=True)
        elif event.key() == Qt.Key_Down:
            if self.__isOpen:
                self._actionDel(writeLog=True)
        elif event.key() == Qt.Key_Up:
            if self.__isOpen:
                self._actionVal(writeLog=True)
        elif event.key() == Qt.Key_Right:
            if self.__isOpen:
                self._actionNext(writeLog=True)
        elif event.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showMaximized()
                self.fullScreenAction.setChecked(False)
            else:
                self.showFullScreen()
                self.fullScreenAction.setChecked(True)
        else:
            pass