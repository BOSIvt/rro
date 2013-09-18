# This Python module was automatically compiled from
# Rule File "ruleFiles/rro_default.txt"
# on Tue May 10 01:31:23 2005
# by the program compileRuleFile.py V0.01




from Transitions import *
from Action import *
from Motion import *
from Initiative import *

from State import *
import Default_initial_state 

# $Id: default_ruleset.py,v 1.2 2005/06/01 18:56:21 bshanks Exp $
#
# COPYRIGHT 2004, 2005 BAYLE SHANKS
# COPYRIGHT 2005 DANA DAHLSTROM
#  Available under the GPL
#
#  Partially based on Henry Prakken's excellent formalization of a large part of Robert's Rules

# It should be noted that no effort is being made to make these rules strictly conform to the any version of Robert's Rules of Order. These rules are an almagation of Henry Prakken's formalization, of the 1915 version of Robert's Rules, and of suggestions by various people.
# Note that there is also an updated version of Robert's Rules which you can buy as a book. I don't have the book, and so these rules DO NOT reflect the "current" version of RRO.
# At some future time perhaps a version strictly following the 1915 version of RRO will be released.

##
## NOTE:
##  I made one predicate, subsidiaries allowed, which covers amendments
##  unless AMENDABLE is specified. Should probably be clarified.
##
##
##    mar 21: changed implementation of this a little. now, if "amendable"
##      is specified, it has the last word on amendments.
##      if it's not specified, then "subsidiaries allowed" covers them.
##



class rro_motion(motion):
	name = 'RRO Motion'

	internal_name = 'rro_motion'

	def type(self, state):
		try:
			return r'motion'

		except AttributeError:
			return None

	def type_precedence(self, state):
		try:
			return 0

		except AttributeError:
			return None
	def motion_precedence(self, state):
		try:
			return 0

		except AttributeError:
			return None
	def debatable(self, state):
		try:
			return True

		except AttributeError:
			return None
	def may_interrupt(self, state):
		try:
			return False

		except AttributeError:
			return None
	def must_be_seconded(self, state):
		try:
			return True

		except AttributeError:
			return None
	def vote_required(self, state):
		try:
			return r'majority'

		except AttributeError:
			return None
	def decision_mode(self, state):
		try:
			return r'vote'

		except AttributeError:
			return None
	def subsidiaries_allowed(self, state, transition):
		try:
			if transition.__class__.__name__ == 'postpone_indefinitely':
				return False
			else:
				return True

		except AttributeError:
			return None
	def only_allowed_during_or_after_voting(self, state):
		try:
			return False

		except AttributeError:
			return None
	# RRO section ref: 24

	def renewable(self, state):
		try:
			"only after the state of affairs has changed" # askUser defaults to True


		except AttributeError:
			return None
	def reconsiderable(self, state, transition):
		try:
			return True

		except AttributeError:
			return None
	def to_be_entered_on_the_record_when_made(self, state):
		try:
			return False

		except AttributeError:
			return None
	def amendable(self, state):
		try:
			return True

		except AttributeError:
			return None
	def requires_target(self, state):
		try:
			return False

		except AttributeError:
			return None
	def category(self, state):
		try:
			return r'none'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'unknown'

		except AttributeError:
			return None
	def unimplemented(self, state):
		try:
			return False

		except AttributeError:
			return None

	def rror_section_ref(self, state):
		try:
			return r'4'

		except AttributeError:
			return None


# no longer applies
#
# Here are the rules for when a given motion may be applied
# to any Robert's Rules motion:
#
# 1) If proposed motion is an amendment, and pending motion
#    specifies "amendable", then that decides it.
#
# 2) Otherwise, all of the following must be satisifed:
#  2a) If proposed initiative is a subsidiary, then
#      subsidiaries_allowed must be true on the pending motion.
#  2b) If "applies only to: VALUE" is specified on the proposed motion,
#      then the pending motion must be of type VALUE.
#  2c) If both the pending motion and the proposed initiative are on
#      the precedence list, then the precedence of the proposed initiative
#      must be higher.
#  2d) Principal motions may never be applied to another motion.
#  2e) If the proposed motion is "only allowed during or after voting",
#      then state.currently_voting must be True




	

	def isValid(self, state): 

	    # motions requiring a target are only valid if they have one
	    if self.requires_target(state):
	        return self.find_targets(state)

	    # motions are invalid if any live initiatives does not yield to them
	    for i in state.getLiveInitiatives():
	        if not i.yieldsTo(state, self):
	            return False

	    # by default, motions are valid
	    return True

	def find_targets(self, state):
	    return []

	# should this be []?

	def yieldsTo(self, state, initiative):

	    precedenceList = [ \
	        'fix_time_to_which_to_adjourn_as_privileged', \
	        'adjourn_as_privileged', \
	        'recess_as_privileged', \
	        'question_of_privilege_as_privileged', \
	        'call_for_the_orders_of_the_day_as_privileged', \
	        'lay_on_the_table', \
	        'previous_question', \
	        'limit_or_extend_debate_as_subsidiary', \
	        'postpone_to_a_certain_time', \
	        'refer_to_committee', \
	        'amend', \
	        'postpone_indefinitely', \
	        'main_motion', \
	        ]
	    precedenceList.reverse() # so higher precedence = higher index

	    try:
	        self_prec = precedenceList.index(self.internal_name)
	        init_prec = precedenceList.index(initiative.internal_name)
	        if init_prec <= self_prec:
	            return False
	    except ValueError:
	        pass

	    return True
	
	def snippets():
	    if isinstance(initiative, subsidiary_motion):
	       if not self.subsidiaries_allowed(state, initiative):
		  return False


	    # applies_only_to_type may or may not be specified, so we must catch
	    # AttributeError
	    # We catch KeyError in case the value of "applies_only_to_type" is 
	    # a mistake.  
	    try:
		if not isinstance(self, globals()[initiative.applies_only_to_type(state)]):
	                return False
	    except AttributeError, KeyError:
	        pass

	    if isinstance(initiative, principal_motion):
	       return False		  

	    if initiative.only_allowed_during_or_after_voting(state) and (not state.currently_voting):
	       return False		  

class privileged_motion(rro_motion):
	name = 'Privileged motion'

	internal_name = 'privileged_motion'

	def type(self, state):
		try:
			return r'rro_motion'

		except AttributeError:
			return None

	def type_precedence(self, state):
		try:
			return 10

		except AttributeError:
			return None
	def debatable(self, state):
		try:
			return False

		except AttributeError:
			return None
	def subsidiaries_allowed(self, state, transition):
		try:
			return True

		except AttributeError:
			return None




	def summary(self, state):
		try:
			return r'Privileged Motions do not relate to the pending question, take precedence of all other questions, and are undebatable. They cannot have subsidiary motions applied to them, except that the motions "to fix the time to which to adjourn" and "to take a recess" may be amended. But after the assembly has actually taken up the orders of the day or a question of privilege, debate and amendment are permitted and the subsidiary motions may be applied the same as on any main motion.'

		except AttributeError:
			return None

	def rro_section_ref(self, state):
		try:
			return r'9'

		except AttributeError:
			return None
	def rror_section_ref(self, state):
		try:
			return r'14'

		except AttributeError:
			return None
	# extra RROR section ref for non-debatability: 35


	

	def isValid(self, state): 
	    if state.openForPrincipalMotion():
	      return False
	      
	    else:
	      return rro_motion.isValid(self,state)

class incidental_motion(rro_motion):
	name = 'Incidental motion'

	internal_name = 'incidental_motion'

	def type(self, state):
		try:
			return r'rro_motion'

		except AttributeError:
			return None

	def type_precedence(self, state):
		try:
			return 20

		except AttributeError:
			return None
	def debatable(self, state):
		try:
			return False

		except AttributeError:
			return None
	def amendable(self, state):
		try:
			return False

		except AttributeError:
			return None
	def subsidiaries_allowed(self, state, transition):
		try:
			if transition.__class__.__name__ == 'postpone_indefinitely':
				return False
			else:
				return True

		except AttributeError:
			return None

	def summary(self, state):
		try:
			return r'Incidental Motions arise out of a pending question. They take precedence of and must be decided before the question out of which they arise; or, they are incidental to a question that has just been pending and should be decided before any other business is taken up.'

		except AttributeError:
			return None

	def rro_section_ref(self, state):
		try:
			return r'8'

		except AttributeError:
			return None
	def rror_section_ref(self, state):
		try:
			return r'13'

		except AttributeError:
			return None



class subsidiary_motion(rro_motion):
	name = 'Subsidiary motion'

	internal_name = 'subsidiary_motion'

	def type(self, state):
		try:
			return r'rro_motion'

		except AttributeError:
			return None

	def type_precedence(self, state):
		try:
			return 30

		except AttributeError:
			return None
	def requires_target(self, state):
		try:
			return True

		except AttributeError:
			return None
	def applies_only_to_type(self, state):
		try:
			return r'principal_motion'

		except AttributeError:
			return None

	def summary(self, state):
		try:
			return r'Subsidiary Motions are applied to other motions in order to modify them, hasten or postpone action on them, refer them to a committee, or kill them entirely.'

		except AttributeError:
			return None

	def rro_section_ref(self, state):
		try:
			return r'7'

		except AttributeError:
			return None
	def rror_section_ref(self, state):
		try:
			return r'12'

		except AttributeError:
			return None




	
	# return list of valid targets, or empty list if none or invalid
	def find_targets(self, state):


	    targets = []

	    for i in state.getLiveInitiatives():

	        try:
	            # if out of order, return no targets
	            if not i.yieldsTo(state, self):
	              return []

	            # add potential targets to list
	            elif isinstance(i, globals()[self.applies_only_to_type(state)]):
	                targets.append(i)

	        except AttributeError, KeyError:
	            pass

	    return targets

class principal_motion(rro_motion):
	name = 'Principal motion'

	internal_name = 'principal_motion'

	def type(self, state):
		try:
			return r'rro_motion'

		except AttributeError:
			return None

	def type_precedence(self, state):
		try:
			return 40

		except AttributeError:
			return None
	def renewable(self, state):
		try:
			return True

		except AttributeError:
			return None
	def subsidiaries_allowed(self, state, transition):
		try:
			return True

		except AttributeError:
			return None

	def summary(self, state):
		try:
			return r'A Main or Principal Motion is a motion made to bring before the assembly, for its consideration, any particular subject. Main motions may be subdivided into Original Main Motions and Incidental Main Motions. Original Main Motions are those which bring before the assembly some new subject, generally in the form of a resolution, upon which action by the assembly is desired. Incidental Main Motions are those main motions that are incidental to, or relate to, the business of the assembly, or its past or future action, as, a committee\'s report on a resolution referred to it.'

		except AttributeError:
			return None

	def rro_section_ref(self, state):
		try:
			return r'6'

		except AttributeError:
			return None
	def rror_section_ref(self, state):
		try:
			return r'11'

		except AttributeError:
			return None




	
	def yieldsTo(self, state, initiative):
	    if isinstance(initiative, globals()['principal_motion']):
	        return False
	    else:
	        return rro_motion.yieldsTo(self, state, initiative)

class main_motion(principal_motion):
	name = 'Main motion'

	internal_name = 'main_motion'

	def type(self, state):
		try:
			return r'principal_motion'

		except AttributeError:
			return None

	def summary(self, state):
		try:
			return r'A Main Motion brings before the assembly a subject for consideration, upon which action is desired.'

		except AttributeError:
			return None

	def category(self, state):
		try:
			return r'primary'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'primary'

		except AttributeError:
			return None

	def rror_section_ref(self, state):
		try:
			return r'11'

		except AttributeError:
			return None



class rescind(principal_motion):
	name = 'Rescind'

	internal_name = 'rescind'

	def motion_to_form_of_name(self, state):
		try:
			return r'Motion to rescind'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'principal_motion'

		except AttributeError:
			return None

	def summary(self, state):
		try:
			return r'A previous action may be rescinded by a majority vote, provided notice of the motion to rescind was given at the previous meeting or in the call for this meeting. For urgent matters an action may be rescinded without notice by a two-thirds vote, or by a vote of a majority of the entire membership. Not in order when the motion to reconsider has been made and not yet called up. Not in order when the action is impossible to undo.'

		except AttributeError:
			return None

	def category(self, state):
		try:
			return r'action'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'anti'

		except AttributeError:
			return None

	# if notice given at previous meeting or in call for meeting:
	#     requires majority vote
	# else:
	#     requires 2/3 vote or vote of majority of entire membership

	def rro_section_ref(self, state):
		try:
			return r'25'

		except AttributeError:
			return None
	def rror_section_ref(self, state):
		try:
			return r'37'

		except AttributeError:
			return None



class reconsider(principal_motion):
	name = 'Reconsider'

	internal_name = 'reconsider'

	def motion_to_form_of_name(self, state):
		try:
			return r'Motion to reconsider'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'principal_motion'

		except AttributeError:
			return None

	def summary(self, state):
		try:
			return r''

		except AttributeError:
			return None

	def category(self, state):
		try:
			return r'action'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'anti'

		except AttributeError:
			return None

	def may_interrupt(self, state):
		try:
			return True

		except AttributeError:
			return None
	def reconsiderable(self, state, transition):
		try:
			return False

		except AttributeError:
			return None

	def debatable(self, state):
		try:
			return (self.parentInitiative().debatable(state))
		except AttributeError:
			return None
	def subsidiaries_allowed(self, state, transition):
		try:
			return True

		except AttributeError:
			return None
	def amendable(self, state):
		try:
			return False

		except AttributeError:
			return None

	# "Another {it interpretation problem/} is that RRO does not explicitly comment on whether postpone indefinitely/to certain day and commit apply to this motion. (This is a special case of the interpretation problem for all principal motions.)" 

	#"The following rules say that a motion to reconsider all motions other than incidental or subsidiary motions is to be entered on the record; and a motion to reconsider an incidental or a subsidiary motion is to be entered unless the vote on that motion had the effect of removing the entire subject from before the assembly (RRO 27, pp. 77--8). (This latter predicate has to be defined by further rules.)"

	def summary(self, state):
		try:
			return r'This motion must be made by someone who voted with the prevailing side (but any member may second it). It can be made only on the day the vote to be reconsidered was taken, or on the next succeeding day. The making of the motion has a higher rank than its consideration. The motion to reconsider can be made practically any time, but its consideration has only the rank of the motion to be reconsidered. When the motion to reconsider is "called up" (after any pending pusiness is disposed of) it has the preference over all other main motions and general orders. Making the motion suspends all action that the original motion would have required until the reconsideration is acted upon. Adopting the motion places before the assembly the original question.'

		except AttributeError:
			return None

	def rro_section_ref(self, state):
		try:
			return r'26,27'

		except AttributeError:
			return None
	def rror_section_ref(self, state):
		try:
			return r'36'

		except AttributeError:
			return None



class limit_or_extend_debate(transition):
	name = 'Limit or extend debate'

	internal_name = 'limit_or_extend_debate'


	def type(self, state):
		try:
			return r'when_(another_motion_is_pending):_subsidiary;_when_(not_another_motion_is_pending):_principal;_(motion)'

		except AttributeError:
			return None





# TODO: automate this "conditional type" handling
#   user should be able to just type:
#TYPE:
#    WHEN (ANOTHER_MOTION_IS_PENDING): PRIVILEGED
#    WHEN (NOT ANOTHER_MOTION_IS_PENDING): PRINCIPAL
#  (motion)

# the (motion) at the end is the "at the least, we're this" base class
#  i guess you could get this by performing inference, but
#   no time to write that now



def limit_or_extend_debate(state):
    if state.openForPrincipalMotion():
        return limit_or_extend_debate_as_principal(state)
    else:
	return limit_or_extend_debate_as_subsidiary(state)

class limit_or_extend_debate_as_principal(principal_motion):
	name = 'Limit or extend debate as principal'

	internal_name = 'limit_or_extend_debate_as_principal'

	name = 'Limit or extend debate'

	def motion_to_form_of_name(self, state):
		try:
			return r'Motion to limit or extend debate'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'principal_motion'

		except AttributeError:
			return None

	def category(self, state):
		try:
			return r'regulatory'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'hasten action'

		except AttributeError:
			return None


	def debatable(self, state):
		try:
			return False

		except AttributeError:
			return None
	def vote_required(self, state):
		try:
			return r'two-thirds'

		except AttributeError:
			return None
	def amendable(self, state):
		try:
			return True

		except AttributeError:
			return None
	def subsidiaries_allowed(self, state, transition):
		try:
			return False

		except AttributeError:
			return None
	# from RRO 1915 text

	def summary(self, state):
		try:
			return r'Limits on debate, when set by a principal motion, remain in effect for the duration of a meeting. To limit or extend the limits of debate require two-thirds vote.'

		except AttributeError:
			return None

	def rro_section_ref(self, state):
		try:
			return r'34'

		except AttributeError:
			return None
	def ronr_section_ref(self, state):
		try:
			return r'10, 15'

		except AttributeError:
			return None



class limit_or_extend_debate_as_subsidiary(subsidiary_motion):
	name = 'Limit or extend debate as subsidiary'

	internal_name = 'limit_or_extend_debate_as_subsidiary'

	name = 'Limit or extend debate'

	def motion_to_form_of_name(self, state):
		try:
			return r'Motion to limit or extend debate'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'subsidiary_motion'

		except AttributeError:
			return None

	def category(self, state):
		try:
			return r'regulatory'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'hasten action'

		except AttributeError:
			return None


	# in order only when immediately pending question is debatable!
	def motion_precedence(self, state):
		try:
			return 3

		except AttributeError:
			return None
	def debatable(self, state):
		try:
			return False

		except AttributeError:
			return None
	def vote_required(self, state):
		try:
			return r'two-thirds'

		except AttributeError:
			return None
	def amendable(self, state):
		try:
			return True

		except AttributeError:
			return None
	def subsidiaries_allowed(self, state, transition):
		try:
			return False

		except AttributeError:
			return None
	# from RRO 1915 text

	def summary(self, state):
		try:
			return r'Motions to limit or extend the limits of debate require two-thirds vote. A motion to limit debate by default applies to the pending question, all incidental and subsidiary motions, and the motion to reconsider, subsequently made, as long as the order is in force; but a motion extending the limits of debate does not apply to any motions except the immediately pending one and such others as are specified. If a motion is adopted closing debate at a certain hour or after a certain time, the motions to postpone and to commit cannot be moved, but the pending question may be laid on the table, and if it is not taken from the table until after the hour appointed for closing the debate and taking the vote, no debate or motion to amend is allowed, as the chair should immediately put the question.'

		except AttributeError:
			return None

	def rro_section_ref(self, state):
		try:
			return r'34'

		except AttributeError:
			return None
	def rror_section_ref(self, state):
		try:
			return r'30'

		except AttributeError:
			return None
	def ronr_section_ref(self, state):
		try:
			return r'15'

		except AttributeError:
			return None




	
	# rro_motion.isValid together with find_targets below should work the same
	#
	# def isValid(self, state):
	#     q = state.getPendingMotion()
	#     if isinstance(q, RootInitiative):
	#         return False
	#     if q.debatable(state):
	#         return True
	#     else:
	#         return False

	def find_targets(self, state):

	    q = state.getPendingMotion()

	    if isinstance(q, RootInitiative):
	        return []

	    if q.debatable(state):
	        return [q]
	    else:
	        return []

class make_a_special_order(principal_motion):
	name = 'Make a special order'

	internal_name = 'make_a_special_order'

	def motion_to_form_of_name(self, state):
		try:
			return r'Motion to make a special order'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'principal_motion'

		except AttributeError:
			return None

	def summary(self, state):
		try:
			return r'To Make a Special Order requires a two-thirds vote, because it suspends all rules that interfere with its consideration at the specific time, except those relating to motions for adjournment or recess, or to questions of privilege or to special orders made before it was made.'

		except AttributeError:
			return None

	def category(self, state):
		try:
			return r'scheduling'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'hasten action'

		except AttributeError:
			return None

	def vote_required(self, state):
		try:
			return r'two-thirds'

		except AttributeError:
			return None

	def rro_section_ref(self, state):
		try:
			return r'13'

		except AttributeError:
			return None
	def rror_section_ref(self, state):
		try:
			return r'20'

		except AttributeError:
			return None



class make_a_general_order(principal_motion):
	name = 'Make a general order'

	internal_name = 'make_a_general_order'

	def motion_to_form_of_name(self, state):
		try:
			return r'Motion to make a general order'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'principal_motion'

		except AttributeError:
			return None

	def summary(self, state):
		try:
			return r'A General Order is part of the orders of the day, and may or may not specify a time. Even when a general order specifies a time, it does not suspend any rule, and therefore cannot interrupt business. But after the appointed hour has arrived it has the preference, when no question is pending, over all other questions except special orders and reconsideration.'

		except AttributeError:
			return None

	def category(self, state):
		try:
			return r'scheduling'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'hasten action'

		except AttributeError:
			return None

	def rro_section_ref(self, state):
		try:
			return r'13'

		except AttributeError:
			return None
	def rror_section_ref(self, state):
		try:
			return r'20'

		except AttributeError:
			return None



class division_of_the_assembly(incidental_motion):
	name = 'Division of the assembly'

	internal_name = 'division_of_the_assembly'

	def motion_to_form_of_name(self, state):
		try:
			return r'Division of the assembly'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'incidental_motion'

		except AttributeError:
			return None
	def only_allowed_during_or_after_voting(self, state):
		try:
			return True

		except AttributeError:
			return None
	def must_be_seconded(self, state):
		try:
			return False

		except AttributeError:
			return None
	def may_interrupt(self, state):
		try:
			return True

		except AttributeError:
			return None
	def decision_mode(self, state):
		try:
			return True

		except AttributeError:
			return None
	def unimplemented(self, state):
		try:
			return True

		except AttributeError:
			return None

	def summary(self, state):
		try:
			return r'A Division of the Assembly may be called for at any time after a question has been put, even after the vote has been announced and another has the floor, provided the vote was taken viva voce, or by show of hands, and it is called for before another motion has been made. This motion is made by saying, "I call for a division," or simply, "Division." The motion does not require obtaining the floor, nor a second, nor a vote. As soon as a division is called for, the chair proceeds to retake the vote by having members rise.'

		except AttributeError:
			return None

	def category(self, state):
		try:
			return r'misc'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'meta'

		except AttributeError:
			return None

	def rro_section_ref(self, state):
		try:
			return r'25'

		except AttributeError:
			return None
	def rror_section_ref(self, state):
		try:
			return r'25'

		except AttributeError:
			return None

	#TODO: right now, "only allowed during or after voting" depends of state.beginning_of_meeting



class motion_related_to_voting(incidental_motion):
	name = 'Motion related to voting'

	internal_name = 'motion_related_to_voting'

	def motion_to_form_of_name(self, state):
		try:
			return r'Motion related to voting'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'incidental_motion'

		except AttributeError:
			return None
	def unimplemented(self, state):
		try:
			return True

		except AttributeError:
			return None

	def summary(self, state):
		try:
			return r'It requires a majority vote to order the vote to be counted, or to be taken by yeas and nays (roll call) or by ballot. These motions are incidental to the question that is pending or has just been pending, and cannot be debated. When different methods are suggested, the vote is taken first on the one taking the most time. In practice the method of taking a vote is generally agreed upon without the formality of a vote.'

		except AttributeError:
			return None

	def only_allowed_during_or_after_voting(self, state):
		try:
			return True

		except AttributeError:
			return None
	def amendable(self, state):
		try:
			return True

		except AttributeError:
			return None

	def category(self, state):
		try:
			return r'misc'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'meta'

		except AttributeError:
			return None

	def rro_section_ref(self, state):
		try:
			return r'38'

		except AttributeError:
			return None
	def rror_section_ref(self, state):
		try:
			return r'25'

		except AttributeError:
			return None



class lay_on_the_table(subsidiary_motion):
	name = 'Lay on the table'

	internal_name = 'lay_on_the_table'

	def motion_to_form_of_name(self, state):
		try:
			return r'Motion to lay on the table'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'subsidiary_motion'

		except AttributeError:
			return None

	def summary(self, state):
		try:
			return r'The objective of this motion is to temporarily lay a question aside, in order to take up more urgent business. The Effect of the adoption of this motion is to place on the table (that is, in charge of the secretary) the pending question and everything adhering to it, including pending amendments and other subsidiary motions. All these questions go together to the table, and when taken from the table they all come up together.'

		except AttributeError:
			return None

	def motion_precedence(self, state):
		try:
			return 1

		except AttributeError:
			return None
	def debatable(self, state):
		try:
			return False

		except AttributeError:
			return None
	def amendable(self, state):
		try:
			return False

		except AttributeError:
			return None
	def subsidiaries_allowed(self, state, transition):
		try:
			return False

		except AttributeError:
			return None
	def reconsiderable(self, state, transition):
		try:
			return (state.was_accepted(self))
		except AttributeError:
			return None


	def getTargetType(self):
		return 'ancestor motion'

	def getPotentialTargets(self):
		result = []
		cur = self.prevMotion()
		while cur:
			result = result.append(cur)
			cur = cur.prevMotion()
			
		return result
	
	
	def motionAdopted(self, state):
		newState = subsidiary_motion.motionAdopted(self,state)
		
		if self.target:
		     (newState, subtree) = self.target.assignResultAndDetach(newState, 'table', transition = None, descendentLabel = 'table')
		     newState.subtreeTables['table'].append(subtree)
		
	

		return newState
	
	def category(self, state):
		try:
			return r'scheduling'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'delay'

		except AttributeError:
			return None

	## it is noted that a fundamental parlimentary principal is that suppression of debate should not happen w/o a 2/3 vote, and that this motion is in direct conflict to that. It is recommended that, if your assembly habitually abuses this motion to supress debate, then it should be changed to require a 2/3 vote.

	def rro_section_ref(self, state):
		try:
			return r'19'

		except AttributeError:
			return None
	def rror_section_ref(self, state):
		try:
			return r'28'

		except AttributeError:
			return None



class previous_question(subsidiary_motion):
	name = 'Previous question'

	internal_name = 'previous_question'

	def motion_to_form_of_name(self, state):
		try:
			return r'Previous question'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'subsidiary_motion'

		except AttributeError:
			return None

	def summary(self, state):
		try:
			return r'This is a motion to immediately end debate on the pending question and put it to vote.'

		except AttributeError:
			return None

	def category(self, state):
		try:
			return r'regulatory'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'hasten action'

		except AttributeError:
			return None

	def motion_precedence(self, state):
		try:
			return 2

		except AttributeError:
			return None
	def debatable(self, state):
		try:
			return False

		except AttributeError:
			return None
	def vote_required(self, state):
		try:
			return r'two-thirds'

		except AttributeError:
			return None
	def amendable(self, state):
		try:
			return False

		except AttributeError:
			return None
	def subsidiaries_allowed(self, state, transition):
		try:
			return False

		except AttributeError:
			return None
	def reconsiderable(self, state, transition):
		try:
			return (state.askUser(r'not (partly) executed'))
		except AttributeError:
			return None

	def rro_section_ref(self, state):
		try:
			return r'20'

		except AttributeError:
			return None




	
	def find_targets(self, state):

	    q = state.getPendingMotion()

	    if isinstance(q, RootInitiative):
	        return []

	    result = []

	    # stupid hack for orderless list to make q be default
	    if q.amendable(state) or q.debatable(state):
	        result.append(q)

	    result.extend([i for i in subsidiary_motion.find_targets(self, state)
	            if i.amendable(state) or i.debatable(state)])

	    return result
	    

class postpone_to_a_certain_time(subsidiary_motion):
	name = 'Postpone to a certain time'

	internal_name = 'postpone_to_a_certain_time'

	def motion_to_form_of_name(self, state):
		try:
			return r'Motion to postpone to a certain time'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'subsidiary_motion'

		except AttributeError:
			return None

	def category(self, state):
		try:
			return r'scheduling'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'delay'

		except AttributeError:
			return None

	# TODO: reconsiderable?

	def subsidiaries_allowed(self, state, transition):
		try:
			if transition.__class__.__name__ == 'previous_question':
				return True
			else:
				return False

		except AttributeError:
			return None

	def motion_precedence(self, state):
		try:
			return 4

		except AttributeError:
			return None
	def amendable(self, state):
		try:
			return (state.askUser(r'changes time of when the motion is being postponed to'))
		except AttributeError:
			return None
# or, "a motion to postpone to a certain time is only amendable by amending the time"
# askUser defaults to Yes

	def debatable(self, state):
		try:
			return True

		except AttributeError:
			return None
## but "not further than necessary for enabling the assembly to judge the propriety of the postponement"

	# Forms:
	# 
	# * postpone (to|and make special order for) the next meeting
	# 
	# * postpone (to|and make special order for) certain hour
	# 
	# * postpone until after a certain event -> always general order
	# 
	# * postpone and make special order for meeting -> THE special order for mtg

	def rro_section_ref(self, state):
		try:
			return r'21'

		except AttributeError:
			return None



class refer_to_committee(subsidiary_motion):
	name = 'Refer to committee'

	internal_name = 'refer_to_committee'

	def motion_to_form_of_name(self, state):
		try:
			return r'Motion to refer to committee'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'subsidiary_motion'

		except AttributeError:
			return None

	def summary(self, state):
		try:
			return r'The object of this motion is to have the motion clarified by a committee, before it can be dealt with by the assembly.'

		except AttributeError:
			return None

	def category(self, state):
		try:
			return r'action'

		except AttributeError:
			return None
	def category(self, state):
		try:
			return r'scheduling'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'delay'

		except AttributeError:
			return None


	def motion_precedence(self, state):
		try:
			return 5

		except AttributeError:
			return None
	def subsidiaries_allowed(self, state, transition):
		try:
			return False

		except AttributeError:
			return None
## note: this seems to disagree with the 1915 text, but I'll go with Prakken.

	def amendable(self, state):
		try:
			return (state.askUser(r'Alters committee') or state.askUser(r'instructs committee'))
		except AttributeError:
			return None
	# askUser defaults to "Yes"      

	# "These two rules say that a motion to refer to a committee is only amendable by altering the committee, or giving it instructions."

	def rro_section_ref(self, state):
		try:
			return r'22'

		except AttributeError:
			return None



class amend(subsidiary_motion):
	name = 'Amend'

	internal_name = 'amend'

	def motion_to_form_of_name(self, state):
		try:
			return r'Motion to amend'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'subsidiary_motion'

		except AttributeError:
			return None

	def category(self, state):
		try:
			return r'action'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'primary'

		except AttributeError:
			return None

	def motion_precedence(self, state):
		try:
			return 6

		except AttributeError:
			return None
	def renewable(self, state):
		try:
			return False

		except AttributeError:
			return None

	def subsidiaries_allowed(self, state, transition):
		try:
			if transition.__class__.__name__ == 'previous_question':
				return True
			else:
				return False

		except AttributeError:
			return None

	def amendable(self, state):
		try:
			return False

		except AttributeError:
			return None
	# except specially by motion to amend amendment

	def rro_section_ref(self, state):
		try:
			return r'23'

		except AttributeError:
			return None




	
	def find_targets(self, state):

	    q = state.getPendingMotion()

	    if isinstance(q, RootInitiative):
	        return []

	    if q.amendable(state):
	        return [q]

	    return [i for i in subsidiary_motion.find_targets(self, state)
	            if i.amendable(state)]

class amend_amendment(subsidiary_motion):
	name = 'Amend amendment'

	internal_name = 'amend_amendment'

	def motion_to_form_of_name(self, state):
		try:
			return r'Motion to amend an amendment'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'subsidiary_motion'

		except AttributeError:
			return None

	def category(self, state):
		try:
			return r'action'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'primary'

		except AttributeError:
			return None

	def motion_precedence(self, state):
		try:
			return 6

		except AttributeError:
			return None
	def applies_only_to_type(self, state):
		try:
			return r'amend'

		except AttributeError:
			return None
	def renewable(self, state):
		try:
			return False

		except AttributeError:
			return None
	def subsidiaries_allowed(self, state, transition):
		try:
			if transition.__class__.__name__ == 'previous_question':
				return True
			else:
				return False

		except AttributeError:
			return None
	def amendable(self, state):
		try:
			return False

		except AttributeError:
			return None

	def rro_section_ref(self, state):
		try:
			return r'23'

		except AttributeError:
			return None




	
	def find_targets(self, state):

	    q = state.getPendingMotion()

	    try:
		if isinstance(q, globals()[self.applies_only_to_type(state)]):
	            return [q]
	    except AttributeError, KeyError:
	        return []

class postpone_indefinitely(subsidiary_motion):
	name = 'Postpone indefinitely'

	internal_name = 'postpone_indefinitely'

	def motion_to_form_of_name(self, state):
		try:
			return r'Motion to postpone indefinitely'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'subsidiary_motion'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'anti'

		except AttributeError:
			return None


	def category(self, state):
		try:
			return r'action'

		except AttributeError:
			return None

	def motion_precedence(self, state):
		try:
			return 7

		except AttributeError:
			return None
	def amendable(self, state):
		try:
			return False

		except AttributeError:
			return None
	def subsidiaries_allowed(self, state, transition):
		try:
			if transition.__class__.__name__ == 'previous_question':
				return True
			else:
				return False

		except AttributeError:
			return None


	def rro_section_ref(self, state):
		try:
			return r'24'

		except AttributeError:
			return None



class point_of_order(incidental_motion):
	name = 'Point of order'

	internal_name = 'point_of_order'

	def motion_to_form_of_name(self, state):
		try:
			return r'Point of order'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'incidental_motion'

		except AttributeError:
			return None

	def must_be_seconded(self, state):
		try:
			return False

		except AttributeError:
			return None
	def decision_mode(self, state):
		try:
			return True

		except AttributeError:
			return None
	def subsidiaries_allowed(self, state, transition):
		try:
			return False

		except AttributeError:
			return None
	def may_interrupt(self, state):
		try:
			return False

		except AttributeError:
			return None

	def category(self, state):
		try:
			return r'meta'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'meta'

		except AttributeError:
			return None

	def rro_section_ref(self, state):
		try:
			return r'14'

		except AttributeError:
			return None



class point_of_information(incidental_motion):
	name = 'Point of information'

	internal_name = 'point_of_information'

	def motion_to_form_of_name(self, state):
		try:
			return r'Point of information'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'incidental_motion'

		except AttributeError:
			return None

	def must_be_seconded(self, state):
		try:
			return False

		except AttributeError:
			return None
	def decision_mode(self, state):
		try:
			return True

		except AttributeError:
			return None
	def subsidiaries_allowed(self, state, transition):
		try:
			return False

		except AttributeError:
			return None
	def may_interrupt(self, state):
		try:
			return True

		except AttributeError:
			return None

	def category(self, state):
		try:
			return r'meta'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'meta'

		except AttributeError:
			return None

	def rro_section_ref(self, state):
		try:
			return r'27'

		except AttributeError:
			return None



class appeal_from_decision_of_chair(incidental_motion):
	name = 'Appeal from decision of chair'

	internal_name = 'appeal_from_decision_of_chair'

	def motion_to_form_of_name(self, state):
		try:
			return r'Motion to appeal from decision of chair'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'incidental_motion'

		except AttributeError:
			return None

	def summary(self, state):
		try:
			return r'An appeal can be made to any decision of the chair.'

		except AttributeError:
			return None

	def category(self, state):
		try:
			return r'regulatory'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'meta'

		except AttributeError:
			return None

	def may_interrupt(self, state):
		try:
			return True

		except AttributeError:
			return None
	# "see table on p. 11"

	def debatable(self, state):
		try:
			return (not state.previous_question_pending() and (state.askUser(r'the appeal does not relate to indecorum, to transgressions of rules of speaking, or to priority of business')))
		except AttributeError:
			return None

## If the appeal is debatable, and if any of "lay on the table",  "postpone", or "previous question" are passed in regards to the appeal, they also apply to the main question. For example, " Thus, if the appeal is from the decision that a proposed amendment is out of order and the appeal is laid on the table, it would be absurd to come to final action on the main question and then afterwards reverse the decision of the chair and take up the amendment when there was no question to amend."

	def subsidiaries_allowed(self, state, transition):
		try:
			return (self.debatable(state) and ((transition.__class__.__name__ == 'motion')) or ((transition.__class__.__name__ == 'motion')))
		except AttributeError:
			return None

	## An appeal must be made immediately after the decision to be appealed, w/o and intervening business.

	def rro_section_ref(self, state):
		try:
			return r'14'

		except AttributeError:
			return None



class object_to_consideration(incidental_motion):
	name = 'Object to consideration'

	internal_name = 'object_to_consideration'

	def motion_to_form_of_name(self, state):
		try:
			return r'Object to the consideration of a question'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'incidental_motion'

		except AttributeError:
			return None

	def summary(self, state):
		try:
			return r'The objective of this motion is to entirely remove the subject from before the assembly.'

		except AttributeError:
			return None

	def category(self, state):
		try:
			return r'action'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'anti'

		except AttributeError:
			return None

	def requires_target(self, state):
		try:
			return True

		except AttributeError:
			return None
	def applies_only_to_type(self, state):
		try:
			return r'main_motion'

		except AttributeError:
			return None
	def may_interrupt(self, state):
		try:
			return True

		except AttributeError:
			return None
	def must_be_seconded(self, state):
		try:
			return False

		except AttributeError:
			return None
	def vote_required(self, state):
		try:
			return r'two-thirds'

		except AttributeError:
			return None
	def subsidiaries_allowed(self, state, transition):
		try:
			return False

		except AttributeError:
			return None

	def rro_section_ref(self, state):
		try:
			return r'23'

		except AttributeError:
			return None




	
	def find_targets(self, state):

	    q = state.getPendingMotion()

	    try:
	        # add potential targets to list
	        if isinstance(q, globals()[self.applies_only_to_type(state)]):
	            return [q]
	    except AttributeError, KeyError:
	        pass

	    return []

class request_to_withdraw_motion(incidental_motion):
	name = 'Request to withdraw motion'

	internal_name = 'request_to_withdraw_motion'

	def motion_to_form_of_name(self, state):
		try:
			return r'Motion to request leave to withdraw a motion'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'incidental_motion'

		except AttributeError:
			return None

	def requires_target(self, state):
		try:
			return True

		except AttributeError:
			return None

	def getTargetType(self):
		return 'ancestor motion'

	def getPotentialTargets(self):
		result = []
		cur = self.prevMotion()
		while cur:
			result = result.append(cur)
			cur = cur.prevMotion()
			
		return result
	
		# actually, it's supposed to be a motion made by you, i believe

	def may_interrupt(self, state):
		try:
			return True

		except AttributeError:
			return None

	def must_be_seconded(self, state):
		try:
			return False

		except AttributeError:
			return None


	def motionAdopted(self, state):
		newState = incidental_motion.motionAdopted(self,state)
		
		if self.target:
		     newState = self.target.assignResultAndRemove(newState, 'withdraw')
		
	

		return newState
	




	def category(self, state):
		try:
			return r'action'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'anti'

		except AttributeError:
			return None

	def rro_section_ref(self, state):
		try:
			return r'17'

		except AttributeError:
			return None

	# note: actually this one is kind of complicated; the chair is supposed to quickly ask for objections. if there are any, then the chair moves to permit withdrawal, and two people are supposed to second. then there must be a vote.


	
	def find_targets(self, state):

	    q = state.getPendingMotion()

	    if isinstance(q, RootInitiative):
	        return []
	    else:
	      return [q]

class suspend_the_rules(incidental_motion):
	name = 'Suspend the rules'

	internal_name = 'suspend_the_rules'

	def motion_to_form_of_name(self, state):
		try:
			return r'Motion to suspend the rules'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'incidental_motion'

		except AttributeError:
			return None


	def category(self, state):
		try:
			return r'meta'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'hasten action'

		except AttributeError:
			return None

	def reconsiderable(self, state, transition):
		try:
			return False

		except AttributeError:
			return None

	def vote_required(self, state):
		try:
			if ((state.askUser(r'Possibly deprives more than 1/3 of members of their right'))):
				return "two-thirds"
			if ((state.askUser(r'Deprives at most 1/3 of members of their right'))):
				return "majority"

		except AttributeError:
			return None

	def subsidiaries_allowed(self, state, transition):
		try:
			return False

		except AttributeError:
			return None

	def renewable(self, state):
		try:
			return False

		except AttributeError:
			return None
## Is renewable after an adjournment. But I assume that will happen by default anyways, without specifically programming that in.

## of course, it's renewable by general consent even so

## NOTE: You can't suspend a rule that protects absentees, even by unanimous consent. That must be done in the bylaws.

	def rro_section_ref(self, state):
		try:
			return r'18'

		except AttributeError:
			return None



class take_from_the_table(principal_motion):
	name = 'Take from the table'

	internal_name = 'take_from_the_table'

	def motion_to_form_of_name(self, state):
		try:
			return r'Motion to take from the table'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'principal_motion'

		except AttributeError:
			return None

	def summary(self, state):
		try:
			return r'This motion can be used to order that motions laying on the table (19) are taken up again by the assembly.'

		except AttributeError:
			return None

	def category(self, state):
		try:
			return r'scheduling'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'hasten action'

		except AttributeError:
			return None

	# Prakken had ref: "laying on the table (19) are taken up again by the assembly"
	def debatable(self, state):
		try:
			return False

		except AttributeError:
			return None
	def amendable(self, state):
		try:
			return False

		except AttributeError:
			return None
	def subsidiaries_allowed(self, state, transition):
		try:
			return False

		except AttributeError:
			return None
	# prakken's ref: RRO 19, pp. 54,56

	def reconsiderable(self, state, transition):
		try:
			return (state.askUser(r'rejected the first time'))
		except AttributeError:
			return None

	def rro_section_ref(self, state):
		try:
			return r'19'

		except AttributeError:
			return None



class fix_time_to_which_to_adjourn(transition):
	name = 'Fix time to which to adjourn'

	internal_name = 'fix_time_to_which_to_adjourn'


	def type(self, state):
		try:
			return r'when_(another_motion_is_pending):_privileged;_when_(not_another_motion_is_pending):_principal;_(motion)'

		except AttributeError:
			return None

	def summary(self, state):
		try:
			return r'The time fixed cannot be beyond the time of the next meeting.'

		except AttributeError:
			return None





# TODO: automate this "conditional type" handling
#   user should be able to just type:
#TYPE:
#    WHEN (ANOTHER_MOTION_IS_PENDING): PRIVILEGED
#    WHEN (NOT ANOTHER_MOTION_IS_PENDING): PRINCIPAL
#  (motion)

# the (motion) at the end is the "at the least, we're this" base class
#  i guess you could get this by performing inference, but
#   no time to write that now



def fix_time_to_which_to_adjourn(state):
    if state.openForPrincipalMotion():
       return fix_time_to_which_to_adjourn_as_principal(state)
    else:
	return fix_time_to_which_to_adjourn_as_privileged(state)

class fix_time_to_which_to_adjourn_as_principal(principal_motion):
	name = 'Fix time to which to adjourn as principal'

	internal_name = 'fix_time_to_which_to_adjourn_as_principal'

	name = 'Fix time to which to adjourn'

	def motion_to_form_of_name(self, state):
		try:
			return r'Motion to fix time to which to adjourn (principal motion)'

		except AttributeError:
			return None


	name = 'Fix time to which to adjourn'


	def type(self, state):
		try:
			return r'principal_motion'

		except AttributeError:
			return None

	def category(self, state):
		try:
			return r'meta'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'adjourn'

		except AttributeError:
			return None

	def amendable(self, state):
		try:
			return (state.askUser(r'Amendment changes the time of proposed meeting'))
		except AttributeError:
			return None
	# askUser defaults to "Yes"

	def subsidiaries_allowed(self, state, transition):
		try:
			if transition.__class__.__name__ == 'postpone_indefinitely':
				return False
			else:
				return True

		except AttributeError:
			return None

	# SUMMARY: "If made in an assembly that already has provided for another meeting on the same or the next day, or if made in an assembly when no question is pending, this is a main motion."

	def rro_section_ref(self, state):
		try:
			return r'10'

		except AttributeError:
			return None
	def rror_section_ref(self, state):
		try:
			return r'16'

		except AttributeError:
			return None



class fix_time_to_which_to_adjourn_as_privileged(privileged_motion):
	name = 'Fix time to which to adjourn as privileged'

	internal_name = 'fix_time_to_which_to_adjourn_as_privileged'

	name = 'Fix time to which to adjourn'

	def motion_to_form_of_name(self, state):
		try:
			return r'Motion to fix time to which to adjourn (privileged motion)'

		except AttributeError:
			return None

	name = 'Fix time to which to adjourn'



	def type(self, state):
		try:
			return r'privileged_motion'

		except AttributeError:
			return None

	def category(self, state):
		try:
			return r'meta'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'adjourn'

		except AttributeError:
			return None

	def motion_precedence(self, state):
		try:
			return 1

		except AttributeError:
			return None
	def amendable(self, state):
		try:
			return (state.askUser(r'Amendment changes the time of proposed meeting'))
		except AttributeError:
			return None

	def subsidiaries_allowed(self, state, transition):
		try:
			if transition.__class__.__name__ == 'postpone_indefinitely':
				return False
			else:
				return True

		except AttributeError:
			return None

	def summary(self, state):
		try:
			return r'The time fixed cannot be beyond the time of the next meeting.'

		except AttributeError:
			return None

	def rro_section_ref(self, state):
		try:
			return r'10'

		except AttributeError:
			return None
	def rror_section_ref(self, state):
		try:
			return r'16'

		except AttributeError:
			return None



class adjourn_as_privileged(privileged_motion):
	name = 'Adjourn as Privileged'

	internal_name = 'adjourn_as_privileged'

	name = 'Adjourn'

	def motion_to_form_of_name(self, state):
		try:
			return r'Motion to adjourn'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'privileged_motion'

		except AttributeError:
			return None


	def category(self, state):
		try:
			return r'meta'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'adjourn'

		except AttributeError:
			return None

	def motion_precedence(self, state):
		try:
			return 2

		except AttributeError:
			return None
	def reconsiderable(self, state, transition):
		try:
			return False

		except AttributeError:
			return None
	def amendable(self, state):
		try:
			return False

		except AttributeError:
			return None
	def subsidiaries_allowed(self, state, transition):
		try:
			return False

		except AttributeError:
			return None
	def renewable(self, state):
		try:
			return (state.askUser(r'Business has been transacted or progress has been made in debate since the last time it was made/renewed'))
		except AttributeError:
			return None

	def rro_section_ref(self, state):
		try:
			return r'11'

		except AttributeError:
			return None



class adjourn_as_principal(principal_motion):
	name = 'Adjourn as Principal'

	internal_name = 'adjourn_as_principal'

	name = 'Adjourn'

	def motion_to_form_of_name(self, state):
		try:
			return r'Motion to adjourn'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'principal_motion'

		except AttributeError:
			return None


	def category(self, state):
		try:
			return r'meta'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'adjourn'

		except AttributeError:
			return None

	def motion_precedence(self, state):
		try:
			return 2

		except AttributeError:
			return None
	def reconsiderable(self, state, transition):
		try:
			return False

		except AttributeError:
			return None
	def amendable(self, state):
		try:
			return False

		except AttributeError:
			return None
	def subsidiaries_allowed(self, state, transition):
		try:
			return False

		except AttributeError:
			return None
	def renewable(self, state):
		try:
			return (state.askUser(r'Business has been transacted or progress has been made in debate since the last time it was made/renewed'))
		except AttributeError:
			return None

	def rro_section_ref(self, state):
		try:
			return r'11'

		except AttributeError:
			return None



class recess_as_principal(principal_motion):
	name = 'Recess as principal'

	internal_name = 'recess_as_principal'

	name = 'Recess'

	def motion_to_form_of_name(self, state):
		try:
			return r'Motion to take a recess'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'principal_motion'

		except AttributeError:
			return None


	def category(self, state):
		try:
			return r'meta'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'adjourn'

		except AttributeError:
			return None

	def motion_precedence(self, state):
		try:
			return 3

		except AttributeError:
			return None
	def reconsiderable(self, state, transition):
		try:
			return False

		except AttributeError:
			return None
	def amendable(self, state):
		try:
			return True

		except AttributeError:
			return None
	# amendable: ONLY WHEN "amendment changes length of recess"
	def subsidiaries_allowed(self, state, transition):
		try:
			return False

		except AttributeError:
			return None
	def renewable(self, state):
		try:
			return (state.askUser(r'Business has been transacted or progress has been made in debate since the last time it was made/renewed'))
		except AttributeError:
			return None

	def rro_section_ref(self, state):
		try:
			return r'11'

		except AttributeError:
			return None



class recess_as_privileged(privileged_motion):
	name = 'Recess as privileged'

	internal_name = 'recess_as_privileged'

	name = 'Recess'

	def motion_to_form_of_name(self, state):
		try:
			return r'Motion to take a recess'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'privileged_motion'

		except AttributeError:
			return None


	def category(self, state):
		try:
			return r'meta'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'adjourn'

		except AttributeError:
			return None

	def motion_precedence(self, state):
		try:
			return 3

		except AttributeError:
			return None
	def reconsiderable(self, state, transition):
		try:
			return False

		except AttributeError:
			return None
	def amendable(self, state):
		try:
			return True

		except AttributeError:
			return None
	# amendable: ONLY WHEN "amendment changes length of recess"
	def subsidiaries_allowed(self, state, transition):
		try:
			return False

		except AttributeError:
			return None
	def renewable(self, state):
		try:
			return (state.askUser(r'Business has been transacted or progress has been made in debate since the last time it was made/renewed'))
		except AttributeError:
			return None

	def rro_section_ref(self, state):
		try:
			return r'11'

		except AttributeError:
			return None



class question_of_privilege_as_privileged(privileged_motion):
	name = 'Question of privilege as privileged'

	internal_name = 'question_of_privilege_as_privileged'

	name = 'Question of privilege'

	def motion_to_form_of_name(self, state):
		try:
			return r'Motion to raise a question of privilege'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'privileged_motion'

		except AttributeError:
			return None

	def summary(self, state):
		try:
			return r'This motion concerns a question relating to the rights and privileges of the assembly, or any of its members.'

		except AttributeError:
			return None

	def category(self, state):
		try:
			return r'meta'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'meta'

		except AttributeError:
			return None

	def debatable(self, state):
		try:
			return False

		except AttributeError:
			return None
	# though apparently it can give rise to a debatable motion

	def may_interrupt(self, state):
		try:
			return (state.askUser(r'Requires immediate action'))
		except AttributeError:
			return None

	def motion_precedence(self, state):
		try:
			return 4

		except AttributeError:
			return None
	def amendable(self, state):
		try:
			return False

		except AttributeError:
			return None
	def subsidiaries_allowed(self, state, transition):
		try:
			return True

		except AttributeError:
			return None

	def rro_section_ref(self, state):
		try:
			return r'12, 9, 35'

		except AttributeError:
			return None




class question_of_privilege_as_principal(principal_motion):
	name = 'Question of privilege as principal'

	internal_name = 'question_of_privilege_as_principal'

	name = 'Question of privilege'

	def motion_to_form_of_name(self, state):
		try:
			return r'Motion to raise a question of privilege'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'principal_motion'

		except AttributeError:
			return None

	def summary(self, state):
		try:
			return r'This motion concerns a question relating to the rights and privileges of the assembly, or any of its members.'

		except AttributeError:
			return None

	def category(self, state):
		try:
			return r'meta'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'meta'

		except AttributeError:
			return None

	def debatable(self, state):
		try:
			return False

		except AttributeError:
			return None
	# though apparently it can give rise to a debatable motion

	def may_interrupt(self, state):
		try:
			return (state.askUser(r'Requires immediate action'))
		except AttributeError:
			return None

	def motion_precedence(self, state):
		try:
			return 4

		except AttributeError:
			return None
	def amendable(self, state):
		try:
			return False

		except AttributeError:
			return None
	def subsidiaries_allowed(self, state, transition):
		try:
			return True

		except AttributeError:
			return None

	def rro_section_ref(self, state):
		try:
			return r'12, 9, 35'

		except AttributeError:
			return None



class call_for_the_orders_of_the_day_as_privileged(privileged_motion):
	name = 'Call for the orders of the day as privileged'

	internal_name = 'call_for_the_orders_of_the_day_as_privileged'

	name = 'Call for the orders of the day'

	def motion_to_form_of_name(self, state):
		try:
			return r'Call for the orders of the day'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'privileged_motion'

		except AttributeError:
			return None

	def summary(self, state):
		try:
			return r'Some motions are assigned to a special time. When that time comes, this motion can be used to call them up.'

		except AttributeError:
			return None

	def category(self, state):
		try:
			return r'scheduling'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'hasten action'

		except AttributeError:
			return None

	def motion_precedence(self, state):
		try:
			return 5

		except AttributeError:
			return None
	def may_interrupt(self, state):
		try:
			return True

		except AttributeError:
			return None
	def must_be_seconded(self, state):
		try:
			return False

		except AttributeError:
			return None
	def subsidiaries_allowed(self, state, transition):
		try:
			if transition.__class__.__name__ == 'postpone_indefinitely':
				return False
			else:
				return True

		except AttributeError:
			return None
	def amendable(self, state):
		try:
			return False

		except AttributeError:
			return None
	def renewable(self, state):
		try:
			return (state.askUser(r'the business that was pending when it was first made has been dealt with'))
		except AttributeError:
			return None
## should formalize

	def rro_section_ref(self, state):
		try:
			return r'13, 61 (p. 198)'

		except AttributeError:
			return None



class call_for_the_orders_of_the_day_as_principal(principal_motion):
	name = 'Call for the orders of the day as principal'

	internal_name = 'call_for_the_orders_of_the_day_as_principal'

	name = 'Call for the orders of the day'

	def motion_to_form_of_name(self, state):
		try:
			return r'Call for the orders of the day'

		except AttributeError:
			return None

	def type(self, state):
		try:
			return r'principal_motion'

		except AttributeError:
			return None

	def summary(self, state):
		try:
			return r'Some motions are assigned to a special time. When that time comes, this motion can be used to call them up.'

		except AttributeError:
			return None

	def category(self, state):
		try:
			return r'scheduling'

		except AttributeError:
			return None
	def purpose(self, state):
		try:
			return r'hasten action'

		except AttributeError:
			return None

	def motion_precedence(self, state):
		try:
			return 5

		except AttributeError:
			return None
	def may_interrupt(self, state):
		try:
			return True

		except AttributeError:
			return None
	def must_be_seconded(self, state):
		try:
			return False

		except AttributeError:
			return None
	def subsidiaries_allowed(self, state, transition):
		try:
			if transition.__class__.__name__ == 'postpone_indefinitely':
				return False
			else:
				return True

		except AttributeError:
			return None
	def amendable(self, state):
		try:
			return False

		except AttributeError:
			return None
	def renewable(self, state):
		try:
			return (state.askUser(r'the business that was pending when it was first made has been dealt with'))
		except AttributeError:
			return None
## should formalize

	def rro_section_ref(self, state):
		try:
			return r'13, 61 (p. 198)'

		except AttributeError:
			return None




class initial_state(Default_initial_state.initial_state):
	name = 'INITIAL STATE'

	internal_name = 'initial_state'

	def type(self, state):
		try:
			return r'initial_state'

		except AttributeError:
			return None




	
	# TODO: remove the "state" arg; what's that good for, anyways?
	def initialStateAllowsApplicationOf(self, state, initiative):    
	    if isinstance(initiative, subsidiary_motion):
	       return False

	    if isinstance(initiative, rro_motion):
	        if initiative.only_allowed_during_or_after_voting(state):
		   if not state.beginning_of_meeting:	
		     return False		  
	           else:
	#             print 'dbg5'
		      pass
		
	    return True 

	def openForPrincipalMotion(self):
	    return isinstance(self.getPendingMotion(), RootInitiative)



all_classnames_list = ['rro_motion', 'privileged_motion', 'incidental_motion', 'subsidiary_motion', 'principal_motion', 'main_motion', 'rescind', 'reconsider', 'limit_or_extend_debate', 'limit_or_extend_debate_as_principal', 'limit_or_extend_debate_as_subsidiary', 'make_a_special_order', 'make_a_general_order', 'division_of_the_assembly', 'motion_related_to_voting', 'lay_on_the_table', 'previous_question', 'postpone_to_a_certain_time', 'refer_to_committee', 'amend', 'amend_amendment', 'postpone_indefinitely', 'point_of_order', 'point_of_information', 'appeal_from_decision_of_chair', 'object_to_consideration', 'request_to_withdraw_motion', 'suspend_the_rules', 'take_from_the_table', 'fix_time_to_which_to_adjourn', 'fix_time_to_which_to_adjourn_as_principal', 'fix_time_to_which_to_adjourn_as_privileged', 'adjourn_as_privileged', 'adjourn_as_principal', 'recess_as_principal', 'recess_as_privileged', 'question_of_privilege_as_privileged', 'question_of_privilege_as_principal', 'call_for_the_orders_of_the_day_as_privileged', 'call_for_the_orders_of_the_day_as_principal', 'initial_state']

conditional_typed_classnames_list = [('limit_or_extend_debate', 'motion'), ('fix_time_to_which_to_adjourn', 'motion')]

nonabstract_classnames_list = ['main_motion', 'rescind', 'reconsider', 'limit_or_extend_debate', 'make_a_special_order', 'make_a_general_order', 'division_of_the_assembly', 'motion_related_to_voting', 'lay_on_the_table', 'previous_question', 'postpone_to_a_certain_time', 'refer_to_committee', 'amend', 'amend_amendment', 'postpone_indefinitely', 'point_of_order', 'point_of_information', 'appeal_from_decision_of_chair', 'object_to_consideration', 'request_to_withdraw_motion', 'suspend_the_rules', 'take_from_the_table', 'fix_time_to_which_to_adjourn', 'adjourn_as_privileged', 'adjourn_as_principal', 'recess_as_principal', 'recess_as_privileged', 'question_of_privilege_as_privileged', 'question_of_privilege_as_principal', 'call_for_the_orders_of_the_day_as_privileged', 'call_for_the_orders_of_the_day_as_principal', 'initial_state']
