from accelidsr import db
from bson import ObjectId
import bson

def fetch_by_id(id, collection):
    if not id or not collection:
        return None

    col = db.get_collection(collection)
    try:
        doc = col.find_one({'_id':  ObjectId(str(id))})
        if doc:
            return doc
        return None
    except bson.errors.InvalidId:
        # Ops, the id provided is not valid
        return None

def save(dbobj):
    if not dbobj or not dbobj.getCollection():
        print "No object or collection specifed"
        return None
    col = db.get_collection(dbobj.getCollection())
    objid = dbobj.getId()
    objdict = dbobj.getDict()
    if objid:
        try:
            out = col.update_one(
               { "_id" : ObjectId(str(objid)) },
               { "$set": objdict },
               upsert=True)
            if out.get('modifiedCount', 0) == 0:
                newid = out.get('upsertedId',None)
                if newid and newid.toString():
                    objdict['_id'] = newid.toString()
                    dbobj.update(objdict)
                    return dbobj
                return None
            if out.get('modifiedCount', 0) == 1:
                return dbobj
            else:
                # More than one record updated?
                print("More than one record updated!")
                return None
        except:
           print(e);
           return None
    else:
        # This is a new object. Needs to be inserted
        out = col.insert_one(objdict)
        if out.get('insertedId', ''):
            newid = out.get('insertedId').toString()
            objdict['_id'] = newid
            dbobj.update(objdict)
            return dbobj
        return False
