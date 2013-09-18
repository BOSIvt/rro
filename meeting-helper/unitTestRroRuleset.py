#!/usr/bin/python

import unittest
rules = __import__('rro_default_ruleset')

class TestRroRuleset(unittest.TestCase):

    class principalMotionStateStub:
        def __init__(self, prevState):
            self.prevState = prevState
        
        def prevMotion(self):
            return rules.principal_motion(self.prevState)

        def openForPrincipalMotion(self):
            return False

    def test_basic(self):
        state = 0

        a = rules.question_of_privilege(state)
        self.assertEqual(a.allowsApplicationOf(0,rules.amendment(state)), True)
        
        a = rules.call_for_the_orders_of_the_day(state)
        self.assertEqual(a.allowsApplicationOf(0,rules.amendment(state)), False)
        self.assertEqual(a.allowsApplicationOf(0,rules.lay_on_the_table(state)), True)
        
#     def test_average(self):
#         self.assertEqual(average([20, 30, 70]), 40.0)
#         self.assertEqual(round(average([1, 5, 7]), 1), 4.3)
#         self.assertRaises(ZeroDivisionError, average, [])
#         self.assertRaises(TypeError, average, 20, 30, 70)

    def test_validActs(self):
        import ParliamentCore
        p = ParliamentCore.ParliamentCore('rro_default_ruleset')

#        print 'p.nonAbstractActNames(): \n' + `p.nonAbstractActNames()`
        
        self.assert_('adjourn' in p.nonAbstractActNames())
        self.assert_('fix_time_of_adjournment' in p.nonAbstractActNames())
        self.assert_('incidental_motion' not in p.nonAbstractActNames())

#        print 'p.validActs(self.principalMotionStateStub(0)): \n' + `p.validActs(self.principalMotionStateStub(0))`

        self.assert_('adjourn' in p.validActs(self.principalMotionStateStub(0)))
        self.assert_('rescind' not in p.validActs(self.principalMotionStateStub(0)))
        
        

    def test_state(self):
        import ParliamentCore
        p = ParliamentCore.ParliamentCore('rro_default_ruleset')
        st = p.getInitialState(0)
        st2 = st.apply(ParliamentCore.rules.principal_motion, st.positionOfPrevMotion(), 0)
        #print `st2`
        #print `st2.transitionTree`
        #print `st2.transitionTree.nodes`
        #print `st2.position`
        #print `st2.prevMotion()`
        self.assertEquals(st2.prevMotion().name, 'Principal motion')

        print 'p.validActs(st2): \n' + `p.validActs(st2)`

        self.assert_('adjourn' in p.validActs(st2))
        self.assert_('rescind' not in p.validActs(st2))
        self.assert_('amendment' in p.validActs(st2))
        self.assert_('postpone_indefinitely' in p.validActs(st2))

        st3 = st2.apply(ParliamentCore.rules.incidental_motion, st2.positionOfPrevMotion(), 0)

        self.assertEquals(st3.prevMotion().name, 'Incidental motion')

        print 'p.validActs(st3): \n' + `p.validActs(st3)`

        self.assert_('adjourn' in p.validActs(st3))
        self.assert_('rescind' not in p.validActs(st3))
        self.assert_('amendment' not in p.validActs(st3))
        self.assert_('postpone_indefinitely' not in p.validActs(st3))

    def test_ParliamentCore(self):
        import ParliamentCore
        p = ParliamentCore.ParliamentCore('rro_default_ruleset')
        p.initState()
        p.applyToDefaultPosition('principal_motion')
        self.assertEquals(p.getPendingMotion().name, 'Principal motion')

        print 'p.currentValidActs():\n' + `p.currentValidActs()`

        self.assert_('adjourn' in p.currentValidActs())
        self.assert_('rescind' not in p.currentValidActs())
        self.assert_('amendment' in p.currentValidActs())
        self.assert_('postpone_indefinitely' in p.currentValidActs())
        
        p.applyToDefaultPosition('incidental_motion')

        self.assertEquals(p.getPendingMotion().name, 'Incidental motion')

        print 'p.currentValidActs():\n' + `p.currentValidActs()`

        self.assert_('adjourn' in p.currentValidActs())
        self.assert_('rescind' not in p.currentValidActs())
        self.assert_('amendment' not in p.currentValidActs())
        self.assert_('postpone_indefinitely' not in p.currentValidActs())
                     


unittest.main() # Calling from the command line invokes all tests
