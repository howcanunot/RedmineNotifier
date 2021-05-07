from redmine_issue_monitor import get_issues_assigned_to
from message_factory import create_issue_change_message, create_issue_assigned_message
from bot import send_message
from time import sleep


class User:

    __users_telegram_ids = {}

    def __init__(self, id, redmine_id, telegram_id, name):
        self.id = id
        self.redmine_id = redmine_id
        self.telegram_id = telegram_id
        self.name = name
        self.issues = []
        self.issues_id = set()
        User.__users_telegram_ids[int(redmine_id)] = telegram_id

    def bind_user_issues(self):
        user_issues = get_issues_assigned_to(self.redmine_id)
        self.issues = sorted(user_issues, key=lambda x: x.id)
        for issue in self.issues:
            self.issues_id.add(issue.id)

    def check_new_issues(self):
        issues = get_issues_assigned_to(self.redmine_id)
        if len(issues) > len(self.issues):
            new_issues = [issue for issue in issues if issue.id not in self.issues_id]
            print(len(self.issues))
            for issue in new_issues:
                self.issues_id.add(issue.id)
                message = create_issue_assigned_message(issue)
                send_message(self.telegram_id, message)
                sleep(2.0)
            self.issues += new_issues
            self.issues.sort(key=lambda x: x.id)

    def check_changed_issues(self):
        issues = sorted([issue for issue in get_issues_assigned_to(self.redmine_id) if issue.id in self.issues_id],
                        key=lambda x: x.id)

        if len(self.issues) != len(issues):
            self.__delete_empty_issues(issues)

        for iter in range(len(self.issues)):
            # if User.get_user_last_update_id(issues[iter]) == int(self.id):
            #     continue
            redmine_changed_time = issues[iter].updated_on
            local_changed_time = self.issues[iter].updated_on
            delta = redmine_changed_time - local_changed_time
            if abs(delta.seconds) > 2:
                message = create_issue_change_message(issues[iter])
                self.issues[iter] = issues[iter]
                send_message(self.telegram_id, message)
                sleep(2.0)
                for watcher in list(issues[iter].watchers.values()):
                    send_message(User.__users_telegram_ids[watcher['id']], message)
                    sleep(2.0)

    def __delete_empty_issues(self, issues):
        issues_id = set()
        for issue in issues:
            issues_id.add(issue.id)
        empty_issues_ids = self.issues_id - issues_id
        self.issues = [issue for issue in self.issues if issue.id not in empty_issues_ids]
        self.issues_id = issues_id


    @staticmethod
    def get_user_last_update_id(issue):
        issue_id = -1
        if issue.journals.total_count > 0:
            issue_id = int(list(issue.journals.values())[-1]['user']['id'])
        return issue_id

    @staticmethod
    def create_user(user_info):
        # Validate user_info.
        return User(user_info[0], user_info[1], user_info[2], user_info[3])
