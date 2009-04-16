## coding:utf-8 ##
"""
Ed2kServer Test
"""

if __name__ == "__main__":
    print "Main Ed2kServrt Test";

import ED2K

ed = ED2K.Ed2kServer("localhost")

ed.listen()


