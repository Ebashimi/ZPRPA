# тут переработаны , основной референс находится по этой ссылке: https://b14esh.com/nix/syslog-rsyslog-zabbix/zabbix-api-python-zabbix-host-item.html
from datetime import datetime

# Инициализация
def __init__(self, api):

    self.api = api
    self.users = self.get_users()
    self.version = self.get_version_zabbix()

    # Всё об узлах
    self.uzel = self.get_uszel_zabbix()
    self.uzel_in_group = self.uzel_in_group_zabbix()
    #
    self.host = self.get_host_zabbix()
    self.host = self.host_zabbix()

    self.group = self.get_group_zabbix()



    self.host_in_item = self.host_in_item_zabbix()
    self.problem = self.problem_in_zabbix()
    self.all_problem = self.all_problem_zabbix()
    # Тригеры
    self.trigers = self.trigers_zabbix()
    self.trigers_in_groups = self.trigers_in_groups_zabbix()


# Тригеры в группе
def trigers_in_groups_zabbix(self):

    # Печатаем список групп
    print(f" \nПечатаем список групп:")
    groups = self.api.hostgroup.get(output=['itemid', 'name'])
    for group in groups:
        print(group['groupid'], group['name'])

    # Получаем триггеры группы узлов с groupids = 2
    triggers = self.api.trigger.get(groupids=2, output='extend', expandDescription=1, selectHosts=['host'], )

    # print(f"\n Печатаем все триггеры groupids2 {triggers}")

    print("\n")

    # Печатаем триггеры
    for t in triggers:
        print("{0} - {1} - {2}".format(t['hosts'][0]['host'], t['description'],
                                       datetime.utcfromtimestamp(int(t['lastchange'])).strftime(
                                           '%Y-%m-%d %H:%M:%S')))

# Печатаем все тригеры
def trigers_zabbix(self):

    # Получить список всех проблем (триггеры сработали)
    triggers = self.api.trigger.get(only_true=1,
                                skipDependent=1,
                                monitored=1,
                                active=1,
                                output='extend',
                                expandDescription=1,
                                selectHosts=['host'],
                                )

    # Получить список какие проблемы не подтверждены.
    unack_triggers = self.api.trigger.get(only_true=1,
                                      skipDependent=1,
                                      monitored=1,
                                      active=1,
                                      output='extend',
                                      expandDescription=1,
                                      selectHosts=['host'],
                                      withLastEventUnacknowledged=1,
                                      )

    unack_trigger_ids = [t['triggerid'] for t in unack_triggers]
    for t in triggers:
        t['unacknowledged'] = True if t['triggerid'] in unack_trigger_ids \
            else False

    # Распечатать список, содержащий только "сработавшие" триггеры
    print(f"\n печатаем триггеры")
    for t in triggers:
        if int(t['value']) == 1:
            print("{0} - {1} {2}".format(t['hosts'][0]['host'],
                                         t['description'],
                                         '(Unack)' if t['unacknowledged'] else ''))

# Печатаем проблемы (надо доработать)
def problem_in_zabbix(self):
    ## Получаем все проблемы по хосту тут будет моё
    ## Для получения проблем, которые были решены ранее, используйте event.get метод.
    problems = self.api.problem.get(host='тут будет моё', recent='true')

    ## Если нужно получить все события, включая решенные, используйте event.get
    # events = self.api.event.get(object='problem', host='тут будет моё')

    for pr in problems:
        print("{0} - {1} - {2} ".format(pr['eventid'], pr['name'],
                                          datetime.utcfromtimestamp(int(pr['clock'])).strftime('%Y-%m-%d %H:%M:%S')))


# Получаем итемы из хоста
def host_in_item_zabbix(self):
    # Получаем список item с хоста c id 13395
    print(f" \nПолучаем список item с хоста c id 0")
    items = self.api.item.get(hostids=0, output=['itemid', 'name'])
    for item in items:
        print(item['itemid'], item['name'])

# Печатаем список хостов из группы
def host_zabbix(self):

    print(f" \nПечатаем список групп:")
    groups = self.api.hostgroup.get(output=['itemid', 'name'])
    for group in groups:
        print(group['groupid'], group['name'])

    print(f" \nПолучаем список хостов в группе с id 0")
    hosts = self.api.host.get(groupids=0, output=['hostid', 'name'])
    for host in hosts:
        print(host['hostid'], host['name'])


# Сморим сколько узлов в группе
def uzel_in_group_zabbix(self):

    print(f" \nПечатаем список групп:")
    groups = self.api.hostgroup.get(output=['itemid', 'name'])
    for group in groups:
        print(group['groupid'], group['name'])

    print(f" \nПолучаем список хостов в группе с id 0")
    hosts = self.api.host.get(groupids=0, output=['hostid', 'host', 'name'], selectInterfaces=['ip', 'port', 'dns'])
    for host in hosts:
        print(host ['host'], host ['name'], host ['interfaces']),

# Печатаем список групп
def get_group_zabbix(self):

    print(f" \nПечатаем список групп:")
    groups = self.api.hostgroup.get(output=['itemid', 'name'])
    for group in groups:
        print(group['groupid'], group['name'])

# Печатаем список узлов c параметром host , name , interfaces
def get_uszel_zabbix(self):

    host_and_ip = self.api.host.get(output=['hostid', 'host', 'name'], selectInterfaces=['ip', 'port', 'dns'])

    for i in host_and_ip:
        print(i['host'], i['name'], i['interfaces'])



# Вывод хостов, не красиво
def get_host_zabbix(self):
    result1 = self.api.host.get(monitored_hosts=1, output='extend')

    # Формируем список
    hostnames1 = [host['host'] for host in result1]
    # Если нужно можем распечатать список
    # print(hostnames1)
    # Печатаем список хостов красиво
    for i in hostnames1:
        print(i)

# Узнаем пользователей в Заббикс
def get_users(self):

    try:

        users = self.api.user.get(output=['userid', 'alias'])

        # Выводим список пользователей
        print("Users in Zabbix:")
        for user in users:
            print(f"ID: {user['userid']}, Alias: {user['alias']}")

        return users

    except Exception as e:

        print(f"Failed to retrieve users: {str(e)}")
        return []


# Узнаем Версию Замбикс
def get_version_zabbix(self):

    # Поле версии ZabbixAPI
    ver = self.api.version
    print(type(ver).__name__, ver)  # APIVersion 6.0.24

    # Метод получения версии ZabbixAPI
    ver = self.api.api_version()
    print(type(ver).__name__, ver)  # APIVersion 6.0.24

    # Дополнительные методы работы
    print(ver.major)  # 6.0
    print(ver.minor)  # 24
    print(ver.is_lts())  # True