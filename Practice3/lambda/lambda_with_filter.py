numbers = [1, 2, 3, 4, 5, 6, 7, 8]
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(odd_numbers)  # [1, 3, 5, 7]

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)  # [2, 4, 6, 8, 10]

emails = [
    'user@gmail.com',
    'admin@yahoo.com',
    'test@gmail.com',
    'info@outlook.com'
]
gmail_only = list(filter(lambda email: '@gmail.com' in email, emails))
print(gmail_only)

