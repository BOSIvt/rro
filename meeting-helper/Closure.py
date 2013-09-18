#!/bin/env python

"""Closure.py

 Implements a Closure class, similar to closures in lisp.

To: python-list@cwi.nl
From: nisse@lysator.liu.se (Niels Moller)
X-newsgroups: comp.lang.python
Subject: Re: Closures (was Re: simple recursion problem)
Date: 12 Sep 1996 20:42:09 +0200
X-organization: Lysator Computer Society, Linkoping University, Sweden

Donald Beaudry <donb@zippy.boston.sgi.com> writes:

> > What I'd like to know if there's any reason that my attempt at a
> > Closure python class can't be improved. That is, if it's possible to
> > avoid copying, and instead store a reference to another function's
> > dictionar{y|ies} of variables, and then define getattr/setattr that
> > accesses that dictionary. That would give you something that's pretty
> > close to closures.
> 
> It can be done... if I had a few extra hours, I'd piece it together
> just for fun.  Right now, I'm having too much fun with work ;)
> 
> Basically, it involves writing a callable built-in object that by
> passes the "normal" initialization stuff prior to invoking the code
> object.  That is, it must arrange for the function to be called with
> the local environment passed to its constructor.  The constructor
> could also allow for a global ennvironment to be passed as well, but
> that might not be a good idea, since the function was written with a
> particular global environment in mind.  All of this is possible and I
> alluded to that fact in that other post I was refering to.

Well, while waiting for your C module, I wrote up one in python. I
know this is the second Closure class I post tonight, but this one is
actually working, and tested. To extend or change the behavior, you
need only use different Environment objects; the Closure class takes
care of all needed magic and I think it's general enough for almost
anything.

I wonder if anyone can find any use for it...

Regards,
	Niels
"""


class Environment:
   def __init__(self, *dicts):
      # If you pass more than one dictionary, they will be searched
      # in order.
      self.dicts = dicts

   def get(self, name):
      for dict in self.dicts:
	 if dict.has_key(name):
	    return dict[name]
      raise AttributeError, name

   def set(self, name, value):
      for dict in self.dicts:
	 if dict.has_key(name):
	    dict[name] = value
	    return
      # Creating new variables is not allowed.
      # One could use an extra dictionary for storing them, though.
      raise AttributeError, name

      
class Closure:
   def __init__(self, f, env):
      self.__dict__['function'] = f
      self.__dict__['environment'] = env

   def __call__(self, *args, **kw):
      return apply(self.function, (self, ) + args, kw)
      
   def __getattr__(self, name):
      return self.environment.get(name)

   def __setattr__(self, name, value):
      self.environment.set(name, value)


# Test functions
def make_adder(n):
   # The classic example
   adder = Closure(lambda state, x: state.n + x,
		   Environment(vars()))

   # The state is not read-only
   def setter_fn(state, new): state.n = new
   setter = Closure(setter_fn,
		    Environment(vars()))

   return adder, setter

def test():
   foo, bar = make_adder(1)
   print map(foo, (3, 5, 7))
   bar(-1)
   print map(foo, (3, 5, 7))
