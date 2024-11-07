# Авторизация
from zabbix_login import ZabbixLoginForm  # Импортируем класс, который делает авторизацию
from PyQt6.QtWidgets import QApplication # Это для интерфейса авторизации
#  Для системы
import sys
# Для расшифровки времени Unix timestamp


# Авторизация в Заббиксе
def authorization_in_zabbix():

    app = QApplication(sys.argv)
    window = ZabbixLoginForm()
    # Подключаем сигнал к функции, которая будет обрабатывать успешный вход
    window.login_successful.connect(on_login_success)
    window.show()
    sys.exit(app.exec())

# Если
def on_login_success(api):
    # Создаем экземпляр Main_Logic и передаем API, выполняем функции которые прописали в Main_Logic
    main_logic = Main_Logic(api)
    # Выходим из акаунта Zabbix
    api.user.logout()


class Main_Logic:

    def __init__(self, api, groupid=None):

        # Инициируем api которое на нужно будет
        self.api = api
        self.groupid = groupid if groupid is not None else input("Введите ID группы: ")
        # С начало нужно узнать сколько у нас групп
        self.group = self.get_group_zabbix()


    # После мы посмотрев какие у нас группы
    def get_group_zabbix(self):

        print(f" \nПечатаем список групп:")
        print("---------------------------------------------------------------------------------------------------------")
        groups = self.api.hostgroup.get(output=['itemid', 'name'])
        for group in groups:
            print(group['groupid'], group['name'])
        print("-------------------------------------------------------------------------------------------------------\n")

    # После выбираем узел с которым мы хотим работать
    def uzel_in_group_zabbix(self):

        print(f" \nПолучаем список хостов в группе с id, которое укажем в переменной")
        hosts = self.api.host.get(groupids=136, output=['hostid', 'host', 'name'],
                                  selectInterfaces=['ip', 'port', 'dns'])
        for host in hosts:
            print(host['host'], host['name'], host['interfaces']),

if __name__ == "__main__":

    authorization_in_zabbix()