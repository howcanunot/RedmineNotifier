import sqlite3
from user import User


class SQLHelper:

    """
    Class provides easy way to work with sqlite database.
    """
    def __init__(self, name):
        self.__connection = sqlite3.connect(name)

    def init(self):
        pass

    def get_users(self, user_id=None, telegram_id=None):
        """ Return list of users from User Table. """

        users = []
        sql_query_get_all = 'SELECT * FROM User'

        try:
            with self.__connection:
                cursor = self.__connection.cursor()
                for row in cursor.execute(sql_query_get_all).fetchall():
                    users.append(User.create_user(row))
        except Exception as exception:
            print('Exception: {}'.format(exception))

        return users

    def __get_issues_from_df(self):
        """ Returns list of issues_id(from redmine) for all issue in Issue table. """

        result = []
        sql_query = 'SELECT redmine_issue_id FROM Issue'

        try:
            cursor = self.__connection.cursor()
            cursor.execute(sql_query)
            data = cursor.fetchone()
            for value in data:
                result.append(value[0])     # WHY append value[0]??? value - string or another collection?
        except Exception as exception:
            print('Exception: {}'.format(exception))

        return result

    def __get_user_map(self):
        """ Returns dictionary with items: user id in redmine -> user id in User table. """

        user_dict = {}
        for user in self.get_users():
            redmine_user_id = user[1]
            user_id = user[0]           # What mean user_id in User Table???
            if redmine_user_id not in user_dict:
                user_dict[redmine_user_id] = user_id

        return user_dict

    def get_issues(self):
        """ Returns list of issues from Issue table. """

        result = []
        sql_query = 'SELECT * FROM Issue'
        try:
            cursor = self.__connection.cursor()
            cursor.execute(sql_query)
            result = cursor.fetchone()
        except Exception as exception:
            print('Exception: %s' % exception)

        return result

    def put_issues(self, local_issues):
        """
        Update assigned_to, update_on, status_id, status_name, description for all issues from Issue table.
        :param local_issues: issues from database.     """

        sql_query = "UPDATE Issue SET assigned_to=?, updated_on=?, status_id=?, status_name=?, description=? WHERE id=?"
        try:
            cur = self.__connection.cursor()
            for issue in local_issues:
                # updated_on = datetime.datetime.strptime(issue[3], '%Y-%m-%d %H:%M:%S')
                cur.execute(sql_query, (issue[2], issue[3], issue[4], issue[5], issue[6], issue[0]))
            self.__connection.commit()
        except Exception as ex:
            print('Exception: {}'.format(ex))

