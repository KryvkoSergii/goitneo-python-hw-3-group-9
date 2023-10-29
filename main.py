from objects import IncorrectPhoneFormatException, IncorrectNameException, UnableToEditPhoneException, Name, Phone, Email, Record, AddressBook, Birthday, BirthdayFormatException


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "Unable to find record"
        except TypeError as e:
            return f"Internal error. Contact developer {e}" 
        except IncorrectPhoneFormatException as err:
            return err
        except IncorrectNameException as err:
            return err
        except UnableToEditPhoneException as err:
            return err
        except BirthdayFormatException as err:
            return err
    return inner


def parse_input(user_input):
    cmd, *args = user_input.split(" ")
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(address_book: AddressBook, args):
    name, phone = args
    name_obj = Name(name)
    record_obj = Record(name_obj)

    phone_obj = Phone(phone)
    record_obj.add_phone(phone_obj)

    address_book.add_record(record_obj)
    return "Contact added."


def find_contact(name: str, address_book: AddressBook) -> Record:
    found = address_book.find(Name(name))
    if not found:
        raise KeyError
    return found


@input_error
def add_phone(address_book: AddressBook, args):
    name, phone = args
    phones = phone.split(",")
    name_obj = Name(name)
    record: Record = find_contact(name_obj, address_book)
    for ph in phones:
        record.add_phone(Phone(ph))
    return "Phone/s added."


@input_error
def remove_phone(address_book: AddressBook, args):
    name, phone = args
    record: Record = find_contact(name, address_book)
    record.remove_phone(Phone(phone))
    return "Phone removed."


@input_error
def get_phone(address_book: AddressBook, args):
    name = args[0]
    record: Record = find_contact(name, address_book)
    phones = list(map(lambda r: str(r), record.phones))
    return ", ".join(phones)


@input_error
def edit_phone(address_book: AddressBook, args):
    name, old_phone, new_phone = args
    record: Record = find_contact(name, address_book)
    phones = list(filter(lambda r: str(r) == str(old_phone), record.phones))
    if phones:
        to_edit: Phone = phones[0]
        to_edit.update_value(new_phone)
        return "Phone changed."
    else:
        raise UnableToEditPhoneException(old_phone)


@input_error
def add_email(address_book: AddressBook, args):
    name, email = args
    record: Record = find_contact(name, address_book)
    record.email = Email(email)
    return "Email added."


@input_error
def change_email(address_book: AddressBook, args):
    name, email = args
    record: Record = find_contact(name, address_book)
    record.email = Email(email)
    return "Email changed."


@input_error
def remove_email(address_book: AddressBook, args):
    name = args[0]
    record: Record = find_contact(name, address_book)
    record.add_email(None)
    return "Email removed."


@input_error
def remove(address_book: AddressBook, args):
    name = Name(args[0])
    address_book.delete(name)
    return "Removed."

@input_error
def add_birthday(address_book: AddressBook, args):
    name, birthday = args
    record: Record = find_contact(name, address_book)
    try:
        record.add_birthday(Birthday(birthday))
        return "Birthday added."
    except ValueError:
        raise BirthdayFormatException(birthday)


@input_error
def show_birthday(address_book: AddressBook, args):
    name = args[0]
    record: Record = find_contact(name, address_book)
    return  record.birthday if record.birthday else "Birthday is not provided yet. Please add birthday"
    

def get_all(address_book: AddressBook):
    print(f"{'_'*135}")
    print(f"|{'Name:':^40}|{'Phone:':^30}|{'Email:':^30}|{'Birthday:':^30}|")
    print(f"|{'_'*40}|{'_'*30}|{'_'*30}|{'_'*30}|")
    if len(address_book.data) > 0:
        for record in address_book.data:
            print(f"|{str(record.name):^40}|{', '.join(list(map(lambda rec: str(rec), record.phones))):^30}|{str(record.email) if record.email else '':^30}|{str(record.birthday) if record.birthday else '':^30}|")
            print(f"|{'_'*40}|{'_'*30}|{'_'*30}|{'_'*30}|")
    else:
        print(f"|{' '*133}|")
        print(f"|{'No records found. Add at first':^133}|")
        print(f"|{'_'*133}|")

def birthdays(address_book: AddressBook):
    birthday_dict = address_book.get_birthdays_per_week()
    print(f"{'_'*73}")
    print(f"|{'Day:':^30}|{'Name:':^40}|")
    print(f"|{'_'*30}|{'_'*40}|")
    if birthday_dict:
        for day, list_of_records in birthday_dict.items():
            print(f"|{day:^30}|{', '.join(list(map(lambda rec: str(rec.name), list_of_records))):^40}|")
            print(f"|{'_'*30}|{'_'*40}|")
    else:
        print(f"|{' '*71}|")
        print(f"|{'No matches found.':^71}|")
        print(f"|{'_'*71}|")

help = """
Available commands:
Exit - 'close' or 'exit'
Start work - 'hello'
Add new contact - 'add' <name without spaces> <phone>
Add new phone - 'add-phone' <name without spaces> <phone1>,<phone2>,...
Remove phone - 'remove-phone' <name without spaces> <phone>
Edit phone - 'edit-phone' <name without spaces> <phone-to-change> <phone-new>
Get all phones for contact - 'get-phone' <name without spaces>
Add email - 'add-email' <name without spaces> <email>
Change email - 'change-email' <name without spaces> <email>
Remove email - 'remove-email' <name without spaces>
Add/change Birthday - 'add-birthday' <name without spaces> <date in format DD.MM.YYYY>
Get Birthday of contact - 'show-birthday' <name without spaces>
Get list of contacts to be congratulated next week - 'birthdays'
Remove contact - 'remove' <name without spaces> 
Print all contacts - 'all'            
        """
 
def main():
    address_book = AddressBook()
    print("Welcome to the assistant bot!")
    print(help)
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)
        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(address_book, args))
        elif command == "add-phone":
            print(add_phone(address_book, args))
        elif command == "remove-phone":
            print(remove_phone(address_book, args))
        elif command == "edit-phone":
            print(edit_phone(address_book, args))
        elif command == "get-phone":
            print(get_phone(address_book, args))
        elif command == "add-email":
            print(add_email(address_book, args))
        elif command == "change-email":
            print(change_email(address_book, args))
        elif command == "remove-email":
            print(remove_email(address_book, args))
        elif command == "add-birthday":
            print(add_birthday(address_book, args))
        elif command == "show-birthday":
            print(show_birthday(address_book, args))
        elif command == "birthdays":
            birthdays(address_book)
        elif command == 'remove':
            print(remove(address_book, args))
        elif command == "all":
            get_all(address_book)
        elif command == "help":
            print(help)
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
