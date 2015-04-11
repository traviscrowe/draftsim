#! /usr/bin/python

import sys
from datetime import datetime

sys.path.append('/home/cmbiwer/cfbhc/dev/tmp')
sys.path.append('/home/cmbiwer/cfbhc/dev/tmp/nflhc')

from league.models import Clock, Team, Pick

Clock.objects.all().delete()
Team.objects.all().delete()
Pick.objects.all().delete()

for teamabbr in ['NYJ', 'BUF', 'NE', 'MIA', 'GB', 'MIN', 'DET', 'CHI', 'NO', 'CAR', 'TB', 'ATL', 'JAX', 'IND', 'HOU', 'TEN']:
  args = {}
  args['slug'] = teamabbr.lower()
  args['name'] = teamabbr
  team = Team(**args)
  team.save()

fp = open('resources/2016-picks.csv', 'r')
lines = fp.readlines()
fp.close()
for line in lines:
  args = {}
  line = line.rstrip('\n').split(',')

  print line

  args = {}
  args['draft_round'] = line[0]
  args['number'] = int(line[1])
  args['team'] = Team.objects.get(name=line[2])
  player = Pick(**args)
  player.save()

pick = Pick.objects.get(number=1)
time = datetime(year=2015, month=2, day=28, hour=10, minute=5, second=0)
clock = Clock(current_pick=pick, current_start_time=time)
clock.save() 
