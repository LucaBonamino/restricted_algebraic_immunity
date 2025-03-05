def get_number_of_function(limit_time, time_per_func, n_cores = 4):
    i = 0
    r = 0
    while r <= limit_time:
        r = (i // n_cores) * time_per_func
        i += 1
    return i-2