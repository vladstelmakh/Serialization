
from datetime import date
import pickle
class Field:
    def __init__(self, value=None):
        self._value = value

    def set_value(self, value):
        self._value = value

    def get_value(self):
        return self._value


class Phone:
    def __init__(self, value):
        self._value = None
        self.set_value(value)

    def set_value(self, value):
        if self.is_valid_phone(value):
            self._value = value
        else:
            raise ValueError("Недійсний номер телефону")

    def get_value(self):
        return self._value

    def is_valid_phone(self, value):
        return len(value) == 10 and value.isdigit()



class Birthday:
    def __init__(self, value=None):
        self._value = None
        self.set_value(value)

    def set_value(self, value):
        if self.is_valid_date(value):
            self._value = value
        else:
            raise ValueError("Некоректна дата народження")

    def get_value(self):
        return self._value

    def is_valid_date(self, value):
        return value is not None

    def days_to_birthday(self):
        if self._value:
            today = date.today()
            next_birthday = date(today.year, self._value.month, self._value.day)
            if next_birthday < today:
                next_birthday = date(today.year + 1, self._value.month, self._value.day)
            return (next_birthday - today).days
        return None


class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = name
        self.phone = Phone(phone)
        self.birthday = Birthday(birthday)




class AddressBook:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        if not isinstance(record, Record):
            raise TypeError("Об’єкт не є екземпляром класу Record")

        self.records.append(record)

    def remove_record(self, record):
        self.records.remove(record)

    def iterator(self, page_size):
        num_pages = (len(self.records) + page_size - 1) // page_size
        for page in range(num_pages):
            start = page * page_size
            end = start + page_size
            yield self.records[start:end]

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.records, file)

    def load_from_file(self, filename):
        with open(filename, 'rb') as file:
            self.records = pickle.load(file)

    def search(self, query):
        results = []
        for record in self.records:
            if query.lower() in record.name.lower() or query in record.phone.get_value():
                results.append(record)
        return results

def main():
    address_book = AddressBook()
    address_book.add_record(Record("John Doe", "3434567895", date(1991, 5, 11)))
    address_book.add_record(Record("Jane Smith", "1276543211", date(1982, 4, 20)))

    address_book.save_to_file("address_book.pkl")
    print("Адресна книга збережена.")

    loaded_address_book = AddressBook()
    loaded_address_book.load_from_file("address_book.pkl")
    print("Адресна книга завантажується.")

    results = loaded_address_book.search("Doe")
    for record in results:
        print(record.name, record.phone.get_value())

if __name__ == '__main__':
    main()