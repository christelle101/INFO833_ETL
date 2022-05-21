from multiprocessing import Process
import multiprocessing
import tasks, redis, time, string, random

r = redis.Redis(host='localhost', port=6379, db=0, charset="utf-8")

def random_hash():
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))


params = {"path": "dataT1.json"}
hash = random_hash()
r.hset(hash, mapping = params)
r.rpush("task_queue", f"T1:{hash}")

def genTask(task):
    taskName = task.split(":")[0]
    hash = task.split(":")[1]
    params = r.hgetall(hash)
    r.delete(hash)
    params = {k.decode("utf-8"): v.decode("utf-8") for k, v in params.items()}
    
    taskObject = getattr(tasks, taskName)(params)
    taskObject.extract()
    data = taskObject.load()
    
    if ("task" in data):
        hash = random_hash()
        params = data["params"] or {}
        r.hset(hash, mapping=params)
        r.rpush("task_queue", data["task"] + ":" + hash)
    else:
        print(data)

while(True):
        if (r.llen("task_queue") == 0):
            print("There is Zero Task to Execute ")
            for i in range(0, 100):
                time.sleep(0.1) 
                if (r.llen("task_queue") > 0):
                    break
            if (r.llen("task_queue") == 0):
                print("Stoping the Program")
                break
    
        
        task = (r.lpop("task_queue")).decode("utf-8")
        p = Process(target=genTask, args=(task,))
        p.start()
