# Custom Imports
import data.mongo_setup as mongo_setup
from services import car_service


def main():
    print_header()
    config_mongo()
    # update_doc_versions()
    user_loop()


def print_header():
    print('-----------------------------------------------')
    print('|                                             |')
    print('|           SERVICE CENTRAL v.08              |')
    print('|               Demo Edition                  |')
    print('|                                             |')
    print('-----------------------------------------------')
    print()


def config_mongo():
    mongo_setup.global_init()


# def update_doc_versions():
#     for car in Car.objects():
#         car._mark_as_changed('vi_number')
#         car.save()


def user_loop():
    while True:
        print("Available actions:")
        print(" * [a]dd car")
        print(" * [l]ist cars")
        print(" * [f]ind car")
        print(" * perform [s]ervice")
        print(" * [p]oorly serviced")
        print(" * all [d]is-satisfied ratings")
        print(" * e[x]it")
        print()
        ch = input("> ").strip().lower()
        if ch == 'a':
            car_service.create_car()
        elif ch == 'l':
            car_service.list_cars()
        elif ch == 'f':
            car_service.find_car_by_id()
        elif ch == 's':
            car_service.service_car()
        elif ch == 'p':
            car_service.show_poor_service_on_car()
        elif ch == 'd':
            car_service.show_all_poorly_serviced_cars()
        elif not ch or ch == 'x':
            print("Goodbye")
            break


if __name__ == '__main__':
    main()
