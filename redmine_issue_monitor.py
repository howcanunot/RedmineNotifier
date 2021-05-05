from redminelib import Redmine

URL = 'http://localhost:3000/'
LOGIN = 'admin'
PASSW = '12345678'

redmine = Redmine(URL, username=LOGIN, password=PASSW)


def get_all_issues():
    result = []
    issues = redmine.issue.all()
    for issue in issues:
        # TODO: change to redminelib filtering
        if issue.status.id != 5:
            # return not closed tasks
            if hasattr(issue, 'assigned_to'):
                if hasattr(issue.assigned_to, 'id') and hasattr(issue.assigned_to, 'name'):
                    result.append((issue.id, issue.tracker.name, (issue.status.id, issue.status.name),
                                   (issue.assigned_to.id, issue.assigned_to.name), issue.updated_on, issue.subject))
    return result


def get_issues_assigned_to(redmine_user_id):
    result = []
    issues = redmine.issue.filter(assigned_to_id=redmine_user_id)
    for issue in issues:
        # TODO: change to redminelib filtering
        if issue.status.id != 5:
            if hasattr(issue, 'assigned_to'):
                if hasattr(issue.assigned_to, 'id') and hasattr(issue.assigned_to, 'name'):
                    result.append((None, issue.id, (issue.assigned_to.id, issue.assigned_to.name), issue.updated_on,
                                   (issue.status.id, issue.status.name), issue.subject, []))
    return result
