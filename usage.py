from models import *

new_car = Car(make='Fiat', model='500', year='1959', engine=1000)
# new_car.insert()
the_car = query(Car, query={'make': 'Fiat'})
print the_car