#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ==================================
# testcase and user guide with Nanorm
# ==================================

from nanorm import *


class Area(Model):
    name = CharField()


class User(Model):
    name = CharField(128)           # CharField default="" max_length=255
    age = IntegerField()            # IntegerField default=0
    score = FloatField(default=6.8) # FloatField default=0.0
    sex = BooleanField()            # BooleanField default=True
    area = ForeignKey(Area)         # ForeignKey can not be null

    def __str__(self):
        return "%s_%s_%s_%s_%s" % (self.__class__.__name__, self.id, self.name, self.age, self.sex)



# ==============================================

set_db_name("nanorm.db")    # set database name to use

Area.query().delete()       # clear the data in tables
User.query().delete()       # or you can manual delete database

# ==============================================


mainland = Area(name="mainland").save() # quick create and save object
taiwan = Area(name="taiwan").save()     # and the save() function return the target object

rs = Area.query().all() # use .query().all() to get a list of all data of this model class
assert len(rs) == 2

# ==============================================

s1 = User()             # create a model object
s1.name = "Joe"         # set the attributes
s1.age = 45 
s1.sex = True   
s1.area = taiwan    
s1.save()               # and save it

q = User.query()        # use query() to convert a model class to a query object
q = q.filter(age=45)    # use filter() to filter the data and update the query
joe = q.first()         # use fisrt() to execute a query of get the first result

assert joe.name == "Joe"


# ==============================================


s2 = User(name="Motive")
s2.age = 40
s2.sex = True
s2.area = mainland
s2.save()

s2.area = taiwan            # modify the attribute
s2.save()                   # save the modify

motive = User.get(id=2)     # use .get(**kwargs) as same as .query().filter(**kwargs).first()

assert motive.area.name == "taiwan"


# ==============================================


s3 = User(name="Sandy", area=mainland)
s3.save()

sandy = User.query().filter(name="Sandy").last()   # use last() to execute a query of get the last result
sandy.age = 32
sandy.sex = False
sandy.save()

rs = User.gets(sex=True)    # use .gets(**kwargs) as same as .query().filter(**kwargs).all()

assert len(rs) == 2


# ==============================================

s = User.query().order("age").all()     # use order() function in query to sort

assert s[0].name == "Sandy"

# ==============================================

s = User.query().filter(sex=True).order("-name").all()  # add "-" to the head of field name to reverse sort

assert s[1].name == "Joe"

# ==============================================

s = User.get(age="32", operator="<=")   # set operator symbol to filter data compare target field with the value

assert s.name == "Sandy"

# ==============================================

s = User.get(name="J%", operator="like")    # also can use "like" operator to filter strings

assert s.name == "Joe"

# ==============================================

s = User.get(area=mainland)         # filter ForeignKey

assert s.name == "Sandy"

# ==============================================

s1 = User.get(name="Sandy")         # if two object has the same model class and the same id
s2 = User.get(name="Sandy")         # then they are equal

assert  s1 == s2

# ==============================================

s1 = User.get(name="Joe")           # has the same model class and no same id
s2 = User.get(name="Sandy")         # aren't equal

assert  s1 != s2

# ==============================================

s1 = User.get(id=1)                 # has the same id and no same model class
s2 = Area.get(id=1)                 # aren't equal

assert  s1 != s2

# ==============================================

# the new function add in version 1.4

auto_commit_close()             # close auto commit, then data is not automatically submitted when the update 

Area(name="uk").save()          # save the two area data, but not commit
Area(name="usa").save()

auto_commit_open()              # open auto commit, and commit at the same time

assert len(Area.gets()) == 4

# ==============================================






# ==============================================

print(User.gets())
print("Success!")
