# Imports
from typing import Optional, List
# Custom Imports
from data.models.car import Car
from data.models.engine import Engine
from data.models.service_history import ServiceHistory
from services.car_report_service import print_dissatisfaction_report, \
    print_dissatisfied_reports, print_report_all_cars


def add_car():
    bulk_add = input("Are you going to add more than one car? (y/n) ").lower()

    if bulk_add == "y":
        cars = []
        count = 0

        while True:
            car = add_car_details()
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
        car = add_car_details()
        car.save()

        print("Car added!")
        print()


def add_car_details() -> Car:
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


def list_cars():
    cars = Car.objects().order_by("-year")
    if cars:
        print_report_all_cars(cars)
    else:
        print("No cars found on record.")
        print()


def find_car():
    print("TODO: find_car")
    print()


def service_car():
    vin = input("What is the VIN of the car to service? ")
    price = float(input("What is the price? "))
    description = input("What type of service is this? ")
    customer_rating = int(input("How happy is our customer? [1-5] "))

    service = ServiceHistory(description=description, price=price, customer_rating=customer_rating)
    updated = Car.objects(vi_number=vin).update_one(push__service_history=service)

    if updated == 0:
        print(f"Car with VIN: '{vin}' not found!")
        print()

    print()


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
