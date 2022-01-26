import converter
import tkinter as tk
import tkinter.filedialog as tkfiledialog
import tkinter.messagebox as tkmessagebox
import webbrowser
from lxml import etree



# Main window.
window = tk.Tk()
window.title('XML to Tabular Converter')


class TopMenu:

    def __init__(self):
        top_menu = tk.Menu(window)

        cascade1 = tk.Menu(top_menu, tearoff=0)
        cascade1.add_command(label='Basic Help', command=self.basic_help_clicked)
        cascade1.add_command(label='Visit GitHub (Online Resource)', command=self.visit_github_clicked)
        cascade1.add_command(label='Read License (Online Resource)', command=self.read_license_clicked)
        cascade1.add_command(label='About', command=self.about_clicked)

        top_menu.add_cascade(label='Help', menu=cascade1)
        window.config(menu=top_menu)

    def basic_help_clicked(self):
        with open('help_msg_content.txt', 'r') as help_file:
            help_msg_content = help_file.read()

        tkmessagebox.showinfo('Help', help_msg_content)

    def visit_github_clicked(self):
        webbrowser.open('https://github.com/T-Tomczyk/XML-to-Tabular-Converter')

    def read_license_clicked(self):
        webbrowser.open('https://github.com/T-Tomczyk/XML-to-Tabular-Converter/blob/master/LICENSE')

    def about_clicked(self):
        with open('about_msg_content.txt', 'r') as about_file:
            about_msg_content = about_file.read()

        tkmessagebox.showinfo('About', about_msg_content)


class Option:

    def __init__(self, label_text, radio_dict, row_idx, column_idx):
        '''
        Create an option widget on the main window.

        An option widget consits of two elements:
        1) a label,
        2) a group of radio buttons (of which only 1 button can be selected).

        label_text is what will be written above the radio buttons.

        radio_dict defines the radio buttons in the following way: dict keys
        are button labels and dict values are the values being returned.

        row_idx, column_idx define where widget will be located (widgets
        expand downwards within a single column, so the column_idx will stay
        unchanged while row_idx will be incremented as needed).
        '''

        self.label_text = label_text
        self.radio_dict = radio_dict
        self.row_idx = row_idx
        self.column_idx = column_idx

        label = tk.Label(window, text=self.label_text, width=17)
        label.grid(column=self.column_idx, row=0)

        # Will store user's selection amid all radio buttons in a group.
        self.selection_var = tk.StringVar()

        # For each radio button:
        for radio_text, radio_value in self.radio_dict.items():
            button = tk.Radiobutton(
                window,
                text=radio_text,
                value=radio_value,
                variable=self.selection_var
                )

            button.grid(column=self.column_idx, row=row_idx)

            # First radio button gets selected by default.
            if row_idx == 1:
                button.select()

            # Increment so that next button will be located in subsequent row.
            row_idx += 1

    def get_selection(self):
        '''
        Return the value currently selected in a radio button group.
        '''
        return self.selection_var.get()


class Main_Button:

    def __init__(self):
        button = tk.Button(
            window,
            text='Continue',
            command=self.main_button_clicked
            )
        button.grid(column=2, row=4)


    def main_button_clicked(self):
        '''
        Event which occurs when user clicks the Convert button.
        '''

        # Ask user to select files that they want converted.
        filepaths = tkfiledialog.askopenfilenames(title='Select XML files')

        try:
            df = converter.parse_xmls_and_save_to_df(
                filepaths,
                include_attributes_option.get_selection(),
                namespaces_style_option.get_selection()
                )

            converter.generate_output_file(df, output_format_option.get_selection())

        except etree.XMLSyntaxError as e:
            tkmessagebox.showerror(
                'Error',
                f'XML file(s) invalid. Unable to convert.\n\nError details:\n {e}'
                )


TopMenu()

output_format_option = Option(
    'Output format:',
    {'.csv':'csv', '.xlsx':'xlsx'},
    1,
    0
    )

namespaces_style_option = Option(
    'Namespaces style:',
    {'Hidden':'hidden', 'Prefixes':'prefixes', 'Full links':'full'},
    1,
    1
    )

include_attributes_option = Option(
    'Include attributes?',
    {'Yes':'yes', 'No':'no'},
    1,
    2
    )

Main_Button()

window.mainloop()
