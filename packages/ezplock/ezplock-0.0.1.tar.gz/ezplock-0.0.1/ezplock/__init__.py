import py_compile

import time as t

import os

def alock():

    def tef(string, delay):

        for char in string:
            print(char, end='')

            t.sleep(delay)

    def main():

        print(' ')

        tef("Please put the script path", 0.223)

        og = input(": ")

        try:

            script = og

            py_compile.compile(script)

            t.sleep(1)

            print(' ')

            tef("The code was compiled successfully", 0.22)

            print(' ')

            tef("Would you like to compile another code?", 0.22)

            kk = input(" Y/N: ")

            if kk == "y" or kk == "Y" or kk == "yes" or kk == "YES":

                t.sleep(1)

                os.system('CLS')

                main()

            elif kk == "N" or kk == "n" or kk == "no" or kk == "NO":

                t.sleep(1)

                exit

        except:

            try:

                def error():
                    print(' ')
                    IKO = "Inncorect script path or a error ocured"

                    def iklo():
                        for i in IKO:
                            print(i, end='')

                            t.sleep(0.223)

                    iklo()

                    print(' ')

                    t.sleep(2)

                    os.system('CLS')

                    main()

                error()

            except:

                print("Inncorect script path or a error ocured")

                main()

    main()