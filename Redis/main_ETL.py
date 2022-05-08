import tasks

task_queue = []

object_T1 = tasks.T1({"path" : "dataT1.json"})
object_T1.extract()
data_T1 = object_T1.load()

task_queue.append({"task": data_T1["task"], "params": data_T1["params"]})

while (len(task_queue) > 0):
    task = task_queue.pop()
    taskObject = getattr(tasks, task["task"])(task["params"])
    taskObject.extract()
    data = taskObject.load()
    
    if ("task" in data):
        task_queue.append({"task": data["task"], "params": data["params"] or None})
    else:
        print(data)
