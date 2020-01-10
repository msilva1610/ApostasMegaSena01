import requests
from multiprocessing.dummy import Pool

pool = Pool(10) # Creates a pool with ten threads; more threads = more concurrency.
                # "pool" is a module attribute; you can be sure there will only
                # be one of them in your application
                # as modules are cached after initialization.

if __name__ == '__main__':
    futures = []
    for x in range(100000):
        futures.append(pool.apply_async(requests.get, ['http://localhost:8090/']))
    # futures is now a list of 10 futures.
    # print(len(futures))
    for future in futures:
        print(future.get()) # For each future, wait until the request is
                            # finished and then print the response object.