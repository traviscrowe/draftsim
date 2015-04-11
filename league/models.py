from datetime import datetime

from django.db import models

_POSITION_CHOICES = (
  ('QB','Quarterback'),
  ('RB','Runningback'),
  ('FB','Fullback'),
  ('WR','Wide Receiver'),
  ('TE','Tight End'),
  ('OT','Offensive Tackle'),
  ('OG','Offensive Guard'),
  ('C','Center'),
  ('DE','Defensive End'),
  ('DT','Defensive Tackle'),
  ('ILB','Inside Linebacker'),
  ('OLB','Outside Linebacler'),
  ('CB','Cornerback'),
  ('FS','Free Safety'),
  ('SS','Strong Safety'),
  ('K','Kicker'),
  ('P','Punter'),
  ('ATH','Athlete'),
)

_ATTRIBUTE_CHOICES = (
  ('scrambling','Scrambling'),
  ('pocketpasser','Pocket Passer'),
  ('speed','Speed'),
  ('power','Power'),
  ('runblocking','Run Blocking'),
  ('passblocking','Pass Blocking'),
  ('passstop','Pass Stop'),
  ('runstop','Run Stop'),
  ('passman','Pass Man-to-Man'),
  ('runman','Run Man-to-Man'),
  ('passzone','Pass Zone'),
  ('runzone','Run Zone'),
  ('man','Man Coverage'),
  ('zone','Zone Coverage'),
  ('accuracy','Accuracy'),
)

class Clock(models.Model):
  '''
  Clock model that controls the draft pick times.

  App assumes there is only one Clock instance.
  '''

  # draft information
  active = models.BooleanField(default=False)

  # pick information
  current_pick = models.ForeignKey('Pick')
  seconds_left = models.IntegerField(max_length=100)

  def render(self):
    '''
    Displays upcoming pick and time left on the clock.
    '''

    # get clock
    clock = Clock.objects.get(pk=1)
    seconds_left = clock.seconds_left

    # get on deck picks
    # FIXME: this whole section can be done more elegantly
    current_pick = clock.current_pick
    deck_1_pick = Pick.objects.filter(number=clock.current_pick.number+1)
    deck_2_pick = Pick.objects.filter(number=clock.current_pick.number+2)
    deck_3_pick = Pick.objects.filter(number=clock.current_pick.number+3)
    deck_4_pick = Pick.objects.filter(number=clock.current_pick.number+4)
    deck_5_pick = Pick.objects.filter(number=clock.current_pick.number+5)

    # create string
    args = {'current_pick' : current_pick,
            'seconds_left' : seconds_left}
    string1 = """(#{current_pick.number}) {current_pick.team.name} is on the clock! There are {seconds_left} seconds left on the clock.""".format(**args)

    string2 = "On deck are:"
    string_list = []
    for query in [deck_1_pick, deck_2_pick, deck_3_pick, deck_4_pick, deck_5_pick]:

        if len(query):
            pick = query[0]
            args = {"pick_number" : pick.number,
                    "team_name" : pick.team.name}
            string_list.append("""(#{pick_number}) {team_name}""".format(**args))
    string2 += ' ' + ', '.join(string_list)

    # return
    return string1 + ' ' + string2

class Team(models.Model):
  '''
  Teams in the league.
  '''

  # information
  slug = models.SlugField(unique=True)
  name = models.CharField(max_length=30)

class Player(models.Model):
  '''
  Player model that relates teams to picks.
  '''

  # information
  slug = models.SlugField(unique=True)
  name = ''
  # player information
  forename = models.CharField(max_length=100)
  surname = models.CharField(max_length=100)
  position = models.CharField(max_length=3, choices=_POSITION_CHOICES)
  height = models.IntegerField(max_length=4)
  weight = models.IntegerField(max_length=3)
  college = models.CharField(max_length=30)
  attribute = models.CharField(max_length=50, choices=_ATTRIBUTE_CHOICES)
  skill = models.IntegerField()

  # combine information
  dash_40 = models.FloatField(blank=True, null=True) 
  vertical_leap = models.FloatField(blank=True, null=True)
  board_jump = models.FloatField(blank=True, null=True)
  bench_press = models.FloatField(blank=True, null=True)
  shuttle = models.FloatField(blank=True, null=True)
  kicking = models.CharField(max_length=2, blank=True, null=True)
  wonderlic = models.IntegerField(max_length=2, blank=True, null=True)

  def __unicode__(self):
      return ' '.join(map(str, [self.position, self.forename, self.surname,
                                self.height, self.weight, 'R', self.college,
                                '['+self.attribute+']', self.skill]))

class Pick(models.Model):
  '''
  Handles owner and player of draft picks.
  '''

  # pick information
  draft_round = models.IntegerField(max_length=2)
  number = models.IntegerField(max_length=3)
  team = models.ForeignKey('Team', blank=True, null=True)
  player = models.ForeignKey('Player', blank=True, null=True)
  compensation_pick = models.BooleanField(default=False)

