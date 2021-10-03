# Imports
import datetime
from typing import Optional, List
# Custom Imports
import bson

from data.models.car import Car
from data.models.engine import Engine
from data.models.owner import Owner
from data.models.service_record import ServiceRecord
from services.car_report_service import print_dissatisfaction_report, \
    print_dissatisfied_reports, print_report_all_cars


###############################################################################
# Create Records
###############################################################################
def create_owner(name: str) -> Owner:
    owner = Owner(name=name)
    owner.save()

    return owner


def create_car():
    bulk_add = input("Are you going to add more than one car? (y/n) ").lower()

    if bulk_add == "y":
        cars = []
        count = 0

        while True:
            car = create_car_details()
            cars.append(car)
            count += 1
            if count == 100:
                Car.objects().insert(cars)
                count = 0
                cars.clear()

            add_more = input("Would you like to add another car? (y/n) ").lower()
            if add_more != 'y':
                Car.objects().insert(cars)
                break
    else:
        car = create_car_details()
        car.save()

        print("Car added!")
        print()


def create_car_details() -> Car:
    make = input("What is the make? ")
    model = input("What is the model? ")
    year = int(input("Year built? "))
    mileage = float(input("Mileage? "))
    horsepower = int(input("What's the horsepower on the car? "))
    mpg = int(input("What's the miles per gallon? "))
    liters = int(input("How many liters is the gas tank? "))

    engine = Engine(horsepower=horsepower, mpg=mpg, liters=liters)
    car = Car(make=make, model=model, year=year, mileage=mileage, engine=engine)

    return car


###############################################################################
# Read Records
###############################################################################

# Car Records
def list_cars():
    cars = Car.objects().order_by("-year")
    if cars:
        print_report_all_cars(cars)
    else:
        print("No cars found on record.")
        print()


def find_car_by_id(car_id: bson.ObjectId):
    car = Car.objects(id=car_id).first()
    if car:
        print(car)
    else:
        print("No car found on record.")

    print()


def find_car_by_vin(vin: str) -> Car:
    car = Car.objects(vi_number=vin).first()

    return car


def show_poor_service_on_car():
    vin = input("What is the VIN of the car in question? ")
    car = find_car_with_bad_service(vin)
    if car is None:
        print("Car does not exist on our records.")
        print()
    else:
        print_dissatisfaction_report(car)


def show_all_poorly_serviced_cars():
    cars = find_cars_with_bad_service()
    if cars:
        print_dissatisfied_reports(cars)
    else:
        print("No cars found on record.")
        print()


def find_car_with_bad_service(vin: Optional[str]) -> Optional[Car]:
    car = Car.objects(service_history__customer_rating__lt=4).filter(vi_number=vin).first()
    return car


def find_cars_with_bad_service() -> Optional[List[Car]]:
    # JS Query: { "service_history.customer_rating" { $lt: level } }
    cars = Car.objects(service_history__customer_rating__lt=4)
    return list(cars)


# Owner Records
def find_owner_by_name(name) -> Owner:
    t0 = datetime.datetime.now()
    owner = Owner.objects(name=name).first()
    dt = datetime.datetime.now() - t0
    print(f"Owner found in {dt.total_seconds() * 1000} ms")

    return owner


###############################################################################
# Update Records
###############################################################################
def service_car():
    vin = input("What is the VIN of the car to service? ")
    price = float(input("What is the price? "))
    description = input("What type of service is this? ")
    customer_rating = int(input("How happy is our customer? [1-5] "))

    service = ServiceRecord(description=description, price=price, customer_rating=customer_rating)
    updated = Car.objects(vi_number=vin).update_one(push__service_history=service)

    if updated == 0:
        print(f"Car with VIN: '{vin}' not found!")
        print()

    car = find_car_by_vin(vin)
    if not car:
        print("Car does not exist on our records.")
    owner = Owner.objects().filter(car_ids=car.id).first()
    record_visit(owner.name)

    print()


def record_visit(customer):
    Owner.objects(name=customer).update_one(inc__number_of_visits=1)


def add_service_record(car_id, description, price, customer_rating):
    record = ServiceRecord(description=description, price=price, customer_rating=customer_rating)

    res = Car.objects(id=car_id).update_one(push__service_history=record)
    if res != 1:
        raise Exception("No car with id {}".format(car_id))


def add_owner(owner_id, car_id):
    res = Owner.objects(id=owner_id).update_one(add_to_set__car_ids=car_id)
    if res != 1:
        raise Exception("No owner with id {}".format(owner_id))
