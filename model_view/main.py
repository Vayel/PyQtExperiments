from PyQt5 import QtCore, QtGui, QtWidgets

class Node():
    def __init__(self, name, parent=None):
        self.setName(name)
        self.setParent(parent)
        self._children = []

        if parent is not None:
            parent.addChild(self)

    def addChild(self, child):
        self._children.append(child)

    def child(self, row):
        try:
            child = self._children[row]
        except KeyError:
            return None
        else:
            return child

    def childCount(self):
        return len(self._children)

    def hasParent(self):
        return self._parent is not None

    def insertChild(self, position, child):
        if position < 0 or position > len(self._children):
            return False

        self._children.insert(position, child)
        child.setParent(self)
        return True

    def removeChild(self, position):
        if position < 0 or position > len(self._children):
            return False

        child = self._children.pop(position)
        child.setParent(None)
        return True

    def row(self):
        if self.hasParent():
            return self._parent._children.index(self)

    # Getters
    def name(self): return self._name
    def parent(self): return self._parent

    # Setters
    def setName(self, name):
        self._name = name

    def setParent(self, parent):
        self._parent = parent


class Orchard(Node):
    def __init__(self, name, position):
        Node.__init__(self, name, None)
        self.setPosition(position)

    # Getters
    def position(self): return self._position

    # Setters
    def setPosition(self, position):
        self._position = position


class OrchardModel(QtCore.QAbstractItemModel):
    def __init__(self, root, parent=None):
        QtCore.QAbstractItemModel.__init__(self, parent)

        self._rootNode = root

    def columnCount(self, parent):
        return 1

    def data(self, index, role):
        if not index.isValid():
            return None

        node = self.getNode(index)

        if role == QtCore.Qt.DisplayRole:
            return node.name()
        elif role == QtCore.Qt.EditRole:
            return node.name()
        elif role == QtCore.Qt.UserRole:
            return node

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable

    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node is not None:
                return node

        return self._rootNode

    def headerData(self, section, orientation, role):
        return "Header not implemented"

    def index(self, row, column, parent):
        childNode = self.getNode(parent).child(row)

        if childNode is not None:
            return self.createIndex(row, column, childNode)
        else:
            return QtCore.QModelIndex()

    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentNode = self.getNode(parent)

        self.beginInsertRows(parent, position, position + rows - 1)

        for i in range(rows):
            childCount = parentNode.childCount()
            childNode = Node("Untitled " + str(childCount))
            success = parentNode.insertChild(position, childNode)

        self.endInsertRows()

        return success

    def parent(self, index):
        node = self.getNode(index) 
        parentNode = node.parent()

        if parentNode == self._rootNode:
            return QtCore.QModelIndex()
        
        return self.createIndex(parentNode.row(), 0, parentNode)

    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        parentNode = self.getNode(parent)

        self.beginRemoveRows(parent, position, position + rows - 1)

        for i in range(rows):
            success = parentNode.removeChild(position)

        self.endRemoveRows()

        return success

    def rowCount(self, parent):
        return self.getNode(parent).childCount()

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        node = self.getNode(index)

        if role == QtCore.Qt.EditRole:
            node.setName(value)
            return True

        return False


class Tree(QtWidgets.QTreeView):
    def __init__(self, parent=None):
        QtWidgets.QTreeView.__init__(self, parent)

    def currentChanged(self, current, old):
        pass


def main(argv=None):
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(argv)

        rootNode = Node("Root")

        leftLeg = Node("Left leg", rootNode)
        leftKnee = Node("Left knee", leftLeg)
        leftFoot = Node("Left foot", leftLeg)

        rightLeg = Node("Right leg", rootNode)
        rightKnee = Node("Right knee", rightLeg)
        rightFoot = Node("Right foot", rightLeg)

        tree = Tree()
        model = OrchardModel(rootNode, tree)
        tree.setModel(model)

        leftLegIndex = model.index(0, 0, QtCore.QModelIndex())
        model.insertRows(1, 2, leftLegIndex)

        tree.show()

        return app.exec_()

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv))
