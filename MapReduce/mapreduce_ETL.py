from collections import Counter
from multiprocessing import Process
import redis, random, time, os, sys, json, string, math, re

file_path = "./t8.shakespeare.txt"
max_nb_processes = 6
r = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)

def random_hash():
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))

def get_nb_processes(nb_words):
    nb_processes = math.ceil(math.log(nb_words))
    nb_processes = nb_processes if nb_processes > 0 else 1
    return nb_processes

def map(words):
    counts = dict()
    for word in words:
        word = re.sub('[^A-Za-z0-9]+', '', word)
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    if len(counts) > 0:
        hash = random_hash()
        r.hset(hash, mapping = counts)
        r.publish('reduce', hash)