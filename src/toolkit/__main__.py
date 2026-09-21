

from toolkit.calculator import Calc
def main():
    a = input()
    print(a)
    if a == 'calc':
        my_calc = Calc()
        my_calc.getinput()
        my_calc.parser()
        my_calc.counter()
        my_calc.printer()

if __name__ == '__main__':
    main()