def numbers_up_to01(max_number):
    output = []

    for number in range(max_number + 1):
        output.append(number)

    return output
def numbers_up_to(max_number):
    for number in range(max_number + 1):
        yield number
# print(list(numbers_up_to(4)))