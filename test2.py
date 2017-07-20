
class Fruit(object):
    """A class that makes various tasty fruits."""
    def __init__(self, label, color, flavor, poisonous):
        self.label = label
        self.color = color
        self.flavor = flavor
        self.poisonous = poisonous

    def description(self):
        print "I'm a %s %s and I taste %s." % (self.color, self.label, self.flavor)

    def is_edible(self):
        if not self.poisonous:
            print "Yep! I'm edible."
        else:
            print "Don't eat me! I am super poisonous."

lemon = Fruit("lemon", "yellow", "sour", False)
apple = Fruit("apple", "red", "sweet", False)
plum = Fruit("plum", "purple", "sweet", False)


lemon.description()
lemon.is_edible()

if apple.label == "apple":
    print "it works!"
else:
    print "it doesnt work"
