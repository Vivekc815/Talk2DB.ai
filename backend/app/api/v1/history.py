lst = []
def history_store(store):
    lst.append(store)
    if(len(lst)>10):
        return lst[-1:-10]
    else:
        return lst[::-1]