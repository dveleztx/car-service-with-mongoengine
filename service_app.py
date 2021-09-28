# Custom Imports
import nosql.mongo_setup as mongo_setup
from nosql.car import Car
from nosql.engine import Engine
from nosql.service_history import ServiceHistory


def main():
    print_header()
    config_mongo()
    user_loop()


def print_header():
    print('-----------------------------------------------')
    print('|                                             |')
    print('|           SERVICE CENTRAL v.02              |')
    print('|               demo edition                  |')
    print('|                                             |')
    print('-----------------------------------------------')
    print()


def config_mongo():
    mongo_setup.global_init()


def user_loop():
    while True:
        print("Available actions:")
        print(" * [a]dd car")
        print(" * [l]ist cars")
        print(" * [p]oorly serviced")
        print(" * [f]ind car")
        print(" * perform [s]ervice")
        print(" * e[x]it")
        print()
        ch = input("> ").strip().lower()
        if ch == 'a':
            add_car()
        elif ch == 'l':
            list_cars()
        elif ch == 'p':
            show_poorly_serviced_cars()
        elif ch == 'f':
            find_car()
        elif ch == 's':
            service_car()
        elif not ch or ch == 'x':
            print("Goodbye")
            break


def add_car():
    model = input("What is the model? ")
    make = "Ferrari" # input("What is the make? ")
    year = int(input("Year built? "))
    mileage = float(input("Mileage? "))

    car = Car()
    car.year = year
    car.make = make
    car.model = model
    car.mileage = mileage

    engine = Engine()
    engine.horsepower = 500
    engine.mpg = 26
    engine.liters = 4.0
    car.engine = engine

    car.save()

    print()


def list_cars():
    cars = Car.objects().order_by("-year")
    for car in cars:
        print(f"{car.make} -- {car.model} with vin {car.vi_number} (year {car.year})")
        print(f"{len(car.service_history)} service records found: ")
        for s in car.service_history:
            print(f"   * ${s.price:,.02f} {s.description}")
    print()


def find_car():
    print("TODO: find_car")
    print()


def service_car():
    # vin = input("What is the VIN of the car to service? ")
    # car = Car.objects(vi_number=vin).first()
    # if not car:
    #     print(f"Car with VIN: '{vin}' not found!")
    #     print()
    #     return
    #
    # print(f"We will service {car.model}")
    # service = ServiceHistory()
    # service.price = float(input("What is the price? "))
    # service.description = input("What type of service is this? ")
    # service.customer_rating = int(input("How happy is our customer? [1-5] "))
    #
    # car.service_history.append(service)
    # car.save()

    vin = input("What is the VIN of the car to service? ")
    service = ServiceHistory()
    service.price = float(input("What is the price? "))
    service.description = input("What type of service is this? ")
    service.customer_rating = int(input("How happy is our customer? [1-5] "))

    updated = Car.objects(vi_number=vin).update_one(push__service_history=service)
    if updated == 0:
        print(f"Car with VIN: '{vin}' not found!")
        print()

    print()


def show_poorly_serviced_cars():
    level = int(input("What max level of satisfaction are we looking for? [1-5] "))

    # JS Query: { "service_history.customer_rating" { $lte: level } }
    cars = Car.objects(service_history__customer_rating__lte=level)
    for car in cars:
        print(f"{car.make} -- {car.model} with vin {car.vi_number} (year {car.year})")
        print(f"{len(car.service_history)} service records found: ")
        for s in car.service_history:
            print(f"  * Satisfaction: {s.customer_rating} ${s.price:,.0f} {s.description}")
    print()


if __name__ == '__main__':
    main()
