import json, utils

class trait:
    def __init__(self, database_id, is_mutation=0, rarity=1, type="", trait_value=1, trait_name="", buddytype="", connection=None) -> None:
        self.id = database_id
        self.mutation = False if is_mutation == 0 else True
        self.rarity = rarity
        self.type = type
        self.trait_value = trait_value
        self.trait_name = trait_name
        self.buddytype = buddytype
        self.connection = connection
        
    def __repr__(self) -> str:
        return str(self.__dict__)
    
    def findBuddiesWith(self) -> any:
        return self.connection.getMicrobuddies(dominantSearch=self.trait_name)
    
    def findMutationWay(self) -> None:
        microbuddiesWithTrait = self.connection.getMicrobuddies(dominantSearch=self.trait_name, species=self.buddytype)
        possibleParentsWithWays = []
        for microbuddy in microbuddiesWithTrait:
            found = False
            parent = microbuddy.getParent()
            if isinstance(parent, int):
                continue
            for dominant in parent.dominants:
                if dominant[2] == self.type and int(dominant[3]) == self.trait_value:
                    found = True
                    break
            if not found:
                for recessive in parent.recessives:
                    if (recessive[2] == self.type and int(recessive[3]) == self.trait_value):
                        found = True
                        break
            if found:
                continue
            possibleParentsWithWays.append(parent)
        possibleCombinationDominant = []
        for microbud in possibleParentsWithWays:
            for dominant in microbud.dominants:
                if dominant[2] == self.type:
                    possibleCombinationDominant.append(json.dumps(dominant))
                    z = round(utils.calculateSubstringPercentage(self.trait_name, dominant[4])/10)
                    if z > 0:
                        for _ in range(z):
                            possibleCombinationDominant.append(json.dumps(dominant))
        probablyDominant = json.loads(max(set(possibleCombinationDominant), key=possibleCombinationDominant.count))
        possibleCombinationRecessive = []
        for microbud in possibleParentsWithWays:
            y = 4
            for recessive in microbud.recessives:
                if recessive[2] != self.type:
                    continue
                if int(recessive[3]) == 255 or int(recessive[3]) == 0 or json.dumps(recessive) in possibleCombinationRecessive or recessive[3] == probablyDominant[3] or int(recessive[3]) > int(self.trait_value):
                    continue
                for _ in range(y):
                    possibleCombinationRecessive.append(json.dumps(recessive))
                z = round(utils.calculateSubstringPercentage(self.trait_name, recessive[4])/10) - round(utils.calculateSubstringPercentage(probablyDominant[4], recessive[4])/10)
                if z == 0:
                    continue
                if z > 0:
                    for _ in range(z):
                        possibleCombinationRecessive.append(json.dumps(recessive))
                y -= 1
        probablyRecessive = json.loads(max(set(possibleCombinationRecessive), key=possibleCombinationRecessive.count))
        self.mutantDom = probablyDominant
        self.mutantRec = probablyRecessive

class microbuddy:
    def __init__(self, tokenid, quote, name, species, generation, dominants, recessives, connection=None) -> None:
        self.id = tokenid
        self.quote = quote
        self.name = name
        self.species = species
        self.generation = generation
        self.dominants = json.loads(dominants)
        self.recessives = json.loads(recessives)
        self.parent = None
        self.connection = connection
        
    def __repr__(self) -> str:
        d = self.__dict__
        return str({x: d[x] for x in d if x not in ["dominants", "recessives", "connection"]})
    
    def getParent(self, id=None) -> any:
        if id is not None:
            self.parent = self.connection.getMicrobuddies(tokenid=id)[0]
        else:
            creationTransaction = self.connection.getTransactions(child=self.id, method="replicate")
            if len(creationTransaction) == 0:
                creationTransaction = self.connection.getTransactions(child=self.id, method="simpleReplicate")
            if len(creationTransaction) == 0:
                self.parent = 0
                return 0
            try:
                self.parent = self.connection.getMicrobuddies(tokenid=creationTransaction[0].microbuddy)[0]
            except:
                return 0
        return self.parent
        
    def getDominants() -> list[trait]:
        pass
    
    def getRecessives() -> list[trait]:
        pass

class transaction:
    def __init__(self, hash, method, inputs, microbuddy=None, child=None, connection=None) -> None:
        self.hash = hash
        self.method = method
        self.inputs = json.loads(inputs)
        self.microbuddy = microbuddy
        self.child = child
        self.connection = connection
        
    def __repr__(self) -> str:
        return str(self.__dict__)
