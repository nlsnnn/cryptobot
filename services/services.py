def text_subscription(flag):
    return 'активна' if flag else 'неактивна'


def text_users(users):
    string = ''
    for user in users:
        string += f'• {user[1]} - {user[0]}\n'
    return string