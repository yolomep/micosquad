import easygui
import tkinter as tk
from easygui import global_state

class Mico_GUItk(easygui.GUItk):
    def __init__(self, msg, title, fields, values, ok_button, mask_last, callback):
        self.ok_button = ok_button
        super().__init__(msg, title, fields, values, mask_last, callback)
    
    
    def create_ok_button(self):

        okButton = tk.Button(self.buttonsFrame, takefocus=1, text=self.ok_button)
        self.bindArrows(okButton)
        okButton.pack(expand=1, side=tk.LEFT, padx='3m', pady='3m',
                      ipadx='2m', ipady='1m')

        # for the commandButton, bind activation events to the activation event
        # handler
        commandButton = okButton
        handler = self.ok_pressed
        for selectionEvent in global_state.STANDARD_SELECTION_EVENTS:
            commandButton.bind("<%s>" % selectionEvent, handler)


class Mico_MultiBox(easygui.MultiBox):
    def __init__(self, msg, title, fields, values, ok_button, mask_last, callback):
        """ Create box object

        Parameters
        ----------
        msg : string
            text displayed in the message area (instructions...)
        title : str
            the window title
        fields: list
            names of fields
        values: list
            initial values
        callback: function
            if set, this function will be called when OK is pressed
        run: bool
            if True, a box object will be created and returned, but not run

        Returns
        -------
        self
            The MultiBox object
        """
        self.callback = callback

        self.fields, self.values = self.check_fields(fields, values)

        self.ui = Mico_GUItk(msg, title, self.fields, self.values, ok_button,
                        mask_last, self.callback_ui)


def mico_multenterbox(msg="Fill in values for the fields.", title=" ",
                 fields=[], values=[], ok_button="OK", callback=None):
    r"""
    Show screen with multiple data entry fields.

    If there are fewer values than names, the list of values is padded with
    empty strings until the number of values is the same as the number
    of names.

    If there are more values than names, the list of values
    is truncated so that there are as many values as names.

    Returns a list of the values of the fields,
    or None if the user cancels the operation.

    Here is some example code, that shows how values returned from
    multenterbox can be checked for validity before they are accepted::

        msg = "Enter your personal information"
        title = "Credit Card Application"
        fieldNames = ["Name","Street Address","City","State","ZipCode"]
        fieldValues = []  # we start with blanks for the values
        fieldValues = multenterbox(msg,title, fieldNames)

        # make sure that none of the fields was left blank
        while 1:
            if fieldValues is None: break
            errmsg = ""
            for i in range(len(fieldNames)):
                if fieldValues[i].strip() == "":
                    errmsg += ('"%s" is a required field.\n\n' % fieldNames[i])
            if errmsg == "":
                break # no problems found
            fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)

        print("Reply was: %s" % str(fieldValues))

    :param str msg: the msg to be displayed.
    :param str title: the window title
    :param list fields: a list of fieldnames.
    :param list values: a list of field values
    :return: String
    """
    mb = Mico_MultiBox(msg, title, fields, values, ok_button, mask_last=False,
                    callback=callback)
    
    
    reply = mb.run()
    return reply
