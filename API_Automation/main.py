# from datetime import datetime
#
# import requests
#
# response = requests.get("https://restful-booker.herokuapp.com/booking")
# print(response.status_code)
# print(response.json())
#
# bookings = response.json()
# first_id = bookings[0]['bookingid']
# detail = requests.get(f"https://restful-booker.herokuapp.com/booking/{first_id}")
# print(detail.json())
# booking = detail.json()
#
# assert detail.status_code==200
# assert 'firstname' in booking
# assert 'lastname' in booking
# assert isinstance(booking['totalprice'], (int,float))
# assert isinstance(booking['depositpaid'],bool)
# assert 'checkin' in booking['bookingdates']
# assert 'checkout' in booking['bookingdates']
# try:
#     datetime.strptime(booking['bookingdates']['checkin'],'%Y-%m-%d')
#     validDate = True
# except ValueError:
#     validDate = False
#
# assert validDate, 'Checkin nu e o data valida'
# assert 'additionalneeds' in booking
# assert booking['additionalneeds'] == 'Breakfast'
#
# print("All tests successful")