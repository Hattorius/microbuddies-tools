"""

    Normally all my python projects get messy as fuck so am going to try to do this right.

"""

from database import db
db = db("localhost", "root", "gay", "microbuddiesv3")

trait = db.getTraits(buddytype="Algae", name="CLOUDJUMPINGBUNNY")[0]
print(trait)
trait.findMutationWay()
print("Probs:", trait.mutantDom[4], trait.mutantRec[4])
