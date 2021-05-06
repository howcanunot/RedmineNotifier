from redmine_issue_monitor import get_issues_assigned_to
from message_factory import create_issue_change_message, create_issue_assigned_message
from bot import send_message
from time import sleep


class User:

    def __init__(self, id, redmine_id, telegram_id, name):
        self.id = id
        self.redmine_id = redmine_id
        self.telegram_id = telegram_id
        self.name = name
        self.issues = []
        self.issues_id = set()

    def bind_user_issues(self):
        user_issues = get_issues_assigned_to(self.redmine_id)
        self.issues = sorted(user_issues, key=lambda x: x[1])
        for issue in self.issues:
            self.issues_id.add(issue[1])

    def check_new_issues(self):
        issues = get_issues_assigned_to(self.redmine_id)
        if len(issues) > len(self.issues):
            new_issues = [issue for issue in issues if issue[1] not in self.issues_id]
            print(new_issues)
            for issue in new_issues:
                self.issues_id.add(issue[1])
                message = create_issue_assigned_message(issue)
                send_message(self.telegram_id, message)
                sleep(2.0)
            self.issues += new_issues
            self.issues.sort(key=lambda x: x[1])
            print(self.issues)

    def check_changed_issues(self):
        issues = sorted([issue for issue in get_issues_assigned_to(self.redmine_id) if issue[1] in self.issues_id],
                        key=lambda x: x[1])
        for iter in range(len(self.issues)):
            if int(issues[iter][8]) == int(self.id):
                continue
            redmine_changed_time = issues[iter][3]
            local_changed_time = self.issues[iter][3]
            delta = redmine_changed_time - local_changed_time
            if abs(delta.seconds) > 2:
                message = create_issue_change_message(self.issues[iter], issues[iter])
                self.issues[iter] = issues[iter]
                send_message(self.telegram_id, message)
                sleep(2.0)

    @staticmethod
    def create_user(user_info):
        # Validate user_info.
        return User(user_info[0], user_info[1], user_info[2], user_info[3])
