##

import requests, time, smtplib, logging, datetime




## CONFIGURE YOUR GEO-LOCATION FOR BETTER AND ACCURATE RESULTS
# find your coordinates at "latlong.net"
# enter your email and passord to get an email notification (optional)


# DONT FORGET TO ENTER YOUR COORDINATES...THOSE ENTERED ARE AN EXAMPLE !!

info = {
    'email':' ',
    'password':"",
    'cood':{
        'longitude':'35.1466',
        'latitude':' -0.671895',
        },

}
ISS_position_api = "http://api.open-notify.org/iss-now.json"
sunrise_sunset_api = "https://api.sunrise-sunset.org/json"


logging.basicConfig(format = "%(levelname)s %(asctime)s   %(message)s",filename = "data.log", level = logging.INFO)
 
class ISS_LOOKOUT:

 
    def get_ISS_pos(self):
        # get the cordinates of the ISs
        response = requests.get(ISS_position_api)
        response.raise_for_status()
        data = response.json()
        latitude = data['iss_position']["latitude"]
        longitude = data['iss_position']['longitude']
        iss_position = (latitude, longitude)

       

        return iss_position


    def is_it_overhead(self):
        # returns true if the ISS is near your coordinates
        iss_pos = self.get_ISS_pos()
        lat = float(iss_pos[0])
        lng = float(iss_pos[1])

        my_lat = float(info['cood']['latitude'])
        my_long = float(info['cood']['longitude'])

        if my_lat -5  <= lat <= my_lat + 5:
        	if my_long -5 <= lng <= my_long + 5:
        		return True
         

    def is_it_dark(self):
        # checks if it is night so that
        # the iss is visible
        parameters = {
            'lat':info['cood']['latitude'],
            'lng':info['cood']['latitude'],
            'formatted':0,
                      }

        response = requests.get(sunrise_sunset_api, params = parameters)
        response.raise_for_status()
        data = response.json()
        
        print(data)
       	sunrise = int(data['results']['sunrise'].split("T")[1].split(":")[0])
       	sunset =int(data['results']['sunset'].split("T")[1].split(":")[0])

        time_now = datetime.datetime.now().hour

       	if sunrise >= time_now  or sunset <= time_now:
        	return True

    def notify_me(self):
    	logging.info("ISS is overhead !")
        try:
            # send yourself an email
            connection = smtplib.SMTP('smtp.gmail.com')
            connection.starttls()
            connection.login(info['email'], info['password'])
            connection.sendmail(
                from_addr = info['email'],
                to_addrs = info['email'],
                msg = """Subject:LOOK UP !

                THE ISS IS NOW VISIBLE...LOOK uP!!!

                """)
        except:
            pass


         


    def run(self):
        while True:
            if self.is_it_dark() and self.is_it_overhead():
                self.notify_me()
 