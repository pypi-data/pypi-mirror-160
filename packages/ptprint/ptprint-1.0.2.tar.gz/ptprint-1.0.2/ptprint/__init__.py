from time import sleep

r = "\033[0m"
b = "\033[1m"
u = "\033[4m"

class C:

    def hexprint(r, g, b, text):
        return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)

    def p(text):
        print(text)

    ###################################################################################################

    def pp(rgb, text):
        r, g, b = rgb.split(",")
        print(C.hexprint(int(r), int(g), int(b), text))

    ###################################################################################################

    def load(text, time, pattern):
        for i in range(int(time)):
            print(pattern[i % len(pattern)] + " " + text, end="\r")
            sleep(1)

    # spinners = ["|", "/", "+", "\\"]
    # load("Loading", 7, spinners)

    ###################################################################################################

    def table(wall, floor, data):

        col_widths = [max(len(str(x)) for x in col) for col in zip(*data)]
        try:
            for row in data:
                C.p(f"{r + floor * (sum(col_widths) + 4 * len(col_widths) - 5)}")
                C.p(f"{r + wall}{r} " + f" {wall}{r} ".join(str(x).center(w) for (x, w) in zip(row, col_widths)) + f" {wall}{r}")
            C.p(f"{r + floor * (sum(col_widths) + 4 * len(col_widths) - 5)}")
        except IndexError:
            print("Error: Data is out of index!")

# title = ["Data Hash", "Username", "Password",  "Email", "Phone", "Adress"]
# data  = ["0x00", "Birdlinux", "testuser123", "bd@crime.su", "N/A", "N/A"]
# data1 = ["0x01", "Nickolaospaparas", "testpassword158151", "testemail@testtsts.su", "N/A", "N/A"]
# C.table("|", "-", [title, data, data1])

    ###################################################################################################