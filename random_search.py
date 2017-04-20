from random import randint
from random import choice
import math
class Node(object):
	def __init__(self, val, left, right):
		self.val = val
		self.left = left
		self.right = right
		if isinstance(val, int):
			self.canConcat = True
		else:
			self.canConcat = left.canConcat and right.canConcat and val == 'c'
	def calc(self):
		if isinstance(self.val, int):
			return 1.0*self.val
		left = self.left.calc()
		right = self.right.calc()
		if self.val == '+':
			return left + right
		if self.val == '-':
			return left - right
		if self.val == '*':
			return left * right
		if self.val == '/':
			return left / right
		if self.val == '^':
			return math.pow(left, right)
		if self.val == 'c':
			return int(str(int(left))+str(int(right)))
	def __repr__(self):
		if self.left is None:
			return str(self.val)
		return "(" + str(self.left) +str(self.val) + str(self.right) + ")"
ops = ['c','+', '*', '-', '/', '^'] #
ops2 = ops[1:]

def randomCalc():
	nodes = []
	for I in range(1, 10):
		node = Node(I, None, None)
		nodes.append(node)
	for J in range(7, -1, -1):
		x = randint(0, J)
		node = Node(choice(ops) if nodes[x].canConcat and nodes[x+1].canConcat else choice(ops2), nodes[x], nodes[x+1])
		#node = Node(choice(ops), nodes[x], nodes[x + 1])
		del nodes[x:x+2]
		nodes.insert(x, node)
	exp = nodes[0]
	try:
		return exp, exp.calc()
	except Exception as e:
		return None, 0


def oneProc(id, bestValues, isFound):
	target = 10958
	closest = -999999999999
	closestExp = None
	lastClosest = None
	I = 0
	while True:
		if 'found' in isFound:
			break
		exp, val = randomCalc()
		if abs(val-target)<abs(closest-target):
			closest = val
			closestExp = exp
			bestValues[id] = (val, exp)
			if val-target == 0:
				isFound['found'] = True
				print('Found')
				print(bestValues)
				print(val, exp)
		if I % 7000 == 0:
			if str(closestExp) != lastClosest:
				#print(closest, closestExp)
				print(bestValues)
			lastClosest = str(closestExp)
		I = I + 1
	#print(closest, closestExp)

from multiprocessing import Pool, Manager

bestValues = [0,0,0,0,0,0,0,0,0] #
#for J in range(0,8):
#	bestValues.append(None)
#oneProc(0)

if __name__ == '__main__':
	with Manager() as manager:
		managedBestValues = manager.list(bestValues)
		isFound = manager.dict()
		p = Pool(7)
		for J in range(0, 6):
			bestValues.append(0)
			p.apply_async(oneProc, (J, managedBestValues, isFound ))
		p.close()
		p.join()

# ((1+2^3)*(4/5))^6*(7/89) => 10957.286
#(10958.668514806757, *(*(1,*(^(+(2,3),/(4,5)),*(6,7))),*(8,9)))
# 10958.286365483147, (1+((((2+(3c4))/5)^6)*(7/(8c9))))
#(10958.3317287401, (((1*((2^3)+4))/5)^(((6+7)/8)+9)))
#10958.286365483147, 1+((2+34)/5)^6*7/89
#10958.286365483147, 1+ (2^3-4/5)^6*7/89
#10957.732771865078, (((1^2)-3)+((4^(5-((6-7)/8)))*9)))