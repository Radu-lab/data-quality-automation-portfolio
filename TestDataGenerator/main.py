import random
import csv
from faker import Faker

fake = Faker()
#first_names = ['John', 'Emma', 'Ryan', 'Lilly', 'Bobby', 'Linda', 'Sergio', 'Alina']
#last_names = ['Watson', 'Morrison', 'Benson', 'Gosling', 'Neston', 'Ramos', 'Hamilton']
domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'company.org']


def write_column_names(writer):
        writer.writerow(['id','first_name','last_name','email','signup_date','purchase_amount'])

def add_rows(i):
    first = fake.first_name()
    last = fake.last_name()
    email = f"{first.lower()}.{last.lower()}@{random.choice(domains)}"
    date = fake.date_between(start_date='-5y',end_date='today').strftime('%Y-%m-%d')
    amount = round(random.uniform(1, 500), 2)
    return [i,first,last,email,date,amount]

def save_to_file(filepath, num_rows):
    with open(filepath,'w',newline='') as f:
        writer = csv.writer(f)
        write_column_names(writer)
        for i in range(1,num_rows+1):
            row = add_rows(i)
            if random.random() < 0.15:  # finger points — hit or miss?
                row = corrupt_rows(row)
            writer.writerow(row)

def corrupt_rows(row):
    field = random.randint(1,5)
    if field == 1:
        row[1] = ''
    elif field == 2:
        row[3] = 'not-an-email'
    elif field == 3:
        row[4] = '2099-13-45'
    elif field == 4:
        row[5] = -50
    elif field == 5:
        row[2] = 'A' * 500
    return row

save_to_file('test_data.csv', 100)
print("Done")


