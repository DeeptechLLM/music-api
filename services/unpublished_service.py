from flask import current_app

def update_unpublished_list(tracks):
    """ Update Unpublished list service
    Args:
        tracks (list): list of track_ids
    
    Returns:
        nothing: returns only msg 
    """
    try:        
        with open('data/v2/unpublished_list.txt', 'w') as list_file:
            for track in tracks:
                list_file.write("%i\n" % track)
        # update current unpublished list in memory
        unpublished_file = open('data/v2/unpublished_list.txt', 'r+')
        UNPUBLISHED_LIST = unpublished_file.readlines() 
        current_app.config['UNPUBLISHED_LIST'] = UNPUBLISHED_LIST
        return None, "updated"    
    except Exception as e:
        print("err: ", e)
        raise Exception(str(e))

def get_unpublished_list():
    """ Get Unpublished list service

    Raises:
        Exception: _description_

    Returns:
        list: list of track_ids
    """
    try:
        list_file = open('data/v2/unpublished_list.txt', 'r')
        unpublished_list = list_file.readlines()
        unpublished_list = [eval(track) for track in unpublished_list]  
        return unpublished_list
    except Exception as e:
        raise Exception(str(e))
            