import sys
import re

# m = re.match(r"(\w+) (\w+)", "Isaac Newton, physicist")

phone_book = [{"name": "Dmytrii", "number": "+380983847085" }]

COMMANDS = ['show all', 'good bye', 'hello', 'exit', 'close', 'add', 'change', 'phone']

DATA_FORMATS = {
    'name': '[A-Z]{1}[a-z]+',
    'phone': '[+][0-9]{12}'
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

@input_error
def get_instruction(message):
    message.replace('You: ', '').lower()
    command_not_found = True
    for command in COMMANDS:
        if message.startswith(command):
            args = message.replace(command, '').strip().split(' ')
            command_not_found = False
            # print(f'command: {command}, args: {args} {command_not_found}')
            return(command, args)
    if command_not_found:
        raise ValueError(f"Please enter a valid command: {', '.join(COMMANDS)}")




def greet():
        print('Assistant: Hello. How can I assist you?')

def show_all_contacts():
    print('Assistant: Here are all your contacts')
    for contact in phone_book:
        print(f"\t{contact['name']}: {contact['number']}")

@input_error
def add_contact(args):
    person_data = args[1]
    new_person = {'name': person_data[0].title(), 'number': person_data[1]}
    phone_book.append(new_person)
    print(f"Assistant: New contact {person_data[0].title()} with number {person_data[1]} has been successfully added")

@input_error
def get_number(args):
    found_person = {}
    for person in phone_book:
        if person["name"] == args[1][0]:
            found_person = person
    print(f"Assistant: {found_person['number']}")

def change_number(args):
    for person in phone_book:
        if person["name"] == args[1][0]:
            person["number"] = args[1][1]
    

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

