class MyClass(object):
     i = 123
     def __init__(self):
         self.i = 345

a = MyClass()
print a.i
# 345
print MyClass.i
# lk123


class foo:
    def bar(self):
            print "hi"

f = foo()
f.bar()