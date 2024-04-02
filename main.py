import pandas as pd


df = pd.read_csv("hotels.csv", dtype={"id": str})
df_creditcard = pd.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_card_security = pd.read_csv("card_security.csv", dtype=str)


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def book(self):
       """Book a hotel by changing its availability to no"""
       df.loc[df["id"] == self.hotel_id, "available"] = "no"
       df.to_csv("hotels.csv", index=False)

    def available(self):
        """Check if the hotel is available"""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False


class Reservation: 
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for your reservation!
        Here are your booking data:
        Name: {self.customer_name}
        Hotel name: {self.hotel.name}
        """
        return content


class CreditCard:
    def __init__(self, number):
        self.number = number
       
    def validate(self, expiration, holder, cvc):
        card_data = {"number": self.number, "expiration": expiration, "cvc": cvc, "holder": holder }
        if card_data in df_creditcard: 
            return True
        else:
            return False


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password):
        password = df_card_security.loc[df_card_security["number"] == self.number, "password"].squeeze()
        if password == given_password:
            return True
        else:
            return False


class Spa(Reservation):
    def reserve_spa(self, spa_reservation):
        if spa_reservation == "yes":
            content = f"""
            Thank you for your reservation!
            Here are your SPA reservation:
            Name: {self.customer_name}
            Hotel name: {self.hotel.name}
            """
            return content
        else:
            return "Enjoy your stay"
                


print(df)
hotel_id = input("Enter the id of the hotel:")
hotel = Hotel(hotel_id)


if hotel.available():
    credit_card = SecureCreditCard(number="1234")
    if credit_card.validate(expiration="12/26", holder="JOHN SMITH", cvc="123"):
        if credit_card.authenticate(given_password = "mypass"): 
            hotel.book()
            name = input("Enter your name:")
            reservation = Reservation(customer_name= name, hotel_object= hotel)
            print(reservation.generate())
            spa = Spa(customer_name = name, hotel_object= hotel)
            spa_reservation = input("Would you like to reserve a place in our spa?: ")
            print(spa.reserve_spa(spa_reservation))
        else: 
            print("Credit card authentication failed")
    else:
       print("There is a problem with your payment method")
else:
    print("Hotel is not available")