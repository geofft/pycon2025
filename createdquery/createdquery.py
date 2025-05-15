import fcntl

F_CREATED_QUERY = 1028


def was_created(file):
    return bool(fcntl.fcntl(file, F_CREATED_QUERY))
