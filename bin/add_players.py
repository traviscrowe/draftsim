#! /usr/bin/python

import sys

sys.path.append('/home/cmbiwer/cfbhc/dev/tmp')
sys.path.append('/home/cmbiwer/cfbhc/dev/tmp/nflhc')

from league.models import Player

Player.objects.all().delete()

fp = open('resources/2016-players.txt', 'r')
lines = fp.readlines()
fp.close()
for line in lines:
  args = {}
  line = line.rstrip('\n')

  # get position
  position = line.split()[0]

  # get height
  height = 0
  i = 0
  tmp = line.split('[')[0]
  tmp = tmp.split()
  for t in tmp:
    if '-' in t and t.split('-')[0].isdigit() and t.split('-')[1].isdigit():
      height = 12 * int(t.split('-')[0]) + int(t.split('-')[1])
      i = tmp.index(t)
      print 't', t
      break

  # get surname
  surname = line.split()[i-1]

  # get forename
  forename = ' '.join(line.split()[1:i-1])

  # get weight
  i += 1
  weight = line.split()[i]

  # get college
  i += 2
  j = 0
  tmp = line.split()
  for t in tmp:
    if '[' in t:
      j = tmp.index(t)
      break
  college = ' '.join(line.split()[i:j])

  # get attribute
  idx1 = line.index('[') + 1
  idx2 = line.index(']')
  attribute = line[idx1:idx2]

  # get skill
  skill = line.split()[-1]

  print line
  print position
  print forename
  print surname
  print height
  print weight
  print college
  print attribute
  print skill

  args = {}
  args['slug'] = position.lower() + '-' + forename.replace(' ', '-').lower() + '-' + surname.replace(' ', '-').lower() + '-' + skill
  args['position'] = position
  args['forename'] = forename
  args['surname'] = surname
  args['height'] = height
  args['weight'] = weight
  args['college'] = college
  args['attribute'] = attribute
  args['skill'] = skill
  player = Player(**args)
  player.save()
 
