import csv
import erppeek
from docutils.nodes import row
from mimetypes import add_type

client = erppeek.Client.from_config('test')

print("Je lance l'import")

bool_tmp = False

iut_device = client.model('iutdevice')
iut_brand = client.model('iutitbrand')
iut_model = client.model('iutitmodel')
iut_model_type = client.model('iutmodeltype')
iut_partner = client.model('res.partner')

tab_types = []

def rech_device(num):
    rech_devices = iut_device.search([('serial_number', '=', num)])
    return iut_device.browse(rech_devices)

def rech_device_all():
    rech_devices = iut_device.search([])
    return iut_device.browse(rech_devices)

def rech_brand(nom):
    rech_brands = iut_brand.search([('name', '=', nom)])
    return iut_brand.browse(rech_brands)

def rech_model(nom):
    rech_models = iut_model.search([('name', '=', nom)])
    return iut_model.browse(rech_models)

def rech_model_types(nom):
    rech_model_types = iut_model_type.search([('name', '=', nom)])
    return iut_model_type.browse(rech_model_types)

def rech_partner(nom):
    rech_partners = iut_partner.search([('name', '=', nom)])
    return iut_partner.browse(rech_partners)


def test_device(str):
    if rech_device(str).serial_number == []:
        return False
    else:
        return True

def test_brands(str):
    if rech_brand(str).name == []:
        iut_brand.create({'name':str}) 
         
def test_model(str):
    if rech_model(str).name == []:
        iut_model.create({'name': str}) 
        

def test_partner(str):
    if rech_partner(str).name == []:
        iut_partner.create({'name':str}) 


def test_types(str):

    tab_types = str.split(':')
                        
    for type in tab_types:
                
        print(rech_model_types(type).name)
                                
        if rech_model_types(type).name == []:
            print("non présent")
            iut_model_type.create({'name':type})
            


def get_id_type(str): 
    
    tab_id = []
    tab_types = str.split(':')
                        
    for type in tab_types:
                
        print(rech_model_types(type).name)
                                
        if rech_model_types(type) == []:
            tab_id.append(rech_model_types(type))
        
    return tab_id

def add_type(str):
        
        a = test_model(str)
        iut_model.write(a, {'type_ids': get_id_type(str)}) 
        
def add_device_to_partner(str, device):
        
        a = test_partner(str)
        iut_partner.write(a, {'device_ids': device}) 


#for device in rech_device():
#    print('{device.id} {device.name}'.format(device=device))
    
    
    
with open('./csvtest.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in spamreader:
                                     
        test_brands(row[5])                 
            
        test_model(row[4])      
            
        test_types(row[6]) 
        
        add_type(row[4])      
             
        test_partner(row[7])                
                    
        if test_device(row[1]):
            # bon baaaa y'a une p'tite faute 
            # le bon 's' à purchase 
            iut_device.create({'name':row[0], 'serial_number': row[1], 'date_allocation':row[2], 'date_purshase': row[3], 'id_model': rech_model(row[4]).ID()}) 
        
        add_device_to_partner(row[7], row[1])

        print(', '.join(row))
        
            