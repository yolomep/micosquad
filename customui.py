import easygui
import tkinter as tk


window_position = "+350+200"

PROPORTIONAL_FONT_FAMILY = ("MS", "Sans", "Serif")
MONOSPACE_FONT_FAMILY = "Courier"

PROPORTIONAL_FONT_SIZE = 10
# a little smaller, because it is more legible at a smaller size
MONOSPACE_FONT_SIZE = 9
TEXT_ENTRY_FONT_SIZE = 12  # a little larger makes it easier to see


STANDARD_SELECTION_EVENTS = ["Return", "Button-1", "space"]

prop_font_line_length = 62
fixw_font_line_length = 80
num_lines_displayed = 50
default_hpad_in_chars = 2

class GUItk(object):

    """ This object contains the tk root object.
        It draws the window, waits for events and communicates them
        to MultiBox, together with the entered values.

        The position in wich it is drawn comes from a global variable.

        It also accepts commands from Multibox to change its message.
    """

    def __init__(self, msg, title, fields, values, mask_last, callback):

        self.callback = callback

        self.boxRoot = tk.Tk()

        self.create_root(title)

        self.set_pos(window_position)  # GLOBAL POSITION

        self.create_msg_widget(msg)

        self.create_entryWidgets(fields, values, mask_last)

        self.create_buttons()

        self.entryWidgets[0].focus_force()  # put the focus on the entryWidget

    # Run and stop methods ---------------------------------------

    def run(self):
        self.boxRoot.mainloop()  # run it!
        self.boxRoot.destroy()   # Close the window

    def stop(self):
        # Get the current position before quitting
        self.get_pos()

        self.boxRoot.quit()

    def x_pressed(self):
        self.callback(self, command='x', values=self.get_values())

    def cancel_pressed(self, event):
        self.callback(self, command='cancel', values=self.get_values())

    def ok_pressed(self, event):
        self.callback(self, command='update', values=self.get_values())

    # Methods to change content ---------------------------------------

    def set_msg(self, msg):
        self.messageWidget.configure(text=msg)
        self.entryWidgets[0].focus_force()  # put the focus on the entryWidget

    def set_pos(self, pos):
        self.boxRoot.geometry(pos)

    def get_pos(self):
        # The geometry() method sets a size for the window and positions it on
        # the screen. The first two parameters are width and height of
        # the window. The last two parameters are x and y screen coordinates.
        # geometry("250x150+300+300")
        geom = self.boxRoot.geometry()  # "628x672+300+200"
        window_position = '+' + geom.split('+', 1)[1]

    def get_values(self):
        values = []
        for entryWidget in self.entryWidgets:
            values.append(entryWidget.get())
        return values

    # Initial configuration methods ---------------------------------------
    # These ones are just called once, at setting.

    def create_root(self, title):

        self.boxRoot.protocol('WM_DELETE_WINDOW', self.x_pressed)
        self.boxRoot.title(title)
        self.boxRoot.iconname('Dialog')
        self.boxRoot.bind("<Escape>", self.cancel_pressed)
        self.boxRoot.attributes("-topmost", True)  # Put the dialog box in focus.

    def create_msg_widget(self, msg):
        # -------------------- the msg widget ----------------------------
        self.messageWidget = tk.Message(self.boxRoot, width="4.5i", text=msg)
        self.messageWidget.configure(
            font=(PROPORTIONAL_FONT_FAMILY, PROPORTIONAL_FONT_SIZE))
        self.messageWidget.pack(
            side=tk.TOP, expand=1, fill=tk.BOTH, padx='3m', pady='3m')

    def create_entryWidgets(self, fields, values, mask_last):

        self.entryWidgets = []

        lastWidgetIndex = len(fields) - 1

        for widgetIndex in range(len(fields)):
            name = fields[widgetIndex]
            value = values[widgetIndex]
            entryFrame = tk.Frame(master=self.boxRoot)
            entryFrame.pack(side=tk.TOP, fill=tk.BOTH)

            # --------- entryWidget -------------------------------------------
            labelWidget = tk.Label(entryFrame, text=name)
            labelWidget.pack(side=tk.LEFT)

            entryWidget = tk.Entry(entryFrame, width=40, highlightthickness=2)
            self.entryWidgets.append(entryWidget)
            entryWidget.configure(
                font=(PROPORTIONAL_FONT_FAMILY, TEXT_ENTRY_FONT_SIZE))
            entryWidget.pack(side=tk.RIGHT, padx="3m")

            self.bindArrows(entryWidget)

            entryWidget.bind("<Return>", self.ok_pressed)
            entryWidget.bind("<Escape>", self.cancel_pressed)

            # for the last entryWidget, if this is a multpasswordbox,
            # show the contents as just asterisks
            if widgetIndex == lastWidgetIndex:
                if mask_last:
                    self.entryWidgets[widgetIndex].configure(show="*")

            # put text into the entryWidget
            if value is None:
                value = ''
            self.entryWidgets[widgetIndex].insert(
                0, '{}'.format(value))

    def create_buttons(self):
        self.buttonsFrame = tk.Frame(master=self.boxRoot)
        self.buttonsFrame.pack(side=tk.BOTTOM)

        self.create_cancel_button()
        self.create_ok_button()

    def create_ok_button(self):

        okButton = tk.Button(self.buttonsFrame, takefocus=1, text="OK")
        self.bindArrows(okButton)
        okButton.pack(expand=1, side=tk.LEFT, padx='3m', pady='3m',
                      ipadx='2m', ipady='1m')

        # for the commandButton, bind activation events to the activation event
        # handler
        commandButton = okButton
        handler = self.ok_pressed
        for selectionEvent in STANDARD_SELECTION_EVENTS:
            commandButton.bind("<%s>" % selectionEvent, handler)

    def create_cancel_button(self):

        cancelButton = tk.Button(self.buttonsFrame, takefocus=1, text="Cancel")
        self.bindArrows(cancelButton)
        cancelButton.pack(expand=1, side=tk.LEFT, padx='3m', pady='3m',
                          ipadx='2m', ipady='1m')

        # for the commandButton, bind activation events to the activation event
        # handler
        commandButton = cancelButton
        handler = self.cancel_pressed
        for selectionEvent in STANDARD_SELECTION_EVENTS:
            commandButton.bind("<%s>" % selectionEvent, handler)

    def bindArrows(self, widget):

        widget.bind("<Down>", self.tabRight)
        widget.bind("<Up>", self.tabLeft)

        widget.bind("<Right>", self.tabRight)
        widget.bind("<Left>", self.tabLeft)

    def tabRight(self, event):
        self.boxRoot.event_generate("<Tab>")

    def tabLeft(self, event):
        self.boxRoot.event_generate("<Shift-Tab>")



class MultiBox(object):

    """ Show multiple data entry fields

    This object does a number of things:

    - chooses a GUI framework (wx, qt)
    - checks the data sent to the GUI
    - performs the logic (button ok should close the window?)
    - defines what methods the user can invoke and
      what properties he can change.
    - calls the ui in defined ways, so other gui
      frameworks can be used without breaking anything to the user
    """

    def __init__(self, msg, title, fields, values, mask_last, callback):
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

        self.ui = GUItk(msg, title, self.fields, self.values,
                        mask_last, self.callback_ui)

    def run(self):
        """ Start the ui """
        self.ui.run()
        self.ui = None
        return self.values

    def stop(self):
        """ Stop the ui """
        self.ui.stop()

    def callback_ui(self, ui, command, values):
        """ This method is executed when ok, cancel, or x is pressed in the ui.
        """
        if command == 'update':  # OK was pressed
            self.values = values
            if self.callback:
                # If a callback was set, call main process
                self.callback(self)
            else:
                self.stop()
        elif command == 'x':
            self.stop()
            self.values = None
        elif command == 'cancel':
            self.stop()
            self.values = None

    # methods to change properties --------------

    @property
    def msg(self):
        """Text in msg Area"""
        return self._msg

    @msg.setter
    def msg(self, msg):
        self.ui.set_msg(msg)

    @msg.deleter
    def msg(self):
        self._msg = ""
        self.ui.set_msg(self._msg)

    # Methods to validate what will be sent to ui ---------

    def check_fields(self, fields, values):
        if len(fields) == 0:
            return None

        fields = list(fields[:])  # convert possible tuples to a list
        values = list(values[:])  # convert possible tuples to a list

        # TODO RL: The following seems incorrect when values>fields.  Replace
        # below with zip?
        if len(values) == len(fields):
            pass
        elif len(values) > len(fields):
            fields = fields[0:len(values)]
        else:
            while len(values) < len(fields):
                values.append("")

        return fields, values



class Mico_GUItk(GUItk):
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
        for selectionEvent in ["Return", "Button-1", "space"]:
            commandButton.bind("<%s>" % selectionEvent, handler)


class Mico_MultiBox(MultiBox):
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
