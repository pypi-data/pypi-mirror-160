from steam_sdk.data import DataDAKOTA as dDAKOTA

class BuilderDAKOTA:
    '''

    '''


    def __init__(self, input_DAKOTA_data: dDAKOTA.DAKOTA_analysis = None, verbose: bool = True):
            """
            Object is initialized by defining DAKOTA variable structure and file template.
            If verbose is set to True, additional information will be displayed
            """
            # Unpack arguments
            self.verbose: bool = verbose
            self.input_DAKOTA_data: dDAKOTA.DAKOTA_analysis = input_DAKOTA_data

            return

