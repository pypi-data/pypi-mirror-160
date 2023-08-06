def get_sudo_password(sql_shell, settings_table_name):
    response = get_data(sql_shell, settings_table_name, 'sudo_password')
    parsed = parse_reponse(response)
    return parsed


def parse_reponse(response):
    """ Обрабтывает ответ от get_data"""
    return response['value']


def get_data(sql_shell, settings_table_name, key, value_column='value', key_column='key', *args, **kwargs):
    command = "SELECT {} FROM {} WHERE {}='{}'".format(value_column, settings_table_name, key_column, key)
    response = sql_shell.get_table_dict(command)
    if response['status'] == 'success':
        return response['info'][0]
    else:
        return response
