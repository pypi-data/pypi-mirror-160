""" Модуль для импорта настроек GCore из wdb """
from wdbse import functions


class WDBSE:
    def __init__(self, sql_shell, settings_table_name, sudo_password):
        self.sql_shell = sql_shell
        self.settings_table_name = settings_table_name
        self.sudo_password = sudo_password

    def get_sudo_pass(self):
        """ Вернуть пароль sudo, используемый в GCore"""
        return self.sudo_password
        # return functions.get_sudo_password(self.sql_shell,
        #                                   self.settings_table_name)
