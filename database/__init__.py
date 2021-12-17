from database.connection import database as db_conn
from database.classes import trait, microbuddy, transaction

class db:
    def __init__(self, host, username, password, database) -> None:
        self.connection = db_conn(host, username, password, database)
        
    def query(self, query) -> any:
        return self.connection.query(query)
    
    
    def traits(self, query) -> list[trait]:
        results = self.query(query)
        res = []
        for row in results:
            res.append(trait(row[0], row[1], row[2], row[3], row[4], row[5], row[6], self))
        return res
    
    def getTraits(self, buddytype=None, type=None, rarity=None, mutation=None, value=None, name=None, nameSearch=None) -> list[trait]:
        query = "SELECT * FROM traits"
        if buddytype is not None:
            query += " WHERE buddytype='" + buddytype + "'"
        if type is not None:
            query += " AND " if "WHERE" in query else " WHERE "
            query += "type='" + type + "'"
        if rarity is not None:
            query += " AND " if "WHERE" in query else " WHERE "
            query += "rarity='" + str(rarity) + "'"
        if mutation is not None:
            query += " AND " if "WHERE" in query else " WHERE "
            query += "mutation='" + "1" if mutation else "0" + "'"
        if value is not None:
            query += " AND " if "WHERE" in query else " WHERE "
            query += "value='" + value + "'"
        if name is not None:
            query += " AND " if "WHERE" in query else " WHERE "
            query += "name='" + name + "'"
        if nameSearch is not None:
            query += " AND " if "WHERE" in query else " WHERE "
            query += "name LIKE '%\"" + name + "\"%'"
        return self.traits(query)

    def microbuddies(self, query) -> list[microbuddy]:
        results = self.query(query)
        res = []
        for row in results:
            res.append(microbuddy(row[1], row[2], row[3], row[4], row[5], row[6], row[7], self))
        return res
    
    def getMicrobuddies(self, tokenid=None, name=None, species=None, generation=None, dominantSearch=None, recessiveSearch=None) -> list[microbuddy]:
        query = "SELECT * FROM microbuddies"
        if tokenid is not None:
            return self.microbuddies(query + " WHERE tokenId=" + str(tokenid))
        
        if name is not None:
            query += " WHERE name='" + name + "'"
        if species is not None:
            query += " AND " if "WHERE" in query else " WHERE "
            query += "species='" + species + "'"
        if generation is not None:
            query += " AND " if "WHERE" in query else " WHERE "
            query += "generation='" + str(generation) + "'"
            
        if dominantSearch is not None:
            query += " AND " if "WHERE" in query else " WHERE "
            query += "dominants LIKE '%\"" + dominantSearch + "\"%'"
        if recessiveSearch is not None:
            query += " AND " if "WHERE" in query else " WHERE "
            query += "recessives LIKE '%\"" + recessiveSearch + "\"%'"

        return self.microbuddies(query)
    
    def transactions(self, query) -> list[transaction]:
        results = self.query(query)
        res = []
        for row in results:
            res.append(transaction(row[3], row[4], row[6], row[9] if row[9] != 0 else None, row[8], self))
        return res
    
    def getTransactions(self, hash=None, method=None, dominantSearch=None, recessiveSearch=None, child=None, microbuddy=None):
        query = "SELECT * FROM transactions"
        if hash is not None:
            return self.transactions(query + " WHERE hash='" + hash + "'")
        
        if method is not None and (dominantSearch is None or recessiveSearch is None):
            query += " WHERE method='" + method + "'"
        if child is not None:
            query += " AND " if "WHERE" in query else " WHERE "
            query += "microbuddy='"+ str(child) +"'"
        if microbuddy is not None:
            query += " AND " if "WHERE" in query else " WHERE "
            query += "parentmicrobuddy='" + str(microbuddy) + "'"
            
        if dominantSearch is not None:
            query += " AND " if "WHERE" in query else " WHERE "
            dominantSearch = hex(int(dominantSearch))[2:]
            query += "inputs LIKE '" + dominantSearch + "'"
        if recessiveSearch is not None:
            query += " AND " if "WHERE" in query else " WHERE "
            recessiveSearch = hex(int(recessiveSearch))[2:]
            query += "inputs LIKE '" + recessiveSearch + "'"
        if recessiveSearch is not None or dominantSearch is not None:
            query += " AND method='replicate'"
            
        results = self.transactions(query)
        if dominantSearch is None and recessiveSearch is None:
            return results

        res = []
        for row in results:
            print(row.inputs)
