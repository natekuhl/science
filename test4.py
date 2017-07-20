


a = ['asd__asdfasdf__asdfasd','asdfa__asdfas__asdfasd','asdfasd__asdfasd__asdfasd']

b = []


for name in a:
    b = b + name.split("__")

print(b)



