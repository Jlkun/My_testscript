

import turtle



# to_test_person_list = [{"person": {"name": "kevin", "country": "cn",   "traveled": "no"}, "test": 0},{"person": {"name": "Alex", "country": "us", "traveled": "yes"}, "test": 0}]
#
# def covid19_test(person_list):
#         return [ person['person']['name'] for person in person_list if person['test'] == 0 ]
#
# if __name__ == "__main__":
#     print(covid19_test(to_test_person_list))


def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum

print (calc(1,2,3)) #14