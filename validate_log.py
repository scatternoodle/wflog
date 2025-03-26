import re
import sys
import csv

def get_emp_from_line(line: str) -> str:
    match = re.match(r'(?i).*Validation error for employee (\w+).*', line)
    if match:
        return match.group(1)
    match = re.match(r'(?i).*Error occurred while importing employee with Id (\w+).*', line)
    if match:
        return match.group(1)
    match = re.match(r'(?i).*app user login_id =\'(\w+).*', line)
    if match:
        return match.group(1)
    return ''


def write_dict_to_csv(data: dict, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, quoting=csv.QUOTE_ALL)
        for key, value in data.items():
            writer.writerow([key, value])

def get_error_data(file_name, print_unhandled):
    error_data: dict[str, str] = {}
    current_emp: str = ""
    unhandled_errors = []
    with open(file_name) as file:
        for line in file:
            line = line.strip('\n')
            if not line.startswith('[ERR'):
                continue
            
            if line.startswith('[ERR_DTL]'):
                if not current_emp:
                    continue
                error_data[current_emp] += '\n' + line
                continue
            
            current_emp = get_emp_from_line(line)
            if not current_emp:
                unhandled_errors.append(line)
                continue

            if not error_data.get(current_emp):
                error_data[current_emp] = ''
            error_data[current_emp] += line.strip()

    if print_unhandled:
        print('unhandled errors:')
        for err in unhandled_errors:
            print(err)

    return error_data

def main():
    if len(sys.argv) < 3:
        print("usage: INPUT_FILE OUTPUT_FILE")
        exit(1)
    input_filename = sys.argv[1]
    output_filename = sys.argv[2]
    

    error_data = get_error_data(input_filename, True)
    write_dict_to_csv(error_data, output_filename)


main()

