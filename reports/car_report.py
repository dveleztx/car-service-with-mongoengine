# Imports
from typing import List, Optional
# Custom Imports
from data.models.car import Car


def print_car_report(car: Car):
    print("-" * 79)
    print(f"- {car.year} {car.make} {car.model} -- VIN: {car.vi_number}")
    if len(car.service_history) == 0:
        print("  No service history found.")
        print()


def print_report_all_cars(cars: List[Car]):
    print("-" * 79)
    for car in cars:
        print(f"- {car.year} {car.make} {car.model} -- VIN: {car.vi_number}")
        if len(car.service_history) == 0:
            print("  No service history found.")
            print()
        else:
            print(f"  {len(car.service_history)} service records found: ")
            for s in car.service_history:
                print(f"    * {s.description.title()} ${s.price:,.02f}")
            print()
    print("-" * 79)
    print()


def print_dissatisfaction_report(car: Car):
    print(f"Car: {car.year} {car.make} {car.model}")
    print(f"{len(car.service_history)} service records found: ")
    for s in car.service_history:
        if s.customer_rating < 4:
            print(f"  * Satisfaction: {s.customer_rating} - Details: {s.description.title()} (${s.price:,.02f})")
            print()


def print_dissatisfied_reports(cars: List[Car]):
    for car in cars:
        print(f"- {car.year} {car.make} {car.model} -- VIN: {car.vi_number}")
        print(f"  {len(car.service_history)} service records found: ")
        for s in car.service_history:
            if s.customer_rating < 4:
                print(f"\t* Satisfaction: {s.customer_rating} - Details: {s.description.title()} (${s.price:,.02f})")
    print()
