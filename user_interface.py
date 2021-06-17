import sys
from data_models import Node, Rod, Load, nodes, rods, loads, MathClass, results
from PyQt5.QtWidgets import QWidget, QApplication, QCheckBox, QVBoxLayout, \
    QPushButton, QTableWidget, QLabel, QLineEdit, QTableWidgetItem, \
    QTabWidget, QComboBox
from PyQt5.Qt import QIntValidator

def load_test():
    nodes.append(Node(1,0,0, True, True))
    nodes.append(Node(2,4,0,False,False))
    nodes.append(Node(3, 8, 0, False, True))
    nodes.append(Node(4, 4, 3, False, False))
    rods.append(Rod(1, nodes[0], nodes[1], 100))
    rods.append(Rod(2, nodes[1], nodes[2], 100))
    rods.append(Rod(3, nodes[0], nodes[3], 100))
    rods.append(Rod(4, nodes[2], nodes[3], 100))
    rods.append(Rod(5, nodes[1], nodes[3], 100))
    loads.append(Load(1, nodes[1], 0, -280))
    loads.append(Load(2, nodes[3], 380, 0))

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
        self.calculate_button.clicked.connect(self.show_result)
        self.result_window = ResultWindow()

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.tab_bar)
        self.main_layout.addWidget(self.calculate_button)
        self.setLayout(self.main_layout)

    def show_result(self):
        self.result_window.show()


class NodeMenu(QWidget):

    def __init__(self):
        super().__init__()
        self.node_index = len(nodes)

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_node)

        self.delete_button = QPushButton('Удалить')
        self.delete_button.clicked.connect(self.delete_node)
        self.delete_button.setEnabled(False)

        self.nodes_table = QTableWidget()
        self.nodes_table.setColumnCount(4)
        self.nodes_table.setHorizontalHeaderLabels(['X', 'Y', 'Связь по X',
                                                    'Связь по Y'])
        self.add_node_form = AddNodeForm(menu=self)

        box = QVBoxLayout()
        box.addWidget(self.add_button)
        box.addWidget(self.delete_button)
        box.addWidget(self.nodes_table)
        self.setLayout(box)
        self.update_table()

    def add_node(self):
        self.add_node_form.show()

    def delete_node(self):
        nodes.pop(self.nodes_table.currentRow())
        self.update_table()

    def changeEvent(self, *args, **kwargs):
        if self.node_index != len(nodes):
            self.update_table()

    def update_table(self):
        self.nodes_table.setRowCount(len(nodes))
        for i in range(len(nodes)):
            node = nodes[i].toList()
            self.nodes_table.setVerticalHeaderItem(i, QTableWidgetItem(
                str(nodes[i].number)))
            for j in range(len(node)):
                self.nodes_table.setItem(i, j, QTableWidgetItem(str(node[j])))
        if len(nodes) == 0:
            self.delete_button.setEnabled(False)
        else:
            self.delete_button.setEnabled(True)
        self.nodes_table.resizeColumnsToContents()


class AddNodeForm(QWidget):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.add_button = QPushButton('OK')
        self.add_button.clicked.connect(self.add_node)
        self.x_label = QLabel('X:')
        self.y_label = QLabel('Y:')
        self.x_textfield = QLineEdit('0')
        self.x_textfield.setValidator(QIntValidator())
        self.y_textfield = QLineEdit('0')
        self.y_textfield.setValidator(QIntValidator())
        self.connection_label = QLabel('Связи:')
        self.x_checkbox = QCheckBox('X')
        self.y_checkbox = QCheckBox('Y')

        box = QVBoxLayout()
        box.addWidget(self.x_label)
        box.addWidget(self.x_textfield)
        box.addWidget(self.y_label)
        box.addWidget(self.y_textfield)
        box.addWidget(self.connection_label)
        box.addWidget(self.x_checkbox)
        box.addWidget(self.y_checkbox)
        box.addWidget(self.add_button)
        self.setLayout(box)

    def add_node(self):
        number = nodes.__len__() + 1
        x = int(self.x_textfield.text())
        y = int(self.y_textfield.text())
        x_connection = self.x_checkbox.isChecked()
        y_connection = self.y_checkbox.isChecked()
        for node in nodes:
            if (node.y == y) and (node.x == x):
                return
        nodes.append(Node(number, x, y, x_connection, y_connection))
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
        self.delete_button.setEnabled(False)

        self.rods_table = QTableWidget()
        self.rods_table.setColumnCount(3)
        self.rods_table.setHorizontalHeaderLabels(['Узел 1', 'Узел 2', 'EI'])

        box = QVBoxLayout()
        box.addWidget(self.add_button)
        box.addWidget(self.delete_button)
        box.addWidget(self.rods_table)
        self.setLayout(box)
        self.update_table()

    def add_rod(self):
        self.add_rod_form.show()

    def delete_rod(self):
        rods.pop(self.rods_table.currentRow())
        self.update_table()

    def showEvent(self, *args, **kwargs) -> None:
        if nodes.__len__() == 0:
            self.add_button.setEnabled(False)
        else:
            self.add_button.setEnabled(True)

    def changeEvent(self, *args, **kwargs):
        if self.rod_index != len(rods):
            self.update_table()

    def update_table(self):
        self.rods_table.setRowCount(len(rods))
        for i in range(len(rods)):
            rod = rods[i].toList()
            self.rods_table.setVerticalHeaderItem(i, QTableWidgetItem(
                str(rods[i].number)))
            for j in range(len(rod)):
                self.rods_table.setItem(i, j, QTableWidgetItem(str(rod[j])))
        if len(rods) == 0:
            self.delete_button.setEnabled(False)
        else:
            self.delete_button.setEnabled(True)
        self.rods_table.resizeColumnsToContents()


class AddRodForm(QWidget):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.add_button = QPushButton('OK')
        self.add_button.clicked.connect(self.add_rod)
        self.first_node_label = QLabel('Узел 1:')
        self.second_node_label = QLabel('Узел 2:')
        self.cb = QComboBox()
        self.node_index = nodes.__len__()
        self.first_node_cb = QComboBox()
        self.second_node_cb = QComboBox()
        self.EI_label = QLabel('Жесткостные хар-ки(EI):')
        self.EI_text_field = QLineEdit()
        self.EI_text_field.setValidator(QIntValidator())
        box = QVBoxLayout()
        box.addWidget(self.first_node_label)
        box.addWidget(self.first_node_cb)
        box.addWidget(self.second_node_label)
        box.addWidget(self.second_node_cb)
        box.addWidget(self.EI_label)
        box.addWidget(self.EI_text_field)
        box.addWidget(self.add_button)
        self.setLayout(box)

    def add_rod(self):
        number = rods.__len__() + 1
        first_node = self.first_node_cb.currentIndex()
        second_node = self.second_node_cb.currentIndex()
        EI = int(self.EI_text_field.text())

        rods.append(Rod(number, nodes[first_node], nodes[second_node], EI))
        self.menu.update_table()

    def changeEvent(self, *args, **kwargs):
        if nodes.__len__() == 0:
            self.add_button.setEnabled(False)
        else:
            self.add_button.setEnabled(True)
        if self.node_index != nodes.__len__():
            for node in nodes:
                self.first_node_cb.addItem(str(node.number))
                self.second_node_cb.addItem(str(node.number))


class LoadsMenu(QWidget):

    def __init__(self):
        super().__init__()
        self.load_index = len(loads)

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_load)

        self.delete_button = QPushButton('Удалить')
        self.delete_button.clicked.connect(self.delete_load)
        self.delete_button.setEnabled(False)

        self.loads_table = QTableWidget()
        self.loads_table.setColumnCount(3)
        self.loads_table.setHorizontalHeaderLabels(['Узел', 'X', 'Y'])
        self.add_load_form = AddLoadForm(menu=self)

        box = QVBoxLayout()
        box.addWidget(self.add_button)
        box.addWidget(self.delete_button)
        box.addWidget(self.loads_table)
        self.setLayout(box)
        self.update_table()

    def add_load(self):
        self.add_load_form.show()

    def delete_load(self):
        loads.pop(self.loads_table.currentRow())
        self.update_table()

    def showEvent(self, *args, **kwargs) -> None:
        if nodes.__len__() == 0:
            self.add_button.setEnabled(False)
        else:
            self.add_button.setEnabled(True)

    def changeEvent(self, *args, **kwargs):
        if self.load_index != len(loads):
            self.update_table()

    def update_table(self):
        self.loads_table.setRowCount(len(loads))
        for i in range(len(loads)):
            load = loads[i].toList()
            self.loads_table.setVerticalHeaderItem(i, QTableWidgetItem(
                str(loads[i].number)))
            for j in range(len(load)):
                self.loads_table.setItem(i, j, QTableWidgetItem(str(load[j])))
        if len(loads) == 0:
            self.delete_button.setEnabled(False)
        else:
            self.delete_button.setEnabled(True)
        self.loads_table.resizeColumnsToContents()


class AddLoadForm(QWidget):
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        self.add_button = QPushButton('OK')
        self.add_button.clicked.connect(self.add_load)
        self.node_label = QLabel('Узел:')
        self.x_label = QLabel('X:')
        self.y_label = QLabel('Y:')
        self.x_textfield = QLineEdit('0')
        self.x_textfield.setValidator(QIntValidator())
        self.y_textfield = QLineEdit('0')
        self.y_textfield.setValidator(QIntValidator())
        self.node_index = nodes.__len__()

        self.node_cb = QComboBox()

        box = QVBoxLayout()
        box.addWidget(self.node_label)
        box.addWidget(self.node_cb)
        box.addWidget(self.x_label)
        box.addWidget(self.x_textfield)
        box.addWidget(self.y_label)
        box.addWidget(self.y_textfield)
        box.addWidget(self.add_button)
        self.setLayout(box)

    def add_load(self):
        number = loads.__len__() + 1
        node = self.node_cb.currentIndex()
        x = int(self.x_textfield.text())
        y = int(self.y_textfield.text())
        loads.append(Load(number, nodes[node], x, y))
        self.menu.update_table()

    def changeEvent(self, *args, **kwargs):
        if self.node_index != nodes.__len__():
            for node in nodes:
                self.node_cb.addItem(str(node.number))


class ResultWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.next_button = QPushButton('')
        self.back_button = QPushButton('Назад')

        self.setWindowTitle('Результаты расчета')
        self.setMinimumSize(800, 600)

        self.tab_bar = QTabWidget()
        self.geometry_menu = GeometryMenu()
        self.separate_matrix_menu = SeparateMatrixMenu()
        self.full_matrix_menu = FullMatrixMenu()
        self.result_menu = ResultMenu()
        self.tab_bar.addTab(self.geometry_menu, 'Геометрические параметры')
        self.tab_bar.addTab(self.separate_matrix_menu, 'Матрицы жесткости '
                                                       'элементов')
        self.tab_bar.addTab(self.full_matrix_menu, 'Общая матрица жесткости')
        self.tab_bar.addTab(self.result_menu, 'Результаты расчетов')

        box = QVBoxLayout()
        box.addWidget(self.tab_bar)
        box.addWidget(self.next_button)
        box.addWidget(self.back_button)
        self.setLayout(box)


class GeometryMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.rod_index = rods.__len__()
        self.data_table = QTableWidget()
        self.data_table.setRowCount(6)
        self.data_table.setColumnCount(1)
        self.data_table.setVerticalHeaderLabels(['L', 'COS', 'SIN',
                                                 'COS2',
                                                 'SIN2', 'COS*SIN'])

        box = QVBoxLayout()
        box.addWidget(self.data_table)
        self.setLayout(box)
        self.update_data_table()

    def showEvent(self, *args, **kwargs):
        if self.rod_index != len(rods):
            self.update_data_table()

    def update_data_table(self):
        self.data_table.setColumnCount(rods.__len__())
        for i in range(len(rods)):
            rod = rods[i].toShow()
            self.data_table.setHorizontalHeaderItem(i, QTableWidgetItem(
                str(rods[i].number)))
            for j in range(len(rod)):
                self.data_table.setItem(j, i, QTableWidgetItem(str(rod[j])))
        self.data_table.resizeColumnsToContents()


class SeparateMatrixMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.tab_bar = QTabWidget()

        box = QVBoxLayout()
        box.addWidget(self.tab_bar)
        self.setLayout(box)

    def showEvent(self, *args, **kwargs):
        self.tab_bar.clear()
        for rod in rods:
            self.tab_bar.addTab(SeparateMatrixTable(rod.separate_matrix),
                                rod.name)


class SeparateMatrixTable(QTableWidget):
    def __init__(self, data):
        super().__init__()
        self.verticalHeader().hide()
        self.horizontalHeader().hide()
        self.setColumnCount(4)
        self.setRowCount(4)
        for i in range(4):
            for j in range(4):
                self.setItem(i, j, QTableWidgetItem(str(data[i][j])))


class FullMatrixMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.data_table = QTableWidget()
        self.data_table.verticalHeader().hide()
        self.data_table.horizontalHeader().hide()

        box = QVBoxLayout()
        box.addWidget(self.data_table)
        self.setLayout(box)

    def showEvent(self, *args, **kwargs):
        self.data_table.clear()
        matrix_states = nodes.__len__()*2
        self.data_table.setColumnCount(matrix_states)
        self.data_table.setRowCount(matrix_states)
        self.maths = MathClass(nodes, rods, loads)
        data = self.maths.matrix
        for i in range(matrix_states):
            for j in range(matrix_states):
                self.data_table.setItem(i, j, QTableWidgetItem(str(data[i][j])))


class ResultMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.data_table = QTableWidget()

        box = QVBoxLayout()
        box.addWidget(self.data_table)
        self.setLayout(box)

    def update_data_table(self):
        self.data_table.setColumnCount(2)
        self.data_table.setHorizontalHeaderLabels(['R', 'N'])

    # def get_pillar_reaction(self):
    #     k = 0
    #     for node in nodes():
    #         if node.z_connection:
    #             k += 1
    #         if node.x_connection:
    #             k += 1
    #     return k


if __name__ == '__main__':
    app = QApplication(sys.argv)
    load_test()
    starter_menu = MainMenu()
    starter_menu.show()
    sys.exit(app.exec_())
