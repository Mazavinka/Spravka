import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore

from interface import Ui_MainWindow
from PyQt5.QtWidgets import QCompleter
from datetime import datetime
from dateutil.relativedelta import relativedelta
from db import singleton_db
from reference import ReferenceNalog, ReferenceWithoutMatPom, ReferencePosob


class GetRef:
    def __init__(self, kpodr, d, tn, dis, flag_mat_pom):
        self.kpodr = kpodr
        self.d = d
        self.tn = tn
        self.dis = dis
        self.flag_mat_pom = flag_mat_pom
        self.cursor = singleton_db

    def get_posob(self):
        self.cursor.execute("EXECUTE PROCEDURE GETPOSREZ('{0}','{1}','{2}', '{3}')".format(self.kpodr, self.d, self.tn, self.dis))
        data = self.cursor.fetchall()
        return data

    def get_data(self):
        self.cursor.execute("EXECUTE PROCEDURE GETNALREZ('{0}', '{1}', '{2}', '{3}', '{4}')".format(self.kpodr, self.d, self.tn, self.dis, self.flag_mat_pom))
        data = self.cursor.fetchall()
        return data

    def get_employee(self):
        self.cursor.execute("SELECT k.FAM, k.tn, k.kpodr, p.nprof from kartochka k, prof p where k.kprof=p.kprof")
        all_employee = self.cursor.fetchall()
        self.all_employers = {'data': []}
        id = 1
        for i in all_employee:
            temp = {'id': str(id),
                    'fam': i[0],
                    'tn': i[1],
                    'kpodr': str(i[2]),
                    'prof': str(i[3]),
                    }
            self.all_employers['data'].append(temp)
            id += 1
        return self.all_employers


class Interface:
    def __init__(self):
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow)
        self.mat_pom_flag = 0
        #корявый метод для вызова экземпляра класса
        self.all_employers = GetRef(259, '01.10.2022', 24110, 1, self.mat_pom_flag).get_employee()

        self.ui.comboBox_2.addItem('')
        for i in self.all_employers['data']:
            self.ui.comboBox_2.addItem(i['fam'] + ' | ' + i['id'])
            self.ui.comboBox_2.setItemData(int(i['id']), 'Профессия: ' + i['prof'], QtCore.Qt.ToolTipRole)
            """if i['fam'].lower() != 'пту' and i['fam'].lower() != 'гпту':
                self.ui.comboBox_2.addItem(i['fam'] + ' | ' + i['id'])"""

        self.ui.comboBox_2.currentIndexChanged.connect(self.check_employee)

        self.ui.comboBox_2.setEditable(True)
        self.ui.comboBox_2.completer().setCompletionMode(QCompleter.PopupCompletion)

        all_buh = ['Хлебчик М.В', 'Хаменок Ю.В', 'Романович С.А', 'Познякова В.М', 'Бут Е.В']
        self.ui.comboBox_5.addItems(all_buh)
        self.ui.comboBox_3.addItems(all_buh)

        self.ui.pushButton_2.clicked.connect(self.on_click)

        MainWindow.show()
        sys.exit(app.exec_())

    def check_employee(self):
        current_employee = self.ui.comboBox_2.currentText()
        if current_employee != '':
            employee_id = current_employee.split(' | ')[1]
            for i in self.all_employers['data']:
                if i['id'] == employee_id:
                    self.selected_employe = i
                    print(self.selected_employe)

    def get_all_date(self):
        get_date_from_cb = '01.' + self.ui.dateEdit_3.text()
        get_month_count_from_cb = self.ui.spinBox_2.value()
        result = []
        result.append(get_date_from_cb)
        date = datetime.strptime(get_date_from_cb, "%d.%m.%Y")
        while get_month_count_from_cb > 1:
            date = date + relativedelta(months=-1)
            result.append(date.strftime("%d.%m.%Y"))
            get_month_count_from_cb -= 1

        return result

    def flag_mat_pom(self):
        if self.ui.radioButton_6.isChecked():
            self.mat_pom_flag = 1
        elif self.ui.radioButton_5.isChecked():
            self.mat_pom_flag = 0
        print(self.mat_pom_flag)

    def on_click(self):
        self.flag_mat_pom()
        all_month = self.get_all_date()
        self.result = []
        for i in all_month:
            if self.ui.radioButton_4.isChecked():
                self.result.append(GetRef(self.selected_employe['kpodr'], i, self.selected_employe['tn'], 1, self.mat_pom_flag).get_posob())
            else:
                self.result.append(GetRef(self.selected_employe['kpodr'], i, self.selected_employe['tn'], 1, self.mat_pom_flag).get_data())
        for i in self.result:
            print(i)

        if self.ui.radioButton_6.isChecked():
            # Без материальной помощи
            reference = ReferenceWithoutMatPom(self.ui.spinBox_2.text(), self.selected_employe['fam'], self.selected_employe['prof'], self.result, "templates/matpom2.html")
            reference.get_reference_header()
            reference.get_reference_body()
            reference.get_reference_footer()
            reference.save_and_open_reference()
        if self.ui.radioButton_5.isChecked():
            # Налоговые отчисления
            reference = ReferenceNalog(self.ui.spinBox_2.text(), self.selected_employe['fam'], self.selected_employe['prof'], self.result, "templates/nalog.html")
            reference.get_reference_header()
            reference.get_reference_body()
            reference.get_reference_footer()
            reference.save_and_open_reference()
        if self.ui.radioButton_4.isChecked():
            # Пособия
            reference = ReferencePosob(self.ui.spinBox_2.text(), self.selected_employe['fam'], self.selected_employe['prof'], self.result, "templates/posob.html")
            reference.get_reference_header()
            reference.get_reference_body()
            reference.get_reference_footer()
            reference.save_and_open_reference()


if __name__ == "__main__":
    a = Interface()
    """app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())"""