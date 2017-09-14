from model import Person, Address
import model
   #Helper Functions
def example_data():
    """Sample Data to Test Database"""

    usr1 = Person(email='happy@gmail.com', password='onefineday', fname='Smiley', lname='Dwarf',
                    phone='425-222-2222', license_number='Null')
    usr2 = Person(email='grumpy@gmail.com', password='onceuponatime', fname='Grump', lname='Dwarf',
                    phone='425-222-2223', license_number='Null')
    usr3 = Person(email='sneezey@gmail.com', password='tissueplease', fname='Snee', lname='Zeee',
                    phone='425-222-2224', license_number='Null')

    Address1 = Address(street_address='321 Main Street', city='Alameda', state='CA', zip_code='94501',
                    latitude = 'Null', longitude='Null', name_of_place='Alameda Point Gym')
    Address2 = Address(street_address='425 Webster', city='Alameda', state='CA', zip_code='94501',
                    latitude ='Null', longitude='Null', name_of_place='Alameda Karate')
    Address3 = Address(street_address='2 Hornet Drive', city='Alameda', state='CA', zip_code='94501',
                    latitude='Null', longitude='Null', name_of_place='Hornet Field')
    Address4 = Address(street_address='1 Boulder Canyon Road', city='Boulder', state='CO', zip_code='80303',
                    latitude='Null', longitude='Null', name_of_place='CU Boulder')

    model.db.session.add_all([usr1,usr2,usr3,Address1,Address2,Address3,Address4])
    model.db.session.commit()
