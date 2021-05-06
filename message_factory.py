def create_issue_change_message(issue):

    updates = {
        'status_id':   ['Status', {'1': 'New', '2': 'In Progress', '3': 'Resolved', '4': 'Feedback', '5': 'Closed'}],
        'priority_id': ['Priority', {'1': 'Low', '2': 'Normal', '3': 'High', '4': 'Urgent', '5': 'Immediate'}],
        'tracker_id':  ['Tracker', {'1': 'Bug', '2': 'Feature', '3': 'Support'}],
        'done_ratio':  ['Progress', {'0': '0%', '10': '10%', '20': '20%', '30': '30%', '40': '40%', '50': '50%',
                                     '60': '60%', '70': '70%', '80': '80%', '90': '90%', '100': '100%'}]
    }

    msg = ""
    for update in list(issue.journals.values())[-1]['details']:
        if update['name'] in updates:
            msg += updates[update['name']][0] + ': ' + updates[update['name']][1][update['new_value']] + '\n'
        elif update['name'] == 'subject':
            msg += 'Subject: {}\n'.format(update['new_value'])
        else:
            continue

    prefix = 'http://192.168.88.145/issues/'
    msg = 'Task #{} modified.\n\n{}\nLink: {}'.format(issue.id, msg, prefix+str(issue.id))
    return msg


def create_issue_assigned_message(issue):
    prefix = 'http://192.168.88.145/issues/'
    msg = 'Task #{} assigned to you.\nStatus: {}\nLink: {}'.format(issue.id, issue.status.name, prefix + str(issue.id))
    return msg