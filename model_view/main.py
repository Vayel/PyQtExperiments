from PyQt5 import QtCore, QtGui, QtWidgets

class Orchard():
    def __init__(self, name, position):
        self.setName(name)
        self.setPosition(position)

    # Getters
    def name(self): return self._name
    def position(self): return self._position

    # Setters
    def setName(self, name):
        self._name = name

    def setPosition(self, position):
        self._position = position

class Window(QtWidgets.QTreeView):
    def __init__(self, parent=None):
        QtWidgets.QTreeView.__init__(self, parent)

        orchard1 = Orchard("Orchard 1", (49, 30))
        orchardItem1 = QtGui.QStandardItem(orchard1.name())
        orchardItem1.setData(orchard1, QtCore.Qt.UserRole)

        orchard2 = Orchard("Orchard 2", (15, 70))
        orchardItem2 = QtGui.QStandardItem(orchard2.name())
        orchardItem2.setData(orchard2, QtCore.Qt.UserRole)

        model = QtGui.QStandardItemModel(self)
        model.appendColumn([])
        model.insertRow(0, orchardItem1)
        model.insertRow(1, orchardItem2)
        self.setModel(model)

        #self.setHeaderHidden(True)
        self.show()

    def currentChanged(self, current, old):
        print(current.data(QtCore.Qt.UserRole).position()) 

def main(argv=None):
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(argv)

        window = Window()

        return app.exec_()

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))
