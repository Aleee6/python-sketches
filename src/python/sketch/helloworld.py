class HelloWorld:
    _hello = "Hello" #protected
    __world = "World" #private

    def sayhello(self):
        print("%s %s" % (self._hello, self.__world))


class HelloUniverse(HelloWorld):
    def sayhello(self):
        self._hello = "Hello Universe"
        super(HelloUniverse, self).sayhello()


