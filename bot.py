import re
import sys



phone_book = [{"name": "Dmytrii", "number": "+380983847085"}]

COMMANDS = ['show all', 'good bye', 'hello',
            'exit', 'close', 'add', 'change', 'phone']

DATA_FORMATS = {
    'phone': '^[+][0-9]{12}$'
}

chat_in_progress = True




def input_error(func):
    def inner_func(args):
        try:
            result = func(args)
            return result
        except KeyError:
            print("Assistant: Please, type a name in order to find a number")
        except IndexError:
            print("Assistant: Please, type name and number")
        except ValueError as err:
            print(err.args[0])
            return (None, None)
    return inner_func


def check_number_validity(number):
    valid_number = re.match(DATA_FORMATS['phone'], number)
    if not valid_number:
        raise ValueError("Assistant: Number should start with '+' and contain 12 digits. Please, try again")


def if_contact_exists(name):
    exists = None

    for person in phone_book:
        if person["name"] == name.title():
            exists = person
    return exists   


@input_error
def get_instruction(message):
    message = message.replace('You: ', '').lower()
    command_not_found = True

    for command in COMMANDS:
        if message.startswith(command):
            args = message.replace(command, '').strip().split(' ')
            command_not_found = False
            return (command, args)
    if command_not_found:
        raise ValueError(
            f"Please enter a valid command: {', '.join(COMMANDS)}")


def greet():
    print('Assistant: Hello. How can I assist you?')


def show_all_contacts():
    print('Assistant: Here are all your contacts: ')
    for contact in phone_book:
        print(f"\t{contact['name']}: {contact['number']}")


@input_error
def add_contact(args):
    person_data = args[1]
    check_number_validity(person_data[1])
    contact = if_contact_exists(person_data[0])

    if contact:
        print("Assistant: contact with such name alreday exists")
        return

    new_person = {'name': person_data[0].title(), 'number': person_data[1]}
    phone_book.append(new_person)
    print(
        f"Assistant: New contact {person_data[0].title()} with number {person_data[1]} has been successfully added")


@input_error
def get_number(args):
    found_person = {}

    for person in phone_book:
        if person["name"] == args[1][0].title():
            found_person = person
            print(f"Assistant: {found_person['number']}")

    if found_person == {}:
        print("Assistant: Person with such name was not found")


@input_error
def change_number(args):
    contact = if_contact_exists(args[1][0])

    if not contact:
        print("Assistant: Person with such name was not found")

    check_number_validity(args[1][1])
    contact["number"] = args[1][1]
    print(f"Assistant: {contact['name']}'s number was successfully changed to {contact['number']}.")

        


def terminate_assistant():
    global chat_in_progress
    print('Assistant: Bye. See you later ;)')
    chat_in_progress = False


while chat_in_progress:

    message = input("You: ")

    command_args = get_instruction(message)

    # print(command_args)

    match command_args[0]:
        case 'hello':
            greet()
        case "show all":
            show_all_contacts()
        case "phone":
            get_number(command_args)
        case 'add':
            add_contact(command_args)
        case 'change':
            change_number(command_args)

    if command_args[0] in ['close', 'exit', 'good bye']:
        terminate_assistant()
