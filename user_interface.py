import sys
from data_models import Node, Rod, Load, nodes, rods, loads, getNode
from PyQt5.QtWidgets import QWidget, QApplication, QCheckBox, QVBoxLayout, \
    QPushButton, QTableWidget, QLabel, QLineEdit, QTableWidgetItem, QTabWidget


class MainMenu(QWidget):
    def __init__(self):
        super(MainMenu, self).__init__()
        self.setWindowTitle('Модуль расчета')
        self.setMinimumSize(800, 600)

        self.tab_bar = QTabWidget()
        self.node_menu = NodeMenu()
        self.rod_menu = RodMenu()
        self.load_menu = LoadsMenu()
        self.tab_bar.addTab(self.node_menu, 'Узлы')
        self.tab_bar.addTab(self.rod_menu, 'Стержни')
        self.tab_bar.addTab(self.load_menu, 'Нагрузки')

        self.calculate_button = QPushButton('Расчет')

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.tab_bar)
        self.main_layout.addWidget(self.calculate_button)
        self.setLayout(self.main_layout)


class NodeMenu(QWidget):

    def __init__(self):
        super().__init__()
        self.node_index = len(nodes)

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_node)

        self.delete_button = QPushButton('Удалить')
        self.delete_button.clicked.connect(self.delete_node)

        self.nodes_table = QTableWidget()
        self.nodes_table.setColumnCount(4)
        self.nodes_table.setHorizontalHeaderLabels(['X', 'Z', 'Связь по X',
                                                    'Связь по Z'])
        self.add_node_form = AddNodeForm(menu=self)

        box = QVBoxLayout()
        box.addWidget(self.add_button)
        box.addWidget(self.delete_button)
        box.addWidget(self.nodes_table)
        self.setLayout(box)

    def add_node(self):
        self.add_node_form.show()

    def delete_node(self):
        pass

    def changeEvent(self, *args, **kwargs):
        if self.node_index != len(nodes):
            self.update_table()

    def update_table(self):
        self.nodes_table.setRowCount(len(nodes))
        for i in range(len(nodes)):
            node = nodes[i].toList()
            self.nodes_table.setHorizontalHeaderItem(i, QTableWidgetItem(
                str(nodes[i].number)))
            for j in range(len(node)):
                self.nodes_table.setItem(i, j, QTableWidgetItem(str(node[j])))
        self.nodes_table.resizeColumnsToContents()


class AddNodeForm(QWidget):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.add_button = QPushButton('OK')
        self.add_button.clicked.connect(self.add_node)
        self.x_label = QLabel('X:')
        self.z_label = QLabel('Z:')
        self.x_textfield = QLineEdit()
        self.z_textfield = QLineEdit()
        self.connection_label = QLabel('Связи:')
        self.x_checkbox = QCheckBox('X')
        self.z_checkbox = QCheckBox('Z')

        box = QVBoxLayout()
        box.addWidget(self.x_label)
        box.addWidget(self.x_textfield)
        box.addWidget(self.z_label)
        box.addWidget(self.z_textfield)
        box.addWidget(self.connection_label)
        box.addWidget(self.x_checkbox)
        box.addWidget(self.z_checkbox)
        box.addWidget(self.add_button)
        self.setLayout(box)

    def add_node(self):
        number = nodes.__len__() + 1
        x = self.x_textfield.text()
        z = self.z_textfield.text()
        x_connection = self.x_checkbox.isChecked()
        z_connection = self.z_checkbox.isChecked()
        nodes.append(Node(number, x, z, x_connection, z_connection))
        self.menu.update_table()


class RodMenu(QWidget):

    def __init__(self):
        super().__init__()
        self.rod_index = len(rods)
        self.add_rod_form = AddRodForm(menu=self)
        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_rod)
        self.delete_button = QPushButton('Удалить')
        self.delete_button.clicked.connect(self.delete_rod)
        self.rods_table = QTableWidget()
        self.rods_table.setColumnCount(2)
        self.rods_table.setHorizontalHeaderLabels(['Узел 1', 'Узел 2'])
        box = QVBoxLayout()
        box.addWidget(self.add_button)
        box.addWidget(self.delete_button)
        box.addWidget(self.rods_table)
        self.setLayout(box)

    def add_rod(self):
        self.add_rod_form.show()

    def delete_rod(self):
        pass

    def changeEvent(self, *args, **kwargs):
        if self.rod_index != len(rods):
            self.update_table()

    def update_table(self):
        self.rods_table.setRowCount(len(rods))
        for i in range(len(rods)):
            rod = rods[i].toList()
            self.rods_table.setHorizontalHeaderItem(i, QTableWidgetItem(
                str(rods[i].number)))
            for j in range(len(rod)):
                self.rods_table.setItem(i, j, QTableWidgetItem(str(rod[j])))
        self.rods_table.resizeColumnsToContents()


class AddRodForm(QWidget):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.add_button = QPushButton('OK')
        self.add_button.clicked.connect(self.add_rod)
        self.first_node_label = QLabel('Узел 1:')
        self.second_node_label = QLabel('Узел 2:')
        self.first_node_textfield = QLineEdit()
        self.second_node_textfield = QLineEdit()

        box = QVBoxLayout()
        box.addWidget(self.first_node_label)
        box.addWidget(self.first_node_textfield)
        box.addWidget(self.second_node_label)
        box.addWidget(self.second_node_textfield)
        box.addWidget(self.add_button)
        self.setLayout(box)

    def add_rod(self):
        number = rods.__len__() + 1
        first_node = self.first_node_textfield.text()
        first_node = getNode(first_node)
        second_node = self.second_node_textfield.text()
        second_node = getNode(second_node)
        rods.append(Rod(number, first_node, second_node))
        self.menu.update_table()


class LoadsMenu(QWidget):

    def __init__(self):
        super().__init__()
        self.load_index = len(loads)

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_load)

        self.delete_button = QPushButton('Удалить')
        self.delete_button.clicked.connect(self.delete_load)

        self.loads_table = QTableWidget()
        self.loads_table.setColumnCount(2)
        self.loads_table.setHorizontalHeaderLabels(['X', 'Z'])
        self.add_load_form = AddLoadForm(menu=self)

        box = QVBoxLayout()
        box.addWidget(self.add_button)
        box.addWidget(self.delete_button)
        box.addWidget(self.loads_table)
        self.setLayout(box)

    def add_load(self):
        pass

    def delete_load(self):
        pass


class AddLoadForm(QWidget):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.add_button = QPushButton('OK')
        self.add_button.clicked.connect(self.add_load)
        self.x_label = QLabel('X:')
        self.z_label = QLabel('Z:')
        self.x_textfield = QLineEdit()
        self.z_textfield = QLineEdit()

        box = QVBoxLayout()
        box.addWidget(self.x_label)
        box.addWidget(self.x_textfield)
        box.addWidget(self.z_label)
        box.addWidget(self.z_textfield)
        box.addWidget(self.add_button)
        self.setLayout(box)

    def add_load(self):
        number = loads.__len__() + 1
        x = self.x_textfield.text()
        z = self.z_textfield.text()
        loads.append(Load(number, x, z))
        self.menu.update_table()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    starter_menu = MainMenu()
    starter_menu.show()
    sys.exit(app.exec_())
