import pymongo
from config import Config

DB_URL   = Config.MONGODB_URL
DB_NAME  = Config.MONGODB_DBNAME
myclient = pymongo.MongoClient(DB_URL)


### Check If Database Exist!
def check_db_exist():
    dblist = myclient.list_database_names()
    if DB_NAME in dblist:
        return 1
    else:
        return 0

### Create DB:
def create_db():
    DB    = myclient[DB_NAME]
    USERS = DB["users"]
    FILMS = DB["films"]
    
    USERS_DICT = {
        "user": "SSID",
        "user_name": "@R00T_SERVER",
        "user_id": Config.BOT_TOKEN,
        "lang": "en",
        "is_premium": False,
        }
    
    FILMS_DICT = {
        "film_name": "tmp",
        "rate": 10,
        "duration": 100,
        "language": "english",
        "region": "United Kingdom",
        "director": "SSID",
        "description": "Descriptions_here_BCDEFGHIJKLMNOPQRSTUVWXYZ1234567890",
        "tags": "#ABC, #DEF, #123",
        "film_id": "BAACAgQAAxkBAAIEaGhn8QgbiBuGhwABx2mc3b_f6SflVQACwxMAAhBfEVM6ZKmfHv9Ymh4E"
        }

    USERS.insert_one(USERS_DICT)
    FILMS.insert_one(FILMS_DICT)
    return 0

### Check User In DB:
def check_user(id):
    DB    = myclient[DB_NAME]
    USERS = DB["users"]
    result = USERS.find_one({"user_id": id})
    
    if result != None and result['user_id'] == id:
        return True
    else:
        return False

### Add User In DB:
def add_user(message):
    if not check_user(message.from_user.id):
        DB    = myclient[DB_NAME]
        USERS = DB["users"]
        QUERY = {
            "first_name": message.from_user.first_name,
            "last_name":  message.from_user.last_name,
            "user_name":  message.from_user.username,
            "user_id":    message.from_user.id,
            "banned":     False,
            "lang":       "en",
            "vip":        {
                            "state":        False,
                            "subscr-date":  0,
                            "expire":       0,
                           }
        }
        USERS.insert_one(QUERY)
        return False
    else:
        return True

def is_banned(message):
    DB     = myclient[DB_NAME]
    USERS  = DB["users"]
    QUERY  = {"user_id": message.from_user.id}
    result = USERS.find_one(QUERY)
    return result['banned']

def ban_user(message):
    DB        = myclient[DB_NAME]
    USERS     = DB["users"]
    QUERY     = { "user_id": message }
    newvalues = { "$set": { "banned": True } }
    USERS.update_one(QUERY, newvalues)

def unban_user(message):
    DB        = myclient[DB_NAME]
    USERS     = DB["users"]
    QUERY     = {"user_id": message}
    newvalues = { "$set": { "banned": False } }
    USERS.update_one(QUERY, newvalues)

def get_total_user():
    DB    = myclient[DB_NAME]
    USERS = DB["users"]
    return USERS.count_documents({})

def get_banned_user():
    DB    = myclient[DB_NAME]
    USERS = DB["users"]
    return USERS.count_documents({"banned": True})

def get_total_film():
    DB    = myclient[DB_NAME]
    FILMS = DB["films"]
    return FILMS.count_documents({})

def add_film_db(id, name):
    if not check_film_exist(name):
        DB       = myclient[DB_NAME]
        FILMS    = DB["films"]
        NEW_FILM = {
            "film_name": name,
            "rate": None,
            "duration": None,
            "language": None,
            "region": None,
            "director": None,
            "description": None,
            "tags": "#ABC, #DEF, #GHI",
            "film_id": id
            }        
        FILMS.insert_one(NEW_FILM)
        return True
    else:
        return False

def get_film_db(name):
    DB     = myclient[DB_NAME]
    FILMS  = DB["films"]
    QUERY  = {"film_name": name}
    result = FILMS.find_one(QUERY)
    return result

def check_film_exist(name):
    DB     = myclient[DB_NAME]
    FILMS  = DB["films"]
    QUERY  = {"film_name": name}
    result = FILMS.find_one(QUERY)
    if result != None:
        return True
    else:
        return False

def delete_film(name):
    if check_film_exist(name):
        DB    = myclient[DB_NAME]
        FILMS = DB["films"]
        QUERY = {"film_name": name}
        FILMS.delete_one(QUERY)
        return True
    else:
        return False

def delete_all_film():
    DB    = myclient[DB_NAME]
    FILMS = DB["films"]
    FILMS.delete_many({})
    return True

def get_all_user_id():
    DB    = myclient[DB_NAME]
    USERS = DB["users"]
    tmp_ids  = []
    for ID in USERS.find({}):
        tmp_ids.append(ID['user_id'])
    UIDS = tmp_ids.copy()
    tmp_ids.clear()
    return UIDS


def del_user(ID):
    DB    = myclient[DB_NAME]
    USERS = DB["users"]
    QUERY = {"user_id": ID}
    USERS.delete_one(QUERY)


def update_film_info(name, key, new_value):
    if key not in ["film_name", "rate", "duration", "language", "region", "director", "description", "tags"]:
        return False
    else:
        DB    = myclient[DB_NAME]
        FILMS = DB["films"]
        QUERY = {"film_name": name}
        newvalues = { "$set": { key: new_value } }
        FILMS.update_one(QUERY, newvalues)
        return True
