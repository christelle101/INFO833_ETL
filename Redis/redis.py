import redis, taches, string

r = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8")
r.delete("task_queue")
