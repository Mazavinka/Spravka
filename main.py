import fdb
import sys
from PyQt5 import QtWidgets
from interface import Ui_MainWindow
from PyQt5.QtWidgets import QCompleter
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import os
import webbrowser
from num2t4ru import decimal2text

con = fdb.connect(dsn='asup5:D:Master\Data\BUHDATA.GDB', user='sysdba',
                  password='masterkey')

cur = con.cursor()

#cur.execute("SELECT SUM(R.SUMMA) FROM UV_REZNACH R, NACHISL N WHERE KPODR=91 AND r.ndate='01.09.2022' AND TN=24039 AND R.NCODE=N.NCODE and N.PENCODE<>205")
#cur.execute("EXECUTE PROCEDURE GETNALREZ('259', '01.10.2022', '24110', '1', '0')")
#cur.execute("EXECUTE PROCEDURE GETPOSREZ(205,'01.10.2022',22795, 2)")

class GetRef:
    def __init__(self, kpodr, d, tn, dis, flag_mat_pom):
        self.kpodr = kpodr
        self.d = d
        self.tn = tn
        self.dis = dis
        self.flag_mat_pom = flag_mat_pom

    def get_posob(self):
        cur.execute("EXECUTE PROCEDURE GETPOSREZ(205,'01.10.2022',22795, 2)")
        data = cur.fetchall()
        return data

    def get_data(self):
        cur.execute("EXECUTE PROCEDURE GETNALREZ('{0}', '{1}', '{2}', '{3}', '{4}')".format(self.kpodr, self.d, self.tn, self.dis, self.flag_mat_pom))
        data = cur.fetchall()
        return data

    def get_prof(self, tn):
        cur.execute("select p.NPROF from kartochka k, prof p where k.kprof=p.KPROF and tn='{0}'".format(tn))
        result = cur.fetchall()
        return result


    def get_employee(self):
        cur.execute("SELECT k.FAM, k.tn, k.kpodr from KARTOCHKA k")
        all_employee = cur.fetchall()
        self.all_employers = {'data': []}
        id = 1
        for i in all_employee:
            employee_prof = str(self.get_prof(i[1])[0][0])
            a = {'id': str(id), 'fam': i[0], 'tn': i[1], 'kpodr': str(i[2]), 'prof': employee_prof}
            self.all_employers['data'].append(a)
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
            if i['fam'].lower() != 'пту' and i['fam'].lower() != 'гпту':
                self.ui.comboBox_2.addItem(i['fam'] + ' | ' + i['id'])

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
            self.get_spravka()
        if self.ui.radioButton_5.isChecked():
            self.get_nalog_spravka()

    def get_nalog_spravka(self):
        with open('templates/nalog.html', 'r+', encoding="utf8") as file:
            all_text = file.readlines()
            all_text = [i for i in all_text]

            if self.ui.spinBox_2.text() == "1":
                all_text[16] = "<p> за " + self.ui.spinBox_2.text() + " месяц</p>"
            elif self.ui.spinBox_2.text() == "2" or self.ui.spinBox_2.text() == "3" or self.ui.spinBox_2.text() == "4":
                all_text[16] = "<p> за " + self.ui.spinBox_2.text() + " месяцa</p>"
            else:
                all_text[16] = "<p> за " + self.ui.spinBox_2.text() + " месяцев</p>"

            all_text[19] = "<p>гр. " + self.selected_employe['fam'] + "</p>"
            all_text[21] = "<p>в качестве: " + self.selected_employe['prof'] +"</p>"


            start_index_table = 33

            date_number_to_text = {
                '1': 'Январь',
                '2': 'Февраль',
                '3': 'Март',
                '4': 'Апрель',
                '5': 'Май',
                '6': 'Июнь',
                '7': 'Июль',
                '8': 'Август',
                '9': 'Сентябрь',
                '10': 'Октябрь',
                '11': 'Ноябрь',
                '12': 'Декабрь'
            }

            nach = 0
            podn = 0
            penn = 0
            prof = 0
            isp = 0
            vid = 0
            alim = 0

            for i in self.result[::-1]:
                month = int(datetime.strftime(i[0][0], "%m"))
                year = str(datetime.strftime(i[0][0], "%Y"))

                all_text.insert(start_index_table, "<tr>")
                start_index_table += 1
                all_text.insert(start_index_table, "<td>" + date_number_to_text[str(month)] + " " + year + 'г.' + "</td>")
                start_index_table += 1
                all_text.insert(start_index_table, "<td>" + '%.2f' % float(i[0][1]) + "</td>")
                nach += float(i[0][1])
                start_index_table += 1
                all_text.insert(start_index_table, "<td>" + '%.2f' % float(i[0][2]) + "</td>")
                start_index_table += 1
                podn += float(i[0][2])
                all_text.insert(start_index_table, "<td>" + '%.2f' % float(i[0][3]) + "</td>")
                start_index_table += 1
                penn += float(i[0][3])
                all_text.insert(start_index_table, "<td>" + '%.2f' % float(i[0][6]) + "</td>")
                start_index_table += 1
                prof += float(i[0][6])
                all_text.insert(start_index_table, "<td>" + '%.2f' % float(i[0][5]) + "</td>")
                start_index_table += 1
                isp += float(i[0][5])
                all_text.insert(start_index_table, "<td>" + '%.2f' % float(i[0][7]) +"</td>")
                start_index_table += 1
                alim += float(i[0][7])
                all_text.insert(start_index_table, "<td>" + '%.2f' % float(i[0][4]) +"</td>")
                start_index_table += 1
                vid += float(i[0][4])
                all_text.insert(start_index_table, "</tr>")
                start_index_table += 1

            all_text.insert(start_index_table, """<tr id="id">""")
            start_index_table += 1
            all_text.insert(start_index_table, """<td  id="id2">Итого:</td>""")
            start_index_table += 1
            all_text.insert(start_index_table, """<td id="id">""" + '%.2f' % nach + """</td>""")
            start_index_table += 1
            all_text.insert(start_index_table, """<td id="id">""" + '%.2f' % podn + """</td>""")
            start_index_table += 1
            all_text.insert(start_index_table, """<td id="id">""" + '%.2f' % penn + """</td>""")
            start_index_table += 1
            all_text.insert(start_index_table, """<td id="id">""" + '%.2f' % prof + """</td>""")
            start_index_table += 1
            all_text.insert(start_index_table, """<td id="id">""" + '%.2f' % isp + """</td>""")
            start_index_table += 1
            all_text.insert(start_index_table, """<td id="id">""" + '%.2f' % alim + """</td>""")
            start_index_table += 1
            all_text.insert(start_index_table, """<td id="id">""" + '%.2f' % vid + """</td>""")
            start_index_table += 1
            all_text.insert(start_index_table, "</tr>")
            start_index_table += 1
            all_text.insert(start_index_table, "</table>")
            start_index_table += 1
            all_text.insert(start_index_table, "<table></table>")
            start_index_table += 1
            all_text.insert(start_index_table, """<div class="summ"><p>(""" + self.num_to_text(vid).upper() +""")</p></div>""")



            new_file = open("Spravka.html", 'w+', encoding="utf8")
            for i in all_text:
                new_file.write(i + '\n')

        spravka_url = os.path.abspath(os.curdir + "/Spravka.html")
        webbrowser.open(spravka_url)

    def get_spravka(self):
        with open('templates/matpom2.html', 'r+', encoding="utf8") as file:
            all_text = file.readlines()
            all_text = [i for i in all_text]

            if self.ui.spinBox_2.text() == "1":
                all_text[16] = "<p> за " + self.ui.spinBox_2.text() + " месяц</p>"
            elif self.ui.spinBox_2.text() == "2" or self.ui.spinBox_2.text() == "3" or self.ui.spinBox_2.text() == "4":
                all_text[16] = "<p> за " + self.ui.spinBox_2.text() + " месяцa</p>"
            else:
                all_text[16] = "<p> за " + self.ui.spinBox_2.text() + " месяцев</p>"

            all_text[19] = "<p>гр. " + self.selected_employe['fam'] + "</p>"
            all_text[21] = "<p>в качестве: " + self.selected_employe['prof'] +"</p>"


            start_index_table = 33

            date_number_to_text = {
                '1': 'Январь',
                '2': 'Февраль',
                '3': 'Март',
                '4': 'Апрель',
                '5': 'Май',
                '6': 'Июнь',
                '7': 'Июль',
                '8': 'Август',
                '9': 'Сентябрь',
                '10': 'Октябрь',
                '11': 'Ноябрь',
                '12': 'Декабрь'
            }

            nach = 0
            podn = 0
            penn = 0
            prof = 0
            isp = 0
            vid = 0

            for i in self.result[::-1]:
                month = int(datetime.strftime(i[0][0], "%m"))
                year = str(datetime.strftime(i[0][0], "%Y"))

                all_text.insert(start_index_table, "<tr>")
                start_index_table += 1
                all_text.insert(start_index_table, "<td>" + date_number_to_text[str(month)] + " " + year + 'г.' + "</td>")
                start_index_table += 1
                all_text.insert(start_index_table, "<td>" + '%.2f' % float(i[0][1]) + "</td>")
                nach += float(i[0][1])
                start_index_table += 1
                all_text.insert(start_index_table, "<td>" + '%.2f' % float(i[0][2]) + "</td>")
                start_index_table += 1
                podn += float(i[0][2])
                all_text.insert(start_index_table, "<td>" + '%.2f' % float(i[0][3]) + "</td>")
                start_index_table += 1
                penn += float(i[0][3])
                all_text.insert(start_index_table, "<td>" + '%.2f' % float(i[0][6]) + "</td>")
                start_index_table += 1
                prof += float(i[0][6])
                all_text.insert(start_index_table, "<td>" + '%.2f' % float(i[0][5]) + "</td>")
                start_index_table += 1
                isp += float(i[0][5])
                all_text.insert(start_index_table, "<td>" + '%.2f' % float(i[0][4]) +"</td>")
                start_index_table += 1
                vid += float(i[0][4])
                all_text.insert(start_index_table, "</tr>")
                start_index_table += 1

            all_text.insert(start_index_table, """<tr id="id">""")
            start_index_table += 1
            all_text.insert(start_index_table, """<td  id="id2">Итого:</td>""")
            start_index_table += 1
            all_text.insert(start_index_table, """<td id="id">""" + '%.2f' % nach + """</td>""")
            start_index_table += 1
            all_text.insert(start_index_table, """<td id="id">""" + '%.2f' % podn + """</td>""")
            start_index_table += 1
            all_text.insert(start_index_table, """<td id="id">""" + '%.2f' % penn + """</td>""")
            start_index_table += 1
            all_text.insert(start_index_table, """<td id="id">""" + '%.2f' % prof + """</td>""")
            start_index_table += 1
            all_text.insert(start_index_table, """<td id="id">""" + '%.2f' % isp + """</td>""")
            start_index_table += 1
            all_text.insert(start_index_table, """<td id="id">""" + '%.2f' % vid + """</td>""")
            start_index_table += 1
            all_text.insert(start_index_table, "</tr>")
            start_index_table += 1
            all_text.insert(start_index_table, "</table>")
            start_index_table += 1
            all_text.insert(start_index_table, "<table></table>")
            start_index_table += 1
            all_text.insert(start_index_table, """<div class="summ"><p>(""" + self.num_to_text(vid).upper() +""")</p></div>""")



            new_file = open("Spravka.html", 'w+', encoding="utf8")
            for i in all_text:
                new_file.write(i + '\n')

        spravka_url = os.path.abspath(os.curdir + "/Spravka.html")
        webbrowser.open(spravka_url)

    def num_to_text(self, num):
        int_units = ((u'рубль', u'рубля', u'рублей'), 'm')
        exp_units = ((u'копейка', u'копейки', u'копеек'), 'f')

        return decimal2text(num, int_units=int_units,exp_units=exp_units)


if __name__ == "__main__":
    a = Interface()
    """app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())"""

#https://tokmakov.msk.ru/blog/item/78