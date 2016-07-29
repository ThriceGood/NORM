from models import *

initialize_models()
# new_car = Car(make='Fiat', model='500', year='1959', engine=1000)
# new_car.insert()
# the_car = query(Car, where={'make': 'Fiat'}, order_desc=['make', 'model'])
# print the_car

# gunny_sack = Sack(name='gunny')
# sack_id = gunny_sack.insert()
# print sack_id
# sack_id = 1
# guitar = Item(name='strat', weight=30, sack=sack_id)
# guitar.insert()

print query(Sack, join=Item)