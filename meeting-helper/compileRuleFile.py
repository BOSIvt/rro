#!/usr/bin/python

import sys, os, re, string, Closure, time




#########################################
#########################################
#
# CONSTANTS 
#
#########################################
#########################################

VERSION = .01
CLASS_INDENT = 0
FUNCTION_INDENT = 1
METACODE_INDENT = 2
CODE_INDENT = 3
SYNOPSIS = 'USAGE:\n\t\tcompileRuleFile.py path_to_rule_file\n'



HEADER = """


from Transitions import *
from Action import *
from Motion import *
from Initiative import *

from State import *
import Default_initial_state 

"""

#########################################
#########################################
#
# GLOBALS 
#
#########################################
#########################################


abstract_classnames_list = []
all_classnames_list = []
conditional_typed_classnames_list = []



#########################################
#########################################
#
# immediate subroutines of main() 
#
#########################################
#########################################




def loadRuleFile():
	try:
		ruleFilename = sys.argv[1]
	except:
		print SYNOPSIS
		sys.exit()

	ruleFileObj = open(ruleFilename)
	ruleFile = ruleFileObj.read()
	ruleFileObj.close()

	return (ruleFilename, ruleFile)


def parseRuleFile(ruleFile):
	result = ''

	sections = re.split(r'(?m)^---+', ruleFile)
	

	for section in sections:
		if re.search(r'(?i)name', section):
			result += (parseTransition().parseSection(section))
		else:
			result += (parseUnknown().parseSection(section))

	return result



def moduleLevelLists():
	result = ''
	result += '\nall_classnames_list = ' + repr(all_classnames_list) + '\n'

	result += '\nconditional_typed_classnames_list = ' + repr(conditional_typed_classnames_list) + '\n'
	
	nonabstract_classnames_list = [c for c in all_classnames_list
				       if c not in abstract_classnames_list]
	result += '\nnonabstract_classnames_list = ' + repr(nonabstract_classnames_list) + '\n'
	
	return result


def compileTimeComment(ruleFilename):
	return '# This Python module was automatically compiled from\n# Rule File "' + ruleFilename + '"\n# on ' + time.strftime('%c') + '\n# by the program compileRuleFile.py V' + `VERSION` + '\n\n' + HEADER

def writeCompiledRuleFile(ruleFilename, compiledRuleFile):
			# e.g. if infile is ruleFiles/rro_default.txt,
			# outfile is rro_default.py
	outFilename = ruleFilename
	outFilename = outFilename.replace('.txt','')
	outFilename += '_ruleset.py'
	outFilename = re.sub('.*/','', outFilename)
	   # result goes in current directory

	compiledFileObj = open(outFilename, 'w')
	compiledFileObj.write(compiledRuleFile)
	compiledFileObj.close()
	





#########################################
#########################################
#
# Parser class 
#
#########################################
#########################################




class parser:
	BASE_INDENT = CLASS_INDENT
	QUOTE_STORAGE_STRING = '"PARLIAMENT_INTERNAL_STORED_QUOTES_'
	elementsWithTransitionArgument = []



	def concatenateMultilines(self, section):
	        section = re.sub(r'\n[\t ]+([^\s#].*)', r'; \1', section)
		section = re.sub(r':\s*;', ': ', section)
		return section



	
	def parseLine(self,line):
		## preserve comments and whitespace and keep them 
		## "in the right place"

		if re.match(r'\s*#',line):
			self.result += line.strip() + '\n'
			return True
		if re.match(r'^\s*$',line):
			self.result += '\n'
			return True
		
		
	
	def parseSection(self,section):
		self.result = ''

		self.codeBlockMatches = re.findall(r'(?m)^{([^}]+)}', section)
		section = re.sub(r'(?m)^{([^}]+)}', '', section)

		section = self.concatenateMultilines(section)

		sectionLines = string.split(section, '\n')
		
		for line in sectionLines:
			self.parseLine(line)

		for codeBlockMatch in self.codeBlockMatches:
			self.result += self.indentText(codeBlockMatch, self.BASE_INDENT)
		


		return self.result


	def fixUpName(self, name):
		 return re.sub(r' ', '_', name.strip()).lower()


	def nameToFunctionDef(self, name, level):
		if name in self.elementsWithTransitionArgument:
			return self.functionDefString(name, level, ['self', 'state', 'transition'])
		else:
			return self.functionDefString(name, level, ['self', 'state'])



	def functionDefString(self, name, level, argumentList):
		return ('\t' * level) + 'def ' + name + '(' + string.join(argumentList, ', ') + '):\n'



	def classDefString(self, name, level, argumentList):
		if not re.match(r'^\w+$', name):
			raise NameError, 'Illegal transition name: ' + name
		
		
		return ('\t' * level) + 'class ' + name + '(' + string.join(argumentList, ', ') + '):\n'



	def indentText(self, text, indentLevel):
		text = re.sub('\n(?=.)', '\n' + '\t' * indentLevel, text)
		text = '\t' * indentLevel + text
		return text



	def indentCode(self, code):
		return self.indentText(code, CODE_INDENT)


	def indentMetaCode(self, code):
		return self.indentText(code, METACODE_INDENT)




	def storeQuotes(self, text, openQuotes=(r'"' + "'"), closeQuotes=None):
		if not closeQuotes:
			closeQuotes = openQuotes

		storedQuotes = []
		QUOTE_STORAGE_STRING = self.QUOTE_STORAGE_STRING
		
		openQuotesRE = '[' + openQuotes + ']'
		closeQuotesRE = '[' + closeQuotes + ']'
		notCloseQuotesRE = r'[^' + closeQuotes + ']' 
		
		def _storer(self, match):
			storedQuotes.append(match.group(1))
			return QUOTE_STORAGE_STRING + `len(storedQuotes) - 1` 			
	       		
		_storer_closure = Closure.Closure(_storer, Closure.Environment(vars()) )
		text = re.sub('(' + openQuotesRE + notCloseQuotesRE + '*' + closeQuotesRE + ')', _storer_closure, text)
		return (text, storedQuotes)



	def unstoreQuotes(self, text, storedQuotes):
		for i in range( len(storedQuotes) ):
			text = text.replace(self.QUOTE_STORAGE_STRING + `i`, storedQuotes[i])
		return text

#########################################
#########################################
#
# parseUnknown subclass 
#
#########################################
#########################################


	
class parseUnknown(parser):
	pass


#########################################
#########################################
#
# parseTransition subclass 
#
#########################################
#########################################


# "transition" is usually a "motion"
class parseTransition(parser):
	elementsWithTransitionArgument = ['subsidiaries_allowed', 'reconsiderable', 'allowsApplicationOf']
	methodsOfStateWhichWantCurrentMotionAdopted = ['was_accepted']
	BASE_INDENT = FUNCTION_INDENT


	def argListStr(self, fnName):
		listOfArgs = ['state']
		if fnName in self.elementsWithTransitionArgument:
			listOfArgs = ['state', 'transition']

		return '(' + string.join(listOfArgs, ', ') + ')' 



	def argListStrForState(self, fnName):
		listOfArgs = []
		if fnName in self.methodsOfStateWhichWantCurrentMotionAdopted:
			listOfArgs = ['self']

		return '(' + string.join(listOfArgs, ', ') + ')' 




	#########################################
        #########################################
	#
	# parseLine
	#
        #########################################
        #########################################

	def parseLine(self, line):
		####
		#### if line is a comment, then copy the comment and move on
		####
		if re.match(r'#',line):
			self.result += '\t' + line + '\n'
			return


		####
		#### if line is a Python block, then copy it and move on
		####
		m = re.match(r'^{([^}]+)}$', line)
		if m:
			self.result += self.indentText(m.group(1), FUNCTION_INDENT)
			return True


		####
		#### if superclass can parse, then move on
		####
		superResult = parser.parseLine(self,line)
		if superResult:
			return


		m = re.match(r'^(?i)name:(.*)',line)
		if m:
			self.parseName(m.group(1), line)
			return

		m = re.match(r'^(?i)internal name:(.*)',line)
		if m:
			self.parseInternalName(m.group(1), line)
			return

		m = re.match(r'^(?i)type:(.*)', line)
		if m:
			line = self.parseType(m.group(1), line)

		m = re.match(r'^(?i)applies only to type:(.*)',line)
		if m:
			self.parseAppliesOnlyToType(m.group(1), line)
			return
		
		m = re.match(r'^(?i)target:(.*)',line)
		if m:
			self.parseTarget(m.group(1), line)
			return

		m = re.match(r'^(?i)on adopt:(.*)',line)
		if m:
			self.parseOnAdopt(m.group(1), line)
			return

	        m = re.match(r'^(?i)on reject:(.*)',line)
		if m:
			self.parseOnReject(m.group(1), line)
			return


	        m = re.match(r'^(?i)(.*?)\s*:\s*(.*)', line)
		if m:
			self.parseArbitraryAttribute(m.group(1), m.group(2), line)
			return 
		

	##############################
	##############################
	# parseLine's subroutines
        ##############################
	##############################

	##############################
	# parseType
        ##############################


	def parseType(self, value, line):
		
		type = value

		(type, isAbstract) = re.subn(r'(?i)\(abstract\)', '', type)
		if isAbstract:
			abstract_classnames_list.append(self.name)
			self.isAbstract = True
			
				
		if re.search(r'[^\w ]', type):
			base_class = 'transition'
			m = re.search(r'\(([^()]+)\)\s*$', type)
			if m:
				base_class = m.group(1)
					
			sys.stderr.write('warning: conditional types not handled yet (in ' + self.name + ')\n')
			conditional_typed_classnames_list.append( (self.name, base_class) )  

			#TODO: handle when type is conditional
		else:
			self.superclass = self.fixUpName(type.strip())

			# MAGIC
			if self.superclass == 'initial_state':
				self.superclass = 'Default_initial_state.initial_state'
					

			self.result = self.result.replace( \
						self.classDefString(self.name, 0, ['transition']), \
						self.classDefString(self.name, 0, [self.superclass]) )

			# actually, let's have this be an attribute too
		return re.sub(r'^(?i)type:(.*)', r'type: "' + self.fixUpName(type) + r'"', line)


	##############################
	# parseInternalName
        ##############################

	# TODO/NOTE: if both "internal name" and "name" are present, then
	# "internal name" MUST come before
	# the "name" attribute

	def parseInternalName(self, value, line):
		rawName = value.strip()
		self.name = self.fixUpName(value)
		all_classnames_list.append(self.name)
		self.result += self.classDefString(self.name, 0, ['transition'])
		self.result += '\t' * FUNCTION_INDENT + "name = '%s'\n\n" % rawName
		self.result += '\t' * FUNCTION_INDENT + "internal_name = '%s'\n\n" % self.name

		return ''



	##############################
	# parseName
        ##############################

	def parseName(self, value, line):
		if not ('name' in dir(self)):
			self.parseInternalName(value, line)
		else:
			rawName = value.strip()	
			self.result += '\t' * FUNCTION_INDENT + "name = '%s'\n\n" % rawName

		return ''


	##############################
	# parseAppliesOnlyToType
        ##############################

	def parseAppliesOnlyToType(self, value, line):
		t = self.fixUpName(value)
		self.result += self.nameToFunctionDef("applies_only_to_type", 1) + self.indentMetaCode('try:\n') + self.indentCode(self.attributeTextToCode(t))  + '\n' + self.indentMetaCode('except AttributeError:\n\treturn None\n')
		return ''



	##############################
	# parseTarget
        ##############################


	def parseTarget(self, value, line):
		ANCESTOR_MOTION_CODE = """
	def getTargetType(self):
		return 'ancestor motion'

	def getPotentialTargets(self):
		result = []
		cur = self.prevMotion()
		while cur:
			result = result.append(cur)
			cur = cur.prevMotion()
			
		return result
	
	"""

	        rawTarget = value.strip()
		if rawTarget == 'ancestor motion':
		    self.result +=  ANCESTOR_MOTION_CODE
		#if rawTarget == 'currently pending motion':
		#	pass
		if rawTarget == 'previous motion':
		    pass

	##############################
	# parseOnAdopt
        #############################

	def parseOnAdopt(self, value, line):
		ON_ADOPT_CODE = """
	def motionAdopted(self, state):
		newState = %s.motionAdopted(self,state)
		%s

		return newState
	"""


		
	        procedureBody = self.parseAction(value.strip())
		self.result +=  ON_ADOPT_CODE % (self.superclass, procedureBody)
		return



	##############################
	# parseOnReject
        #############################
	def parseOnReject(self, value, line):
		ON_REJECT_CODE = """
	def motionAdopted(self, state):
		newState = %s.motionRejected(self,state)
		%s

		return newState
	"""

	        procedureBody = self.parseAction(value.strip())
		self.result += ON_REJECT_CODE % (self.superclass, procedureBody)
		return


	##############################
	# parseArbitraryAttribute
        #############################

	def parseArbitraryAttribute(self, name, value, line):

		name = self.fixUpName(name)
		value = value.strip()

		if not value:
		    return
				
		setattr(self, name, value)
#				self.result += self.nameToFunctionDef("applies_only_to", 1) + self.indentMetaCode('try:\n') + self.indentCode(self.attributeTextToCode(t))  + '\n' + self.indentMetaCode('except AttributeError:\n\t#return None\n')
		self.result += self.nameToFunctionDef(name, 1) + self.indentMetaCode('try:\n') + self.indentCode(self.attributeTextToCode(value))  + '\n'+ self.indentMetaCode('except AttributeError:\n\treturn None\n')

		return


	#########################################
        #########################################
	#
	# end of parseLine and its subroutines
	#
        #########################################
        #########################################





















	def attributeTextToCode(self, attributeText):
		attributeText = attributeText.strip()


		####
		#### quoted text -> string
		####
		m = re.match(r'^"(.*)"$', attributeText)
		if m:
			return 'return r\'%s\'\n' % m.group(1)

		####
		#### "yes" -> True
		####
		m = re.match(r'^(?i)yes$', attributeText)
		if m:
			return 'return True\n'

		####
		#### "no" -> False
		####
		m = re.match(r'^(?i)no$', attributeText)
		if m:
			return 'return False\n'

		####
		#### EXCEPT
		####
		m = re.match(r'EXCEPT \'(.+)\'', attributeText)
		if m:
			exception = "'" + self.fixUpName(m.group(1)) + "'"
					
			return 'if transition.__class__.__name__ == %s:\n\treturn False\nelse:\n\treturn True\n' % exception

		# todo: use isinstance?
#todo: make everything else case insensitive

		####
		#### IF or ONLY WHEN
		####
	        m1 = re.match(r'(?i)IF (.*)', attributeText)
	        m2 = re.match(r'(?i)ONLY WHEN (.*)', attributeText)
		m = m1 or m2
		if m:
			restOfLine = self.processCondition(m.group(1))
			return 'return ' + '(' + restOfLine + ')'

					    
		####
		#### ONLY 
		####
		m = re.match(r'ONLY \'(.+)\'', attributeText)
		if m:
			exception = "'" + self.fixUpName(m.group(1)) + "'"
			return 'if transition.__class__.__name__ == %s:\n\treturn True\nelse:\n\treturn False\n' % exception


		####
		#### numbers
		####
		m = re.match(r'([\d\.-/]+)', attributeText)
		if m:
			number = m.group(1)
			return 'return %s\n' % number

		####
		#### WHEN
		####
	        m = re.match(r'(WHEN ([^;]*?):[^;]*?;?)+', attributeText)
		if m:
			linesConditions = []
			linesValues = []
			resultLines = []
			
			lines = attributeText.split(';')
			for i in range(len(lines)):
				mLine = re.match(r'\s*WHEN (.*?):(.*)', lines[i])
				linesConditions.append(mLine.group(1).strip())
				linesValues.append(mLine.group(2).strip())
				linesConditions[i] = self.processCondition(linesConditions[i])
				resultLines.append('if (%s):\n\treturn %s\n' % (linesConditions[i], linesValues[i]) )
				#sys.stderr.write('APPENDED:' + 'if (%s):\n\treturn %s\n' % 	(linesConditions[i], linesValues[i]))
			
			return string.join(resultLines,'')

		
		return '%s\n\n' % attributeText
	        # should never be called?






		
	def processCondition(self, conditionText):

		####
		#### "this is" or "this" or "this initiative is"
		#### or "this motion", etc                          
		####
		conditionText = re.sub(r'(?i)\bthis(?: initiative| motion)? is ','this.', conditionText)
		conditionText = re.sub(r'(?i)\bthis(?: initiative| motion)? ','this.', conditionText)
		conditionText = re.sub(r'(?i)(\w+\.)\(([\w _]+)\)',r'(\1\2)', conditionText)

		####
		#### "parent initiative is"
		####
		conditionText = re.sub(r'(?i)\b(parent(?: initiative| motion)? is )([\w _]+)',r'\1(\2)', conditionText)
		conditionText = re.sub(r'(?i)\bparent(?: initiative| motion)? is ','self.parentInitiative().', conditionText)
		

		####
		#### AND/OR/NOT
		####		
		conditionText = re.sub(r'(?i)\bAND\b','and', conditionText)
		conditionText = re.sub(r'(?i)\bOR\b','or', conditionText)
		conditionText = re.sub(r'(?i)\bNOT\b','not', conditionText)



 		####
		#### some confusing stuff
		####		

		(conditionText, storedQuotes) = self.storeQuotes(conditionText)
		
		replaceFn = lambda m: r'state.' + self.fixUpName(m.group(1)) + self.argListStrForState(self.fixUpName(m.group(1)))
		conditionText = re.sub(r'(?<!\.)\(([\w ]+)\)', replaceFn, conditionText)



		replaceFn = lambda m: r'self.' + self.fixUpName(m.group(1)) + self.argListStr(self.fixUpName(m.group(1)))
		conditionText = re.sub(r'\( *this\.([\w ]+)\)', replaceFn, conditionText)


		replaceFn = lambda m: m.group(1) + self.fixUpName(m.group(2)) + self.argListStr(self.fixUpName(m.group(2)))
		conditionText = re.sub(r'([\w()]+\.)\(([\w ]+)\)', replaceFn, conditionText)
				

		(conditionText) = self.unstoreQuotes(conditionText, storedQuotes)

		searchRE = r'(?i)(motion|initiative) is ' + "'([^']+)'"
		replaceRE = r'(transition.__class__.__name__ == ' + "'" + r'\1' + "')" 
		conditionText = re.sub(searchRE, replaceRE, conditionText)



 		####
		#### text strings in conditions --> askUser(string)
		####		
		replaceRE = r'state.askUser(r' + "'" + r'\1' + "'" + r')'
		conditionText = re.sub('"(.*?)"', replaceRE, \
				       conditionText)


		####
		#### that's it
		####		

		return conditionText



        def parseAction(self, actionText):
		#print actionText
		if actionText == 'withdraw target':
			return """
		if self.target:
		     newState = self.target.assignResultAndRemove(newState, 'withdraw')
		
	"""
		if actionText == 'table target':
			return """
		if self.target:
		     (newState, subtree) = self.target.assignResultAndDetach(newState, 'table', transition = None, descendentLabel = 'table')
		     newState.subtreeTables['table'].append(subtree)
		
	"""
		
		return ''



#########################################
#########################################
#
# main() 
#
#########################################
#########################################

def main():
	(ruleFilename, ruleFile) = loadRuleFile()

	result = compileTimeComment(ruleFilename) 
	result += parseRuleFile(ruleFile)
	result += moduleLevelLists()

	writeCompiledRuleFile(ruleFilename, result)



main()


