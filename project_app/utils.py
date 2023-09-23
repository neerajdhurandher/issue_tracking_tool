from dateutil.parser import isoparse


class Utils():
    def validate_datetime_format(date_string):
        """
        Validates if a given date string is in ISO-8601 format.

        Parameters:
        - date_string (str): The date string to validate.

        Returns:
        - bool: True if the date string is in ISO-8601 format, False otherwise.
        """
        try:
            isoparse(date_string)
            return True
        except ValueError:
            return False

    def get_object_by_id(ObjectModel, id):
        """This function is used for get any model object from DB using its id

        Args:
            ObjectModel (class): Class of the model which want to be retrieve
            id (string): unique id 

        Returns:
            object : Object with two item
            -status (boolean): based on object exists with given id
            -data : object data if status true , else error message

        """
        try:
            object = ObjectModel.objects.get(id=id)
            object_data = object.__dict__
            del object_data['_state']
            return ({'status': True, 'data': object_data})
        except ObjectModel.DoesNotExist:
            return ({'status': False, "error": "The {} does not exist"})
