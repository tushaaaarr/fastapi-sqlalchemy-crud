# fastapi-sqlalchemy-crud

Live demo --  https://myaddress-book.herokuapp.com/user/2/view-addresses/

Swagger doc --  https://myaddress-book.herokuapp.com/docs


After Cloning project Follow below steps


run the following commands (on project base directory) 
```
pip install -r requirements.txt
```


Run the following command to start Fastapi Project locally
```
uvicorn main:app --reload
```



```
User Section--
1) See all registered users (/view-all_users)

2) Add new user(/add-user/)

parameters = 
{
"email":"tusharspatil808@gmai.com",
"password":1234
 }


Address Section--



1)Retrieve the addresses that are within a given distance and location coordinates 
Note - Enter distance in km only
 input_params = 
          {
              "distance":100,
              "coordinates": "Latitude :28.679079, Longitude:77.069710"

          }


2)View all addresses (/user/{user_id}/view-addresses/).

3)View one address (/user/view-address/{address_id})
 
4)Create new address (/user/{user_id}/create-addresse/) 

parameters = 
              {
              "address":"city name, pincode",
              "coordinates":"Latitude : 16.4020402, Longitude: 74.3842372",
               }

5)Update address ("/user/update-address/{address_id})
parameters = 
              {
              "address":"city name, pincode",
              "coordinates":"Latitude : 16.4020402, Longitude: 74.3842372",
               }

6)Delete address (/user/delete-addresse/{address_id})
```
