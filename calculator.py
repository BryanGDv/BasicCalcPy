import PySimpleGUI as gui


def add_top_number(num: str, value: str):
    if num is None:
        return value

    return num + value


def operate(operation: str):

    if len(operation) == 0:
        return "ERR_EMPTY"
    try:
        return eval(operation)
    except Exception as ex:
        if type(ex) == ZeroDivisionError:
            return "ERR_ZDE"


def calculator_layout():
    BUTTON_SIZE = (4, 2)

    menu_layout = [["File", ["Close"]]]

    calc_layout = [
        [gui.Button("1", key="-NUM1-", size=BUTTON_SIZE), gui.Button("2", key="-NUM2-", size=BUTTON_SIZE),
         gui.Button("3", key="-NUM3-", size=BUTTON_SIZE), gui.Button("+", key="-OPERATOR_SUM-", size=BUTTON_SIZE)],

        [gui.Button("4", key="-NUM4-", size=BUTTON_SIZE), gui.Button("5", key="-NUM5-", size=BUTTON_SIZE),
         gui.Button("6", key="-NUM6-", size=BUTTON_SIZE), gui.Button("-", key="-OPERATOR_SUB-", size=BUTTON_SIZE)],

        [gui.Button("7", key="-NUM7-", size=BUTTON_SIZE), gui.Button("8", key="-NUM8-", size=BUTTON_SIZE),
         gui.Button("9", key="-NUM9-", size=BUTTON_SIZE), gui.Button("*", key="-OPERATOR_MUL-", size=BUTTON_SIZE)],

        [gui.OK("OK", key="-OK-", size=BUTTON_SIZE), gui.Button("0", key="-NUM0-", size=BUTTON_SIZE),
         gui.Button("DEL", key="-DEL-", size=BUTTON_SIZE), gui.Button("/", key="-OPERATOR_DIV-", size=BUTTON_SIZE)],

        [gui.Text("Input:", font=("Helvetica", 11))],
        [gui.Input("", readonly=True, size=(22, 1), key="-RESULT-")],
        [gui.Text("Log:", font=("Helvetica", 11))],
        [gui.Multiline("", size=(24, 2), font=("Helvetica", 11), disabled=True, key="-LOG-")]
    ]

    app_layout = [[gui.Menu(menu_layout, key="-MENU-", font=("Helvetica", 9))], [gui.Col(calc_layout)]]

    return app_layout


def init_project():
    gui.theme("GrayGrayGray")
    gui.set_options(font=("Helvetica", 13))

    window = gui.Window(title="Calculator", layout=calculator_layout())

    error_message = {"ERR_ZDE": "Error: Estás dividendo entre cero.",
                     "ERR_EMPTY": "Error: No has puesto ninguna operación."}
    operations_log = list()

    operation_dict = {"SUM": "+", "SUB": "-", "MUL": "*", "DIV": "/"}
    operation_line = ""

    first_num = old_second_num = second_num = None
    old_operator = operator = ''

    result = 0

    while True:
        event, value = window.read()

        if event == gui.WIN_CLOSED or event == "Close":
            break

        if event == "-DEL-":
            first_num = old_second_num = second_num = None
            old_operator = operator = ''
            result = 0

            window["-RESULT-"].Update("")
            continue

        if event == "-OK-":

            if old_operator != '':
                operation_line = str(result) + " " + old_operator + " " + old_second_num

            result = operate(operation_line)

            if isinstance(result, str) and result.startswith("ERR"):
                operations_log.insert(0, error_message[result])
                window["-LOG-"].Update("\n".join(operations_log))

                old_operator = ''
                old_second_num = second_num = None
                continue

            if isinstance(result, float):

                if result * 10 % 10 == 0:
                    result = int(result)
                else:
                    result = result.__round__(3)

            first_num = result

            if old_operator == '':

                old_second_num = second_num
                old_operator = operator

                operator = ''
                second_num = None

            operations_log.insert(0, operation_line + " = " + str(result))
            window["-LOG-"].Update("\n".join(operations_log))
            window["-RESULT-"].Update(result)

        elif event.startswith("-NUM"):

            if result != 0:
                first_num = old_second_num = second_num = None
                old_operator = operator = ''
                result = 0

            num = event[4]

            if len(operator) == 0:
                first_num = add_top_number(first_num, num)
                operation_line = "{0}".format(first_num)
            else:
                second_num = add_top_number(second_num, num)
                operation_line = "{0} {1} {2}".format(first_num, operator, second_num)

            window["-RESULT-"].Update(operation_line)
            continue

        elif event.startswith("-OPERATOR"):

            if result != 0:
                result = 0

            if first_num is None:
                operations_log.insert(0, error_message["ERR_EMPTY"])
                window["-LOG-"].Update("\n".join(operations_log))
                continue

            if second_num is not None:
                second_num = None

            if old_operator != '':
                old_operator = ''
                old_second_num = None

            operator = operation_dict[event[10:13]]


            operation_line = "{0} {1}".format(first_num, operator)
            window["-RESULT-"].Update(operation_line)
            continue
    window.close()


if __name__ == "__main__":
    init_project()
