import random

def rede():
  redes_list = [
    "Не зная броду, не суйся в воду",
    "Любишь кататься, люби и саночки носить",
    "Дважды в год лето не бывает"
  ]

  return random.choice(redes_list)

def print_rede():
  print(rede())

if __name__ == '__main__':
  print_rede()
