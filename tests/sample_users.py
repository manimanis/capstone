import random

from app.auth import generate_random_picture

NAMES = list({
    'mani', 'jedidi', 'sassi', 'fkih', 'mhiri',
    'baccouche', 'abed', 'daghrir', 'said', 'gharzoul',
    'laatiri', 'ben amor', 'hammami', 'layouni', 'ghanmi',
    'ben abdallah', 'dorgham', 'achour', 'gharbi', 'rjab',
    'zouari', 'golli', 'letaief'
})

SURNAMES = list({
    'mohamed anis', 'mohamed yosri', 'yosra', 'faouzia', 'sana',
    'wafa', 'hala', 'hassen', 'yassine', 'asma',
    'hedi', 'fatma', 'hajer', 'fethi', 'baher',
    'sondes', 'slim', 'souhir', 'eya', 'karim',
    'lazhar', 'samira', 'mattar', 'mohamed', 'mariem',
    'sirine', 'majd'
})


def generate_names(count=20):
    """Generate a set of 'count' names"""
    names_set = set([])
    while len(names_set) < count:
        names_set.add(random.choice(SURNAMES) + ' ' + random.choice(NAMES))
    return list(names_set)


def build_username(name):
    """Generate a username by joining the first letter of each word and the
    last word"""
    words = name.split()
    return ''.join(w[0] for w in words[:-1]) + words[-1]


def generate_usernames(names):
    """Generate usernames for each name in the list 'names'"""
    usernames_list = []
    for name in names:
        username = build_username(name)
        base_username = username
        while username in usernames_list:
            username = f'{base_username}{random.randint(2, 1000)}'
        usernames_list.append(username)
    return usernames_list


def generate_roles(roles=['teacher', 'student'], count=20):
    """Generate 'count' roles"""
    return random.choices(roles, k=count)


def generate_random_users(count=20, role=None):
    """Generate random users dictionaries"""
    random_names = generate_names(count)
    usernames = generate_usernames(random_names)
    roles = (generate_roles(count)
             if role is None else [role for i in range(count)])
    users = [dict(username=username, fullname=name, role=role,
                  picture=generate_random_picture())
             for name, username, role in zip(random_names, usernames, roles)]
    return users
