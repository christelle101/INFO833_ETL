from collections import Counter
from multiprocessing import Process
import redis, random, os, sys, json, string, math, re

# file to be processed by MapReduce
file_path = "./t8.shakespeare.txt" 
# maximum number of processes
max_nb_processes = 12
# instance of redis
r = redis.StrictRedis('localhost', 6379, charset="utf-8", decode_responses=True)

def random_hash():
    """
        Returns a random hash.
    """
    return "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))

def get_nb_processes(nb_words):
    """
        Returns the number of processes.
    """
    nb_processes = math.ceil(math.log(nb_words))
    nb_processes = nb_processes if nb_processes > 0 else 1
    return nb_processes

def map(words):
    """
        Implements the mapping task of the MapReduce algorithm.
    """
    counts = dict()
    for word in words:
        word = re.sub('[^A-Za-z0-9]+', '', word)
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    if len(counts) > 0:
        hash = random_hash()
        r.hmset(hash, mapping = counts)
        r.publish('reduce', hash)

def reduce(hash1, hash2):
    """
        Implements the reducing task of the MapReduce algorithm.
    """
    count1 = r.hgetall(hash1)
    r.delete(hash1)
    count1 = {i: int(k) for i, k in count1.items()}
    count2 = r.hgetall(hash2)
    r.delete(hash2)
    count2 = {i: int(k) for i, k in count2.items()}
    counts = {i: count1.get(i, 0) + count2.get(k, 0) for i in set(count1) | set(count2)}

    hash = random_hash()
    r.hmset(hash, mapping=counts)
    r.publish('reduce', hash)

def process(hash):
    """
        Writes a json file with all the occurrences once the reducing is done.
    """
    counts = r.hgetall(hash)
    counts = {i: int(k) for i, k in counts.items()}
    counts = dict(sorted(counts.items(), key=lambda item: item[1], reverse=True))
    with open(os.path.join(sys.path[0], "processed_file.json"), "w") as outfile:
        json.dump(counts, outfile, indent = 4)
    exit()

def main():
    """
        Main method.
    """
    file = open(os.path.join(sys.path[0], file_path), "rt")
    data = file.read()
    words = data.split()
    nb_words = len(words)
    nb_processes = get_nb_processes(nb_words)
    active_reducers = 0
    total_reducers = ((nb_processes - 1) if nb_processes > 1 else 1)
    print("The total number of processes is: ", nb_processes)
    print("The total number of reducers is: ", total_reducers)

    for p in range(nb_processes):
        start = math.floor(nb_words/nb_processes*p)
        end = math.floor(nb_words/nb_processes*(p+1))
        process = Process(target = map, args = (words[start:end],))
        process.start() 

    temp_hash = None

    sub = r.pubsub()
    sub.subscribe('reduce')
    for msg in sub.listen():
        if msg is not None and isinstance(msg, dict) and msg.get('type') == "msg":
            hash = msg.get("data")
            if (active_reducers == total_reducers):
                process(hash)
            elif temp_hash is None:
                temp_hash = hash
            else:
                active_reducers += 1
                process = Process(target = reduce, args = (hash, temp_hash))
                process.start()
                temp_hash = None

if __name__ == '__main__':
    main()