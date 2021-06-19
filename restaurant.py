class Restaurant(object):
    def __init__(self, name, address, phone):
        self.name = name
        self.address = address
        self.phone = phone

    def __eq__(self, other):
        return self.name == other.name \
            and self.address == other.address \
            and self.phone == other.phone

    def __ne__(self, other):
        return self.name != other.name \
               or self.address != other.address \
               or self.phone != other.phone

    def __hash__(self):
        return hash((self.name, self.address, self.phone))