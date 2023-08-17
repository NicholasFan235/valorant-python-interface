
def print_teams(match_data):
    print('Blue team:')
    for p in match_data['data']['players']['blue']:
        print('\t', p['name'])
    print('\nRed team:')
    for p in match_data['data']['players']['red']:
        print('\t', p['name'])

def print_rough_json_outline(d, level=1):
    for key in d:
        if isinstance(d[key], dict):
            print('|   '*(level-1 if level > 1 else 0) + '|---'*(1 if level > 0 else 0) + key)
            print_rough_json_outline(d[key], level+1)
        elif isinstance(d[key], list):
            print('|   '*(level-1 if level > 1 else 0) + '|---'*(1 if level > 0 else 0) + key + ' -> List')
            if len(d[key]) > 0: print_rough_json_outline(d[key][0], level+1)
        else:
            print('|   '*(level-1 if level > 1 else 0) + '|---'*(1 if level > 0 else 0) + key + ' -> ' + type(d[key]).__name__)
    print('|   '*(level-2 if level > 2 else 0))