from datetime import datetime

from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from league.models import _POSITION_CHOICES
from league.models import Clock, Player, Pick

def HomePage(request):

  # get clock
  clock = Clock.objects.all()[0]

  # render
  context = {'clock' : clock}
  return render_to_response('home.html', context,
                            context_instance=RequestContext(request))

def PositionPage(request, position):

  # get clock
  clock = Clock.objects.all()[0]

  position         = position.upper()
  position_verbose = [x[1] for x in _POSITION_CHOICES if x[0] == position][0]

  players = Player.objects.filter(position=position)

  # render
  context = {'clock'            : clock,
             'position'         : position,
             'position_verbose' : position_verbose,
             'players'          : players}
  return render_to_response('position.html', context,
                            context_instance=RequestContext(request))

def DraftPicksPage(request):

  # get clock
  clock = Clock.objects.all()[0]

  picks = Pick.objects.all()

  # render
  context = {'clock' : clock,
             'picks' : picks}
  return render_to_response('draft_picks.html', context,
                            context_instance=RequestContext(request))

