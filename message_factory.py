def create_issue_change_message(issue):
    prefix = 'http://192.168.88.145/issues/'
    msg = 'Task #{} modified.\nStatus: {}\nLink: {}'.format(issue[1], issue[4][1], prefix+str(issue[1]))
    return msg


def create_issue_assigned_message(issue):
    prefix = 'http://192.168.88.145/issues/'
    msg = 'Task #{} assigned to you.\nStatus: {}\nLink: {}'.format(issue[1], issue[4][1], prefix + str(issue[1]))
    return msg