import configparser
import simplejson as json
import redis

settings = configparser.ConfigParser()
settings.read('settings.ini')

# redis persistence docs: https://redis.io/topics/persistence

# connect to redis
r = redis.StrictRedis(host = settings['redis']['redisdb_host'], port = settings['redis']['redisdb_port'], db = settings['redis']['redisdb'])

def set_obj_redis(name, obj):
    try:
        r.set(name, json.dumps(obj))
        return True
    except:
        return False


def get_obj_redis(name):
    try:
        obj = json.loads(r.get(name).decode('utf-8'))
        return obj
    except:
        return False


def del_obj_redis(name):
    try:
        result = r.delete(name)
        return result
    except:
        return False


def hset_redis(name, field, val):
    # it saves in key "name" the field=val
    try:
        r.hset(name, field, val)
        return True
    except:
        return False


def hget_redis(name, field):
    try:
        obj = r.hget(name, field).decode('utf-8')
        return obj
    except:
        return False


def hdel_redis(name, field):
    try:
        obj = r.hdel(name,field)
        return obj
    except:
        return False


def hkeys_redis(name):
    try:
        obj = r.hkeys(name)
        return obj
    except:
        return False






