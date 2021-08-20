def get_db_path():
    with open('config.txt', 'r') as file:
        path = 'NOT FIND'
        lines = file.readlines()
        for line in lines:
            if line.find('DATABASE_PATH=') == 0:
                path = line.lstrip('DATABASE_PATH=')

    return path

