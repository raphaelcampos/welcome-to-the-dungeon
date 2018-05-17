import itertools
import pandas as pd
import numpy as np


class Monster(object):

  def __init__(self, id, name, demage):
    self.id = id
    self.name = name
    self.demage = demage

class Hero(object):

  def __init__(self, id, name, hp, items):
    self.id = id
    self.name = name
    self.hp = self.curr_hp = hp
    self.armors = []
    self.potion = None
    self.dis_items = []
    self.reuse_items = []

    for item in items:
      if isinstance(item, Armor):
         self.armors.append(item)
      elif isinstance(item, Potion):
         self.potion = item
      elif isinstance(item, ReusableItem):
        self.reuse_items.append(item)
      else:
         self.dis_items.append(item)

  def get_ready(self):
    for armor in self.armors:
      armor.activate(self)

  def is_dead(self):
    return self.curr_hp <= 0

  def reset_hp(self):
    self.curr_hp = self.hp

  def can_kill(self, monster):
    can = False
    for item in self.reuse_items:
      can |= item.activate(monster)
    return can



class Dungeon(object):

  def enter(self, hero, monsters):
    hero.get_ready()
    monsters = [monster for monster in monsters if not hero.can_kill(monster)]

    monsters.sort(key=lambda x: -x.demage)
    if len(monsters) > 0 :
      if len(hero.dis_items) > 0:
        del monsters[0]
      for monster in monsters:
        hero.curr_hp -= monster.demage
        if hero.is_dead() and not hero.potion is None:
          hero.potion.activate(hero)
          hero.potion = None

    return not hero.is_dead()


class Potion(object):

   def activate(self, hero):
      if hero.is_dead():
        hero.reset_hp()
        return True

      return False

class Armor():

   def __init__(self, extra_hp):
      self.extra_hp = extra_hp

   def activate(self, hero):
     hero.curr_hp += self.extra_hp

class DisposableItem(object):
  pass

class Machado(DisposableItem):

  def activate(self, monster):
    return True

class ReusableItem(object):
  pass

class Torche(ReusableItem):

  def activate(self, monster):
    return monster.demage <= 3

class MarteloGollem(ReusableItem):

  def activate(self, monster):
    return monster.demage == 5


monsters_demages = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7]
monsters = np.array([Monster('', '', demage) for demage in monsters_demages])
print(monsters)

items = [Potion(), Armor(4), Armor(3), Torche(), MarteloGollem(), Machado()]
Barbare = Hero('', 'Barbare', 4, items)

print(items)

d = Dungeon()
result = d.enter(Barbare, monsters)
print(result)
#[]


possibilities = itertools.product('01', repeat=len(items) + len(monsters))
arr = []
for i in possibilities:
   i = np.array(list(map(int, i)), dtype=bool)
   if i[:len(monsters)].sum() == 0:
      continue
   result = Dungeon().enter(Hero('', 'Barbare', 4, [item for item, ii in zip(items, list(i[len(monsters):])) if ii]), monsters[i[:len(monsters)]])
   arr.append(list(i) + [result])


df = pd.DataFrame(arr, dtype=int,
             columns=list(monsters_demages) + ['potion', 'armor1', 'armor2', 'torche', 'martello', 'machado', 'survived'])

df.to_csv("barbare.csv", index=False)
