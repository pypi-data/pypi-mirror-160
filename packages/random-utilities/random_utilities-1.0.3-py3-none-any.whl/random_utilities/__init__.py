import os
import random
import pymongo
import console
import models.time_created
import traceback
import sys


def log(msg: str, is_error=False, is_success=False, is_force=False):
    """ Logs verbose information about runtime. """
    if bool(os.environ.get("SHOW_LOGS", False)) == True or is_force:
        msg = console.fx.bold(str(msg))

        """Get the current timestamp"""
        _time = models.time_created.TimeCreatedModel()
        time = f"{_time.formatted_date} {_time.time}"

        """Show the message"""
        print(f'{console.fx.dim(time + " |")} [{console.fg.red(msg) if is_error else (console.fg.white(msg) if not is_success else console.fg.green(msg))}]')
log(f"""Verbose mode: {os.environ.get('SHOW_LOGS', 'False')}. To be able to use the log utility, requires you to set the 'SHOW_LOGS' env variable to 'True' / '1'.""", is_force=True)


def query_to_dict(query_string: str) -> dict:
    """ Convert a URL query string to a dictionary """
    query_string_split_pairs = query_string.split("&")
    dict_query_string = { }
    for query in query_string_split_pairs:
        query_split = query.split("=") # name=value === ["name", "value"]
        dict_query_string[query_split[0]] = query_split[1]
        if query_split[1] in ("true", "false"):
            dict_query_string[query_split[0]] = bool(query_split[1]) # Parse boolean values
        elif query_split[1].isdecimal():
            dict_query_string[query_split[0]] = float(query_split[1])
    return dict_query_string


def random_sort(_list: list) -> list:
    """ Returns a randomly sorted list. """
    random_sorted_indices = []
    for _ in _list:
        b = len(_list) - 1
        index = random.randint(a=0, b=b)
        while index in random_sorted_indices:
            index = random.randint(a=0, b=b)
            if index not in random_sorted_indices:
                break
        random_sorted_indices.append(index)
    
    """ Re-structure the list with the randomness. """
    random_list = [0 for i in range(len(_list))]
    for index, random_index in enumerate(random_sorted_indices):
        random_list[index] = _list[random_index]
    return random_list
    

def read_request_body(request) -> dict:
    """Reads the binary data sent in the request."""
    request_data = request.get_data()

    """Proof check if the data is readable as normal text or not."""
    if request_data != b'' or request_data.isascii():
        request_body = request.get_json()
        if request_body != None:
            return request_body
        else:
            """Else return an empty dictionary."""
            return dict()
    else:
        """Else return an empty dictionary."""
        return dict()


"""Checks if a dictionary contains all fields in a provided array, returns missing fields if any"""
def fields_all_check(dct: dict, lst: list) -> tuple:
    for field in dct:
        if field in lst:
            lst.remove(field)
    is_all_check = True if len(lst) == 0 else False
    return is_all_check, lst


"""Database connection capabilities."""
default_database = None # global access variable to save the db connections
default_collection = None # to assign it to a collection connection
def initiate_mongodb_connection(mongo_host, database_name, collection_name):
    if mongo_host and collection_name and database_name:
        try:
            log("Connecting to database and testing connection...")
            mongo_client = pymongo.MongoClient(mongo_host,
                server_api=pymongo.server_api.ServerApi("1"))

            default_database = mongo_client[database_name]
            default_collection  = default_database[collection_name]
            document_count = default_collection.count_documents({ })

            log(f"Database successfully connected with `{document_count}` documents in collection `media_resources`.")

            return default_collection, True
        except:
            log("Opps something went wrong. " + traceback.format_exc())
            sys.exit(1)
    else:
        log("No database connection specified. Not connecting to any.")
        return None, False
