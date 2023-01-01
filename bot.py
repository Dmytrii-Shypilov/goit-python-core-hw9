import sys

phone_book = [{"name": "Dmytrii", "number": "+380983847085" }]

COMMANDS = ['show all', 'good bye', 'hello', 'exit', 'close', 'add', 'change', 'phone']

DATA_FORMATS = {
    'name': '[A-Z]{1}[a-z]+',
    'phone': '[+][0-9]{12}'
}

chat_in_progress = True



def get_instruction(message):
    message.replace('You: ', '')
    command_not_found = True
    for command in COMMANDS:
        if message.startswith(command):
            args = message.replace(command, '').strip().split(' ')
            command_not_found = False
            # print(f'command: {command}, args: {args}')
            return command, args
    if command_not_found:
        raise ValueError(f"Please enter a valid command: {', '.join(COMMANDS['all'])}")


def input_error(func):
    try:
        func()
    except KeyError:
        print()


def greet():
        print('Assistant: Hello. How can I assist you?')

def show_all_contacts():
    for contact in phone_book:
        print(f"{contact['name']}: {contact['number']}")

def add_contact(args):
    phone_book[args[0]] = phone_book[args[1]]

def get_number(args):
    print(args)
    found_person = {}
    for person in phone_book:
        if person["name"] == args[1][0]:
            found_person = person
    print(f"Assitant: {found_person['number']}")


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
        

    if command_args[0] in ['close', 'exit', 'good bye']:
        terminate_assistant()

