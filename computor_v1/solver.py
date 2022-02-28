from main import error_syntax

error_format = 'Error format: The expression is not well formatted in element [{0}]'

class Solver:
    def __init__(self, weight: float, power:int):
        self.weight = float(weight)
        self.power = int(power)
        self.dic = dict()
        self.tab = []

    def get_max_power_equation(self, tab):
        l = len(tab)
        if l == 0:
            return (0)
        return (tab[l - 1].get_power())
    def get_weight(self):
        return self.weight
    def get_power(self):
        return self.power

    def prepare_expression(self, str_val):
        str_val = str_val.replace(" ", "").replace("\t", "").replace("\n", "").replace("+", " +").replace("-",
                " -").replace("=", " = ")
        expres = str_val.split("=")
        # print('******'+str_val+'******')
        if (len(expres) != 2):
            print(error_syntax)
            exit(1)
        expres[0] = expres[0].strip()
        expres[1] = expres[1].strip()
        return expres

    def get_elemt_expression(self, e):
        index = 0
        len_elem = len(e)
        if e[0] == "-" or e[0] == '+': ## sign
            index += 1
        while index < len_elem and ((e[index] == '.') or (e[index].isdigit())):
            index += 1 ## skiping '.' & [0-9] characters

        if index == len_elem - 1 and e[index] == "X": ## last character == 'X'? 
            elem = e.replace("+", "").replace("-", "")## remove +/- character
            if len(elem) == 1 and elem == "X":
                if e[0] == "-":
                    e_weight = -1
                else:
                    e_weight = 1
                elem = Solver(float(e_weight), 1)
                return elem
        
        if index == len_elem and e[index - 1] == ".":
            print("Error format [{0}]".format(e))
            return None
        try:
            if (len(e) == 1):
                e_weight = float(e[:index])
            else:
                if (index == len(e)):
                    e_weight = float(e[:index])
                elif e[index] == 'X':
                    if (e[0] == '+' or e[0] == '-') and e[1] == 'X':
                        e_weight = 1
                    elif e[0] == 'X':
                        e_weight = 1
                    else:
                        e_weight = float(e[:index])
                else:
                    e_weight = float(e[:index])
        except ValueError:
            print("Error format [{0}]".format(e))
            exit(1)
        power = 0
        if index < len_elem:
            if e[index] == "*" or e[index] == "X":
                if e[index] == "*":
                    index += 1
                if index < len_elem and e[index] == "X":
                    index += 1
                    if index < len_elem and (e[index] == "^"):
                        index += 1
                        if index == len_elem:
                            print("Error format : the power of the unknown element is not indicated : [{0}]".format(e))
                            return None
                        else:
                            power = e[index:]
                            if not power.isdigit():
                                print("Error format : the power of the unknown element is not well formatted: [{0}] int expected".format(e))
                                return None
                    elif index == len_elem:
                        power = 1
                    else:
                        print(error_format.format(e))
                        return None
                else:
                    print(error_format.format(e))
                    return None
            else:
                print(error_format.format(e))
                return None
        return Solver(weight=e_weight, power=power)


    def sort_equation_asc(self, tab):
        i = 0
        l = len(tab)
        while i + 1 < l:
            if int(tab[i].get_power()) > int(tab[i + 1].get_power()):
                temp = tab[i]
                tab[i] = tab[i + 1]
                tab[i + 1] = temp
                i = 0
            else:
                i += 1
        return tab


    def leftPart(self, expression, dict):
        elem = expression.split(" ")
        for e in elem:
            el = self.get_elemt_expression(e)
            if el is None:
                exit(1)
            else:
                if el.get_power() in dict.keys():
                    dict[el.get_power()] += el.get_weight()
                else:
                    dict[el.get_power()] = el.get_weight()

    def rightPart(self, expression, dict):
        elem = expression.split(" ")
        for e in elem:
            el = self.get_elemt_expression(e)
            if el is None:
                exit(1)
            else:
                if el.get_power() in dict.keys():
                    dict[el.get_power()] -= el.get_weight()
                else:
                    dict[el.get_power()] = -el.get_weight()

    def convert_to_str(self, tab):
        ret = ""
        l = len(tab)
        i = 0
        for e in tab:
            if not( i == l  or i == 0):
                if (e.get_weight() > 0):
                    ret += " +"
                else:
                    ret += " "
            if e.get_weight() != 1:
                ret += str(e.get_weight())
            ret += "X^"+str(e.get_power())
            i += 1
        if (ret == ""):
            ret += "0" 
        return ret+" = 0"

    def solve_neg_delta(self, a, b, delta):
        r = delta ** 0.5
        if (r * r) == delta :
            print("x1 = (-{0} - i * {1})/ {2}  ".format(b, r, 2 * a))
            print("x2 = (-{0} + i * {1})/ {2}  ".format(b, r, 2 * a))
        else:
            print("x1 = (-{0} - i * √ {1})/ {2}  ".format(b, delta, 2 * a))
            print("x2 = (-{0} + i * √ {1})/ {2}  ".format(b, delta, 2 * a))

    def minimize_expression(self, expression):
        self.leftPart(expression[0], self.dic)
        self.rightPart(expression[1], self.dic)
        for key, val in self.dic.items():
            k = int(key)
            v = float(val)
            if v != 0:
                self.tab.append(Solver(v, k))
        return self.sort_equation_asc(self.tab)

    def second_degree_solver(self, tab):
        b = 0
        c = 0
        for e in tab:
            if (e.get_power() == 2):
                a = e.get_weight()
            elif (e.get_power() == 1):
                b = e.get_weight()
            elif (e.get_power() == 0):
                c = e.get_weight()
        delta = (b * b) - (4 * a * c)
        print("[a == {0}]  [b == {1}]  [c == {2}]  [delta == {3}]".format(a, b, c, delta))
        if (delta > 0):
            print("Discriminant is strictly positive, the two solutions are:")
            sol1 = (-b - (delta ** 0.5)) / (2 *a)
            sol2 = (-b + (delta ** 0.5)) / (2 *a)
            print("x1 = {0}".format(sol1))
            print("x2 = {0}".format(sol2))
        elif delta == 0:
            print("Discriminant is null, the solution is:")
            sol1 = (-b - (delta ** 0.5)) / (2 *a)
            print("x = {0}".format(sol1))
        else:
            self.solve_neg_delta(a, b, delta=delta)
            # print("!Ther's no solution in ℝ")
            exit(0)
                                                                                        
    def first_degree_solver(self, tab):
        l = len(tab)
        if (l == 1):
            print("The solution is : 0")
        else:
            b = tab[0].get_weight()
            a = tab[1].get_weight()
            print("The solution is : {0}".format(-b / a))
