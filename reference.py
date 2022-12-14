from datetime import datetime
from num2t4ru import decimal2text
import os
import webbrowser


class ReferenceWithoutMatPom:
    def __init__(self, month_count, worker_name, worker_prof, data, template_path):
        self.month_count = month_count
        self.worker_name = worker_name
        self.worker_prof = worker_prof
        self.data = data
        self.start_index_table = 33
        self.path_to_template = template_path

        self.all_text = self.get_template()

        self.date_number_to_text = {
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

        self.nach = 0
        self.podn = 0
        self.penn = 0
        self.prof = 0
        self.isp = 0
        self.vid = 0
        self.alim = 0

        self.matpom = 0
        self.mat_pom_rozhdenie_rebenka = 0
        self.posob_po_berem_i_rodam = 0
        self.posob_do_3_let = 0
        self.posob_do_18_let = 0
        self.posob_na_rozhdenie = 0
        self.posob_do_12_ned = 0
        self.posob_deti_invalid = 0
        self.isp_list_and_alim = 0



    def num_to_text(self, number):
        int_units = ((u'рубль', u'рубля', u'рублей'), 'm')
        exp_units = ((u'копейка', u'копейки', u'копеек'), 'f')
        return decimal2text(number, int_units=int_units, exp_units=exp_units)

    def get_template(self):
        with open(self.path_to_template, 'r+', encoding="utf8") as file:
            all_text = file.readlines()
            all_text = [i for i in all_text]
            return all_text

    def get_reference_header(self):
        if self.month_count  == "1":
            self.all_text[16] = "<p> за " + self.month_count + " месяц</p>"
        elif self.month_count == "2" or self.month_count == "3" or self.month_count == "4":
            self.all_text[16] = "<p> за " + self.month_count + " месяцa</p>"
        else:
            self.all_text[16] = "<p> за " + self.month_count + " месяцев</p>"

        self.all_text[19] = "<p>гр. " + self.worker_name + "</p>"
        self.all_text[21] = "<p>в качестве: " + self.worker_prof + "</p>"

    def get_reference_body(self):
        for i in self.data[::-1]:
            month = int(datetime.strftime(i[0][0], "%m"))
            year = str(datetime.strftime(i[0][0], "%Y"))

            self.all_text.insert(self.start_index_table, "<tr>")
            self.start_index_table += 1
            self.all_text.insert(self.start_index_table, "<td>" + self.date_number_to_text[str(month)] + " " + year + 'г.' + "</td>")
            self.start_index_table += 1
            self.all_text.insert(self.start_index_table, "<td>" + '%.2f' % float(i[0][1]) + "</td>")
            self.nach += float(i[0][1])
            self.start_index_table += 1
            self.all_text.insert(self.start_index_table, "<td>" + '%.2f' % float(i[0][2]) + "</td>")
            self.start_index_table += 1
            self.podn += float(i[0][2])
            self.all_text.insert(self.start_index_table, "<td>" + '%.2f' % float(i[0][3]) + "</td>")
            self.start_index_table += 1
            self.penn += float(i[0][3])
            self.all_text.insert(self.start_index_table, "<td>" + '%.2f' % float(i[0][6]) + "</td>")
            self.start_index_table += 1
            self.prof += float(i[0][6])
            self.all_text.insert(self.start_index_table, "<td>" + '%.2f' % float(i[0][5]) + "</td>")
            self.start_index_table += 1
            self.isp += float(i[0][5])
            self.all_text.insert(self.start_index_table, "<td>" + '%.2f' % float(i[0][4]) + "</td>")
            self.start_index_table += 1
            self.vid += float(i[0][4])
            self.all_text.insert(self.start_index_table, "</tr>")
            self.start_index_table += 1

    def get_reference_footer(self):
        self.all_text.insert(self.start_index_table, """<tr id="id">""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td  id="id2">Итого:</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td id="id">""" + '%.2f' % self.nach + """</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td id="id">""" + '%.2f' % self.podn + """</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td id="id">""" + '%.2f' % self.penn + """</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td id="id">""" + '%.2f' % self.prof + """</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td id="id">""" + '%.2f' % self.isp + """</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td id="id">""" + '%.2f' % self.vid + """</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, "</tr>")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, "</table>")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, "<table></table>")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<div class="summ"><p>(""" + self.num_to_text(self.vid).upper() + """)</p></div>""")

    def save_and_open_reference(self):
        new_file = open("Spravka.html", 'w+', encoding="utf8")
        for i in self.all_text:
            new_file.write(i + '\n')
        reference_url = os.path.abspath(os.curdir + "/Spravka.html")
        webbrowser.open(reference_url)


class ReferenceNalog(ReferenceWithoutMatPom):
    def get_reference_body(self):
        for i in self.data[::-1]:
            month = int(datetime.strftime(i[0][0], "%m"))
            year = str(datetime.strftime(i[0][0], "%Y"))

            self.all_text.insert(self.start_index_table, "<tr>")
            self.start_index_table += 1
            self.all_text.insert(self.start_index_table, "<td>" + self.date_number_to_text[str(month)] + " " + year + 'г.' + "</td>")
            self.start_index_table += 1
            self.all_text.insert(self.start_index_table, "<td>" + '%.2f' % float(i[0][1]) + "</td>")
            self.nach += float(i[0][1])
            self.start_index_table += 1
            self.all_text.insert(self.start_index_table, "<td>" + '%.2f' % float(i[0][2]) + "</td>")
            self.start_index_table += 1
            self.podn += float(i[0][2])
            self.all_text.insert(self.start_index_table, "<td>" + '%.2f' % float(i[0][3]) + "</td>")
            self.start_index_table += 1
            self.penn += float(i[0][3])
            self.all_text.insert(self.start_index_table, "<td>" + '%.2f' % float(i[0][6]) + "</td>")
            self.start_index_table += 1
            self.prof += float(i[0][6])
            self.all_text.insert(self.start_index_table, "<td>" + '%.2f' % float(i[0][5]) + "</td>")
            self.start_index_table += 1
            self.isp += float(i[0][5])
            self.all_text.insert(self.start_index_table, "<td>" + '%.2f' % float(i[0][7]) + "</td>")
            self.start_index_table += 1
            self.alim += float(i[0][7])
            self.all_text.insert(self.start_index_table, "<td>" + '%.2f' % float(i[0][4]) + "</td>")
            self.start_index_table += 1
            self.vid += float(i[0][4])
            self.all_text.insert(self.start_index_table, "</tr>")
            self.start_index_table += 1

    def get_reference_footer(self):
        self.all_text.insert(self.start_index_table, """<tr id="id">""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td  id="id2">Итого:</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td id="id">""" + '%.2f' % self.nach + """</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td id="id">""" + '%.2f' % self.podn + """</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td id="id">""" + '%.2f' % self.penn + """</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td id="id">""" + '%.2f' % self.prof + """</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td id="id">""" + '%.2f' % self.isp + """</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td id="id">""" + '%.2f' % self.alim + """</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td id="id">""" + '%.2f' % self.vid + """</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, "</tr>")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, "</table>")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, "<table></table>")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<div class="summ"><p>(""" + self.num_to_text(self.vid).upper() + """)</p></div>""")


class ReferencePosob(ReferenceWithoutMatPom):
    def __init__(self, month_count, worker_name, worker_prof, data, template_path):
        super().__init__(month_count, worker_name, worker_prof, data, template_path)
        self.start_index_table = 44

    def get_reference_body(self):
        for i in self.data[::-1]:
            month = int(datetime.strftime(i[0][0], "%m"))
            year = str(datetime.strftime(i[0][0], "%Y"))

            self.all_text.insert(self.start_index_table, "<tr>")
            self.start_index_table += 1
            self.all_text.insert(self.start_index_table, "<td>" + self.date_number_to_text[str(month)] + " " + year + 'г.' + "</td>")
            self.start_index_table += 1
            self.all_text.insert(self.start_index_table, "<td>" + '%.2f' % float(i[0][1]) + "</td>")
            self.nach += float(i[0][1])
            self.start_index_table += 1
            self.all_text.insert(self.start_index_table, "<td>" + '%.2f' % float(i[0][5]) + "</td>")
            self.start_index_table += 1
            self.matpom += float(i[0][5])
            self.all_text.insert(self.start_index_table, "<td>" + '%.2f' % float(i[0][6]) + "</td>")
            self.start_index_table += 1
            self.mat_pom_rozhdenie_rebenka += float(i[0][6])
            self.all_text.insert(self.start_index_table, "<td>" + '%.2f' % float(i[0][8]) + "</td>")
            self.start_index_table += 1
            self.posob_po_berem_i_rodam += float(i[0][8])
            self.all_text.insert(self.start_index_table, "<td>" + '%.2f' % float(i[0][2]) + "</td>")
            self.start_index_table += 1
            self.posob_do_3_let += float(i[0][2])
            self.all_text.insert(self.start_index_table, "<td>" + '%.2f' % float(i[0][3]) + "</td>")
            self.start_index_table += 1
            self.posob_do_18_let += float(i[0][3])
            self.all_text.insert(self.start_index_table, "<td>" + '%.2f' % float(i[0][7]) + "</td>")
            self.start_index_table += 1
            self.posob_na_rozhdenie += float(i[0][7])
            self.all_text.insert(self.start_index_table, "<td>" + '%.2f' % float(i[0][9]) + "</td>")
            self.start_index_table += 1
            self.posob_do_12_ned += float(i[0][9])
            self.all_text.insert(self.start_index_table, "<td>" + '%.2f' % float(i[0][4]) + "</td>")
            self.start_index_table += 1
            self.posob_deti_invalid += float(i[0][4])
            self.all_text.insert(self.start_index_table, "<td>" + '%.2f' % float(i[0][13]) + "</td>")
            self.start_index_table += 1
            self.isp_list_and_alim += float(i[0][13])
            self.all_text.insert(self.start_index_table, "<td>" + '%.2f' % float(i[0][10]) + "</td>")
            self.start_index_table += 1
            self.podn += float(i[0][10])
            self.all_text.insert(self.start_index_table, "<td>" + '%.2f' % float(i[0][11]) + "</td>")
            self.start_index_table += 1
            self.penn += float(i[0][11])
            self.all_text.insert(self.start_index_table, "<td>" + '%.2f' % float(i[0][12]) + "</td>")
            self.start_index_table += 1
            self.prof += float(i[0][12])
            self.all_text.insert(self.start_index_table, "<td>" + '%.2f' % float(i[0][14]) + "</td>")
            self.start_index_table += 1
            self.vid += float(i[0][14])
            self.all_text.insert(self.start_index_table, "</tr>")
            self.start_index_table += 1

    def get_reference_footer(self):
        self.all_text.insert(self.start_index_table, """<tr id="id">""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td  id="id2">Итого:</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td id="id">""" + '%.2f' % self.nach + """</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td id="id">""" + '%.2f' % self.matpom + """</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td id="id">""" + '%.2f' % self.mat_pom_rozhdenie_rebenka + """</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td id="id">""" + '%.2f' % self.posob_po_berem_i_rodam + """</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td id="id">""" + '%.2f' % self.posob_do_3_let + """</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td id="id">""" + '%.2f' % self.posob_do_18_let + """</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td id="id">""" + '%.2f' % self.posob_na_rozhdenie + """</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td id="id">""" + '%.2f' % self.posob_do_12_ned + """</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td id="id">""" + '%.2f' % self.posob_deti_invalid + """</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td id="id">""" + '%.2f' % self.isp_list_and_alim + """</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td id="id">""" + '%.2f' % self.podn + """</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td id="id">""" + '%.2f' % self.penn + """</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td id="id">""" + '%.2f' % self.prof + """</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<td id="id">""" + '%.2f' % self.vid + """</td>""")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, "</tr>")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, "</table>")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, "<table></table>")
        self.start_index_table += 1
        self.all_text.insert(self.start_index_table, """<div class="summ"><p>(""" + self.num_to_text(self.vid).upper() + """)</p></div>""")





