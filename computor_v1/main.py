import sys
from solver import *

error_syntax = 'Error: Usage Python3 \'[aX2 + bX + c = 0]\''

def run(equation_str):
    solve = Solver(0.0, 0)
    expression = solve.prepare_expression(equation_str)
    if (len(expression[0]) and len(expression[1])):
        expression_minim_tab = solve.minimize_expression(expression) ## list 
        min_equation = solve.convert_to_str(expression_minim_tab) 
        power_max = solve.get_max_power_equation(expression_minim_tab)
        print("Reduced form: {0}".format(min_equation))
        if power_max == 0:
            print("Polynomial degree: {0}".format(power_max + 1))
        else:
            print("Polynomial degree: {0}".format(power_max))
        if (power_max > 2):
            print("The polynomial degree is strictly greater than 2, I can't solve.")
            exit(0)
        elif power_max == 2:
            solve.second_degree_solver(expression_minim_tab)
        elif power_max == 1:
            solve.first_degree_solver(expression_minim_tab)
        elif power_max == 0:
            if expression_minim_tab:
                print("There's no solution!")
            else:
                print("All the X member of R are the solution") 
                
    else:
        print(error_syntax)

def main():
    if len(sys.argv) == 2 :
        equation_str = sys.argv[1]
        size = len(equation_str.split('='))
        if size == 2:
            run(equation_str)
        else:
            print(error_syntax)
    else:
        print(error_syntax)

if __name__ == "__main__":
    main()