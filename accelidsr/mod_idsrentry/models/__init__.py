from accelidsr import db
from bson import ObjectId
from idsr import Idsr
import bson

def fetch_idsr(id):
    """
    Fetch an idsrform from the database and returns its Idsr object.
    If id is empty, no idsrform found for the given id or more than one
    record for the given, id returns None.

    :param id: Unique identifier for the idsrform to be retrieved
    :type id: 12-byte input or a 24-character hex string
    :returns: The Idsr object that corresponds to the given id
    """
    if not id:
        return None

    doc = None
    try:
        doc = db.idsrform.find_one({'_id':  ObjectId(str(id))})
    except bson.errors.InvalidId:
        # Ops, the id provided is not valid
        return None

    if not doc or len(doc) > 1:
        return None

    idsr = Idsr(id)
    # TODO Initialize the object values with db data
    return idsr
