numbers = [23, 21, 63, 4, 531, 6]
names = ['eden', 'hugo', 'john', 'sally']

nameAgeDict = {
    'eden': 27,
    'hugo': 20,
    'john': 52,
    'sally': 7,
}

i = 0
# for number in numbers:
#     # print(f'{i}:{number}')
#     i += 1

# for i in range(len(numbers)):
#     # print(f'{i}:{numbers[i]}')

# for i, number in enumerate(numbers):
#     # print(f'{i}:{number}')

# for name in names:
#     print(name)

# for number, name in zip(numbers, names):
#     print(number, name)

print(nameAgeDict.values())

for age in nameAgeDict.values():
    print(age)