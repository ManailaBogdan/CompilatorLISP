from sys import argv
from src.Lexer import Lexer



	


def concat(list):
	spec = [
			("list_of_lists", "\( ([0-9]+ | \ | \( | \) )+ \)"),
			("concat", "\+\+"),\
			("space", "\ +"),
		 
		   ]
	
	lexer = Lexer(spec)
	rez = lexer.lex(list)
	for (x, y) in rez:
		if x == "list_of_lists":
			rez = y
			break


	spec = [
			("atom", "[0-9]+"),
			("space", "\ +"),
		 	("list_of_lists", "\( ([0-9]+ | \ | ( \( ([0-9]+ | \ )* \) ) )+ \)"),
			 ("vida", "\(\)"),
			 ("close", "\)"),
		   ]
	
	lexer = Lexer(spec)
	rez = lexer.lex(rez[1:-1])
	

	fin = "( "

	for (x, y) in rez:
		if x == "atom":
			fin += y + " "
		elif x == "list_of_lists":
			fin += y[1:-1] + " "

	return fin + ")"

def sum(list):
	spec = [
			("list_of_lists", "\( ([0-9]+ | \ | \( | \) )+ \)"),
			("sum", "\+"),
			("space", "\ +"),
		 
		   ]
	
	lexer = Lexer(spec)
	rez = lexer.lex(list)
	for (x, y) in rez:
		if x == "list_of_lists":
			rez = y
			break

	

	spec = [
			("atom", "[0-9]+"),
			("space", "\ +"),
		 	("list_of_lists", "\( ([0-9]+ | \ | ( \( ([0-9]+ | \ )* \) ) )+ \)"),
			 ("vida", "\(\)"),
		   ]
	
	lexer = Lexer(spec)
	rez = lexer.lex(rez[1:-1])

	

	suma = 0

	while len(rez) >= 1:
		(x, y) = rez[0]
		if x == "atom":
			suma += int(y)
		elif x == "list_of_lists":
			rez += lexer.lex(y[1:-1])

		rez = rez[1:]

	return suma

def lambda_function(tokens):

	lambda_expr = tokens[0][1]
	tokens = tokens[1:]

	spec = [
			("lambda", "lambda"),
			("space", "\ +"),
			("id", "([a-z] | [A-Z])+"),
			("join", ":"),
	]

	lexer = Lexer(spec)

	rez = lexer.lex(lambda_expr)

	ids = []
	variables = []
	d = {}
	for (x, y) in rez:
		if x == "id":
				ids.append(y)
	

	tokens = [(x, y) for (x, y) in tokens if x != "space" and x != "close"]

	
	ok = True
	expresion = ""
	w = ""
	for (x, y) in tokens:
		if (x == "id" or x == "id_list") and ok:
			expresion  = y
			ok = False
		elif x == "atom":
			if w != "":
				variables.append(w)
				w = ""
			variables.append(y)
		elif x == "list_of_lists":
			if w != "":
				variables.append(w)
				w = ""
			v = ""
			ct = 0
			for i in range(len(y)):
				if y[i] == '(':
					ct += 1
				elif y[i] == ')':
					ct -= 1
				if ct < 0:
					ct = 0
					variables.append(v)
					v = ""
				else:
					v += y[i]
		elif x == "lambda":
			if w != "":
				variables.append(w)
				w = ""
			w += y
		else:
			w += y
		
	if w != "":
		variables.append(w)

	
				
	
	for i in range(len(ids)):
		d[ids[i]] = variables[0]
		variables = variables[1:]


	
	

	spec = [
		("open", "\("),
		("close", "\)"),
		("id", "([a-z] | [A-Z])+"),
		("space", "\ +"),
		("plus", "\+"),
	]

	lexer = Lexer(spec)
	tokens = lexer.lex(expresion)

	rez = ""
	for (x, y) in tokens:
		if x == "id":
			rez += d[y]
		else:
			rez += y

	for x in variables:
		rez += " " + x + ")"

	

	return rez


	pass

def main():
	if len(argv) != 2:
		return
	
	filename = argv[1]
	# TODO implementarea interpretor L (bonus)

	
	spec = [
		 ("vida", "\(\)"), 
		 ("space", "\ +"), 
		 ("atom", "[0-9]+"), 
		 ("atom_list", "\( ([0-9]+ | \ )+ \)"),
		 ("list_of_lists", "\( ([0-9]+ | \ | \( | \) )+ \)"),
		 ("concat", "\( \ * \+\+ \ + \( ([0-9]+ | \ | \( | \) )+ \)"),
		 ("sum", "\( \ * \+ \ + \( ([0-9]+ | \ | \( | \) )+ \)"),
		 ("lambda", "(lambda \ + ([a-z] | [A-Z])+ : \ *)+"),
		 ("open", "\("),
		("close", "\)"),
		("join", ":"),
		("id", "([a-z] | [A-Z])+"),
		("id_list", "\( ([a-z] | [A-Z] | \ | \+ | \( | \)  )+ \)"),
		("plus", "\+"),
		("plusplus", "\+\+")
		
		   ]
	

	lexer = Lexer(spec)


	expresion = ""

	with open(filename, 'r') as f:
		# TODO citirea din fisier
		content = f.read()
		content = content.replace("\n", " ")
		content = content.replace("\t", " ")
		expresion += content
		pass

	

	rez = lexer.lex(expresion)
	aux = [(x, y) for (x, y) in rez if x == "plus" or x == "plusplus"]
	
	tokens = [(x, y) for (x, y) in rez if x != "space" and x != "open" and x != "plus" and x != "plusplus"]

	
	
	
	while True:
		rez = tokens[0]
		

		if rez[0] == "atom":
			rez = rez[1]
			break
		elif rez[0] == "atom_list":
			rez = rez[1]
			break
		elif rez[0] == "list_of_lists":
			rez = rez[1]
			break
		elif rez[0] == "concat":
			rez = concat(rez[1][1:-1])
		elif rez[0] == "sum":
			rez = str(sum(rez[1][1:-1]))
		elif rez[0] == "lambda":
			rez = lambda_function(tokens)

		new = ""
		if aux != []:
			ct = 0
			for (x, y) in aux:
				new += "( "
				new += y + " "
				ct += 1
			new += rez + " "
			for i in range(ct):
				new += ") "
			rez = new

		
		
		tokens = lexer.lex(rez)
		aux = [(x, y) for (x, y) in tokens if x == "plus" or x == "plusplus"]
		tokens = [(x, y) for (x, y) in tokens if x != "space" and x != "open" and x != "plus" and x != "plusplus"]
		

	

	


	fin = ""
	for i in range(len(rez)):
		if rez[i] != ' ':
			if i != len(rez) - 1:
				if rez[i] == '(' and rez[i + 1] == ')':
					fin += rez[i]
				elif rez[i] == '(':
					fin += rez[i] + " "
				elif rez[i+1] == ' ' or rez[i+1] == ')':
					fin += rez[i] + ' '
				else:
					fin += rez[i]
			else:
				fin += rez[i]

	
	print(fin)
	




	

if __name__ == '__main__':
    main()
