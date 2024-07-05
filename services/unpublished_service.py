def update_unpublished_list(tracks):
    try:        
        with open('data/v2/unpublished_list.txt', 'w') as list_file:
            for track in tracks:
                list_file.write("%i\n" % track)
        return None, "updated"    
    except Exception as e:
        print("err: ", e)
        raise Exception(str(e))

def get_unpublished_list():
    try:
        list_file = open('data/v2/unpublished_list.txt', 'r')
        unpublished_list = list_file.readlines()
        unpublished_list = [eval(track) for track in unpublished_list]  
        return unpublished_list
    except Exception as e:
        raise Exception(str(e))
            