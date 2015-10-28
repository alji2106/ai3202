# Alixandria Jimenez
# Assignment 6
# CSCI 3202 AI

import getopt
import sys

# Bayes network node
class Node:
	def __init__(self):
		self.marg = 0
		self.cond = {}
		self.name = ""
		self.parent = []
		self.child = []

# Code representation of bayes network graph
def network():
	pollutionNode = Node()
	smokerNode = Node()
	cancerNode = Node()
	xrayNode = Node()
	dyspnoeaNode = Node()
	
	pollutionNode.name = "p"
	smokerNode.name = "s"
	cancerNode.name = "c"
	xrayNode.name = "x"
	dyspnoeaNode.name = "d"
	
	pollutionNode.child.append(cancerNode)
	smokerNode.child.append(cancerNode)
	cancerNode.child.append(xrayNode)
	cancerNode.child.append(dyspnoeaNode)

	cancerNode.parent.append(smokerNode)
	cancerNode.parent.append(pollutionNode)
	xrayNode.parent.append(cancerNode)
	dyspnoeaNode.parent.append(cancerNode)

	pollutionNode.marg = 0.9
	smokerNode.marg = 0.3
	
	cancerNode.cond["~ps"] = 0.05
	cancerNode.cond["s~p"] = 0.05
	cancerNode.cond["~p~s"] = 0.02
	cancerNode.cond["~s~p"] = 0.02
	cancerNode.cond["ps"] = 0.03
	cancerNode.cond["sp"] = 0.03
	cancerNode.cond["p~s"] = 0.001
	cancerNode.cond["~sp"] = 0.001
	xrayNode.cond["c"] = 0.9
	xrayNode.cond["~c"] = 0.2
	dyspnoeaNode.cond["c"] = 0.65
	dyspnoeaNode.cond["~c"] = 0.3
	
	leNetwork = {"smoker": smokerNode, "pollution": pollutionNode, "cancer": cancerNode, "xray": xrayNode, "dyspnoea": dyspnoeaNode}
	return leNetwork
	
def newVal(network, arg, value):
	if arg == "p" or arg == "P":
		pollution = network["pollution"]
		pollution.marg = value
	elif arg == "s" or arg == "S":
		smoker = network["smoker"]
		smoker.marg = value
	else:
		return
# Marginal #
	
def calcM(network, arg):
	isOpp = False
	pollution = network["pollution"]
	smoker = network["smoker"]
	cancer = network["cancer"]
	xray = network["xray"]
	dyspnoea = network["dyspnoea"]
	if arg[0] == "~":
		# Will change to 1-marginal at end
		isOpp = True
		# Move to actual letter
		arg = arg[1]
	# For P and S these are already set or read in
	if arg == "P" or arg == "p":
		marg = pollution.marg
	elif arg == "S" or arg == "s":
		marg = smoker.marg
	# Relies on all combinations of P and S
	elif arg == "C" or arg == "c":
		m1 = cancer.cond["~ps"]*(1-pollution.marg)*(smoker.marg)
		m2 = cancer.cond["~p~s"]*(1-pollution.marg*(1-smoker.marg))
		m3 = cancer.cond["ps"]*pollution.marg*smoker.marg
		m4 = cancer.cond["p~s"]*pollution.marg*(1-smoker.marg)
		marg = m1 + m2 + m3 + m4
	elif arg == "X" or arg == "x":
		cancerMarg = calcM(network, "C")
		marg = xray.cond["c"]*cancerMarg
		marg += xray.cond["~c"]*(1-cancerMarg)
	elif arg == "D" or arg == "d":
		# Relies on cancer's marginal as well 
		cancerMarg = calcM(network, "c")
		marg = dyspnoea.cond["c"]*cancerMarg
		marg += dyspnoea.cond["~c"]*(1-cancerMarg)
	else:
		print"Please enter P, p, S, s, C, c, X, x, D, or d."
		return 0
	if isOpp:
		return 1-marg
	else:
		return marg

# Conditional #
def calcC(network, arg, con):
	isOpp = False
	if arg[0] == '~':
		isOpp = True
		newArg = arg[1]
	else:
		newArg = arg
	varList = []
	for i in range(0, len(con)):
		if con[i] == '~':
			i = i + 1
			var = con[i-1] + con[i]
			varList.append(var)
		else:
			varList.append(con[i])
		i = i + 1
	conList = varList
	if newArg == "p":
		node = network["pollution"]
	elif newArg == "s":
		node = network["smoker"]
	elif newArg == "c":
		node = network["cancer"]
	elif newArg == "x":
		node = network["xray"]
	elif newArg == "d":
		node = network["dyspnoea"]
	if (len(conList) == 0):
		return calcM(network, arg)
	elif con in node.cond:
		cond = node.cond[con]
	else: 
		return 1
	# Need conditionals for one two and three conditionals
	# somehow based on which network node it's currently on...
	if isOpp:
		return 1 - cond
	else:
		return cond
	return 1

# Joint #

# Begin Main Code #

bayesN = network()
try:
    opts, args = getopt.getopt(sys.argv[1:], "m:g:j:p:")
except getopt.GetoptError as err:
    print(err)
    sys.exit(2)
for o, a in opts:
    if o in ("-p"):
        print("flag: ", o)
        print("args: ", a)
        print(a[0])
        print(float(a[1:]))
        newVal(bayesN, a[0], float(a[1:]))
    elif o in ("-m"):
        print("flag: ", o)
        print("args: ", a)
        print(type(a))
        marginal = calcM(bayesN, a)
        print("marginal", a, marginal)
    elif o in ("-g"):
        print("flag: ", o)
        print("args: ", a)
        print(type(a))
        p = a.find("|")
        print(a[:p])
        print(a[p+1:])
        print "This is barely implemented"
        conditional = calcC(bayesN, a[:p], a[p+1:])
        print("conditional", a, conditional)
    elif o in ("-j"):
        print("flag: ", o)
        print("args: ", a)
        print("Not implemented")
    else:
        assert False, "Not an option."