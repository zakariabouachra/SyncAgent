import threading
import mongodb_utils
import mysql_utils


def main():
    all_collections = mongodb_utils.db.list_collection_names()

    mongo_threads = []
    for col_name in all_collections:
        t = threading.Thread(target=mongodb_utils.watch_collection, args=(col_name,))
        t.start()
        mongo_threads.append(t)

    mysql_thread = threading.Thread(target=mysql_utils.watch_mysql)
    mysql_thread.start()

    mysql_thread.join()
    for t in mongo_threads:
        t.join()

if __name__ == "__main__":
    main()