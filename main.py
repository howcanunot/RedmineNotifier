from SQLHelper import SQLHelper
from bot import start


def main():
    _ = start()
    sql_helper = SQLHelper('database.sqlite')

    users = sql_helper.get_users()

    for user in users:
        user.bind_user_issues()

    while True:
        for user in users:
            user.check_changed_issues()
            user.check_new_issues()


if __name__ == '__main__':
    main()
