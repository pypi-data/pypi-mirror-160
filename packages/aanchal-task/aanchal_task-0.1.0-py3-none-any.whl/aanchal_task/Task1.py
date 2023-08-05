from datetime import datetime

class Dummy:
    """Class with getter and setter functions for private attributes
    """
    def __init__(self, bias, baseline=1/3):
        """__init__ function of class Dummy

        Args:
            bias (int): private attribute
            baseline (float, optional): private attribute. Defaults to 1/3.
        """
        self.__bias = bias
        self.__baseline = baseline

    @property
    def get_bias(self):
        """Getter function to get the value of private variable bias

        Returns: value of bias
        """
        return self.__bias

    @property
    def get_baseline(self):
        """Getter function to get the value of private variable baseline

        Returns: value of baseline
        """
        return self.__baseline

    @get_baseline.setter
    def set_baseline(self, val):
        """Setter function for setting the value of baseline with the variable val

        Args:
            val (float): Value of baseline to set
        """
        self.__baseline = val

    def multiply(self, multiplier):
        """Performs the following operation : multiplier * baseline + bias

        Args:
            multiplier (int): value to be used in performing given operation

        Returns:
            float: value of the operation rounded up to 3 digits
        """
        return round(multiplier * self.get_baseline + self.get_bias, 3)
        
    def get_current_date(self):
        """Function to get the current data and time in a specific format

        Returns:
            datetime: Returns current data and time in the given format
        """
        date_time = datetime.now()
        return date_time.strftime("%H:%M:%S %d/%m/%Y")