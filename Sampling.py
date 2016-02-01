import random


def sample_list(var_list, sample_size):
    if len(var_list) > sample_size:
        return random.sample(var_list, sample_size)
    else:
        print 'sample size is greater than num points'
        return var_list


def sample_unzip(var_tuples, sample_size):
    var_sampled = sample_list(var_tuples, sample_size)
    if len(var_sampled) > 0:
        return zip(*var_sampled)
    else:
        return [], []
