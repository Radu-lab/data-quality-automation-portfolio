import re
import csv

def read_log(filepath):
    with open(filepath, 'r') as f:
        extracted = f.read()
        return extracted

def extract_errors(log_content):
    regex_pattern = r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) ERROR (.*)$'
    error_messages = re.findall(regex_pattern,log_content, re.MULTILINE)
    return error_messages

def count_errors(errors):
    count = {}
    for timestamp, error in errors:
        if error not in count:
            count[error] = 0
        count[error] += 1
    sorted_errors = sorted(count.items(), key=lambda x: x[1], reverse=True)
    return sorted_errors

def print_summary(sorted_errors, total):
    print(f"\n{'=' * 40}")
    print("LOG ANALYSIS SUMMARY")
    print(f"\nTotal errors found:{len(total)} ")
    print(f"\nTop errors by frequency: ")
    for error, freq in sorted_errors:
        print(f"  {error} - {freq}")
    print(f"\n{'=' * 40}")

def export_csv(sorted_errors, filepath):
    with open(filepath, 'w', encoding='utf-8', newline='') as cv:
        writer = csv.writer(cv)
        for error in sorted_errors:
            writer.writerow(error)

# with open("app.log",'r') as file:
#     extracted_file = file.read()
#     print(extracted_file)
#     regex_pattern = r'^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) ERROR (.*)$'
#     error_messages = re.findall(regex_pattern,extracted_file,re.MULTILINE)
#     print(error_messages)
#     count = {}
#     for timestamp,error in error_messages:
#         if error not in count:
#             count[error] = 0
#         count[error] +=1
#     print(count)
#     sorted_errors = sorted(count.items(),key = lambda x:x[1],reverse=True)
#     print(sorted_errors)
#     with open("logdata.csv",'w',encoding='utf-8',newline='') as cv:
#         writer = csv.writer(cv)
#         for error in sorted_errors:
#             writer.writerow(error)
#     print(f"\n{'='*40}")
#     print("LOG ANALYSIS SUMMARY")
#     print(f"\nTotal errors found:{len(error_messages)} ")
#     print(f"\nTop errors by frequency: ")
#     for error, freq in sorted_errors:
#         print(f"  {error} - {freq}")
#     print(f"\n{'='*40}")

log_content = read_log("app.log")
errors = extract_errors(log_content)
errors_sorted = count_errors(errors)
print_summary(errors_sorted,errors)
export_csv(errors_sorted,"logdata1.csv")