from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMenu

def createContextMenu(node, model, dataAttr, actions):
    node.setContextMenuPolicy(Qt.CustomContextMenu)
    def createTrigger(action):
        index = node.currentIndex()
        row = index.row()
        result = getattr(model, dataAttr)[row]
        return lambda pos: action(result)
    def contextMenu(position):
        menu = QMenu(node)
        for (label, trigger) in actions:
            menu.addAction(label).triggered.connect(createTrigger(trigger))
        menu.exec(node.mapToGlobal(position))
    node.customContextMenuRequested.connect(contextMenu)
