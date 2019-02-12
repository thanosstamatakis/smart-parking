""" Module containing constants used in project. """


class ValidationNamespace():
    """ User validation constants class. """

    def __init__(self):
        """ Class constructor. """
        self.USER_EXISTS = 'User exists in DB.'
        self.WRONG_PASSWORD = 'Wrong Password.'
        self.UNKNOWN_USER = 'User does not exist.'
        self.VALIDATION_ERROR = 'Check users credentials.'
        self.USER_LOCATION_INPUT_ERROR = "Check user location's parameters."


class RegistrationNamespace():
    """ User registration constants class. """

    def __init__(self):
        """ Class constructor. """
        self.USERNAME_EXISTS = 'Username exists, try a different one.'
        self.REGISTRATION_ERROR = 'User was unsuccessfuly stored. Check users credentials again.'

    def get_correct_registration_message(self, username):
        """ Return correct registration message. """
        return f'User {username} is saved to db.'


class PlacemarkNamespace():
    """ Placemarks constants class. """

    def __init__(self):
        """ Class constructor. """
        self.DEMAND_ERROR = 'An error occured. Demand is not updated!'
        self.FILE_ERROR = 'File parsing was unsuccessful.'

    def get_correct_file_parsing_message(self, filename):
        """ Return string for correct file parsing. """
        return f'File {filename} was successfuly parsed.'

    def get_correct_demand_update_message(self, placemark):
        """ Return string for correct placemark's demand update. """
        return f'Demand of Placemark:{placemark} is updated!'

    def get_database_deletion_message(self, number_of_keys):
        """ Return string for deleting all placemark keys from database. """
        return f'{number_of_keys} keys deleted from database.'


PLACEMARK_NAMESPACE = PlacemarkNamespace()
VALIDATION_NAMESPACE = ValidationNamespace()
REGISTRATION_NAMESPACE = RegistrationNamespace()
