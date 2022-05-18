from multiprocessing import Process
import tasks, redis, time, string, random

r = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8")

def random_hash():
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))

