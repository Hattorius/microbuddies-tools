"""

    Normally all my python projects get messy as fuck so am going to try to do this right.

"""

from database import db
microbuddiesv2 = db("localhost", "root", "gay", "microbuddiesv2")

a = microbuddiesv2.getTraits(mutation=True, buddytype="Virus", type="Body Patterns")[0]