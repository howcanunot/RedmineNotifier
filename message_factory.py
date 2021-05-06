def create_issue_change_message(issue, new_issue):
    prefix = 'http://192.168.88.145/issues/'
    msg = 'Task #{} modified.\n' \
          'Status: {} -> {}\n' \
          'Tracker: {} -> {}\n' \
          'Subject: {} -> {}\n' \
          'Link: {}'.format(new_issue[1], issue[4][1], new_issue[4][1], issue[7], new_issue[7],
                            issue[5], new_issue[5], prefix+str(new_issue[1]))
    return msg


def create_issue_assigned_message(issue):
    prefix = 'http://192.168.88.145/issues/'
    msg = 'Task #{} assigned to you.\nStatus: {}\nLink: {}'.format(issue[1], issue[4][1], prefix + str(issue[1]))
    return msg