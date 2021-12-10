import ast, sys, pickle, os, collections

#This class hunts for functions in an AST, then performs ast.walk on function's subtree
#This resolves bug where function names get inserted into other functions, since breadth-first swaps between incomplete functions
class TypeInstrumenter(ast.NodeVisitor):
    curr_params = []
    exit_num = 0
    func_name = ""

    #Find each function node in ast
    def visit(self, node):
        #print(type(node).__name__, ast.unparse(node))
        if isinstance(node, ast.FunctionDef):
            self.return_hunting(node)     
        ast.NodeVisitor.generic_visit(self, node)

    #For given function node, hunt for returns in its subtree
    def return_hunting(self, node):
        #same variables as before ***
        self.curr_params = []
        self.exit_num = 0
        self.func_name = node.name

        #collect function's parameters, place dictionary key initializers
        for param in node.args.args:
            self.curr_params.append(param)
            plant_dict_entry = ast.parse("d[\""+self.func_name+"():::ENTER\"][\""+param.arg+"\"]=type_prep("+param.arg+")")
            node.body.insert(0, plant_dict_entry)
        plant_dict = ast.parse("if d.get(\""+self.func_name+"():::ENTER\") is None: d[\""+self.func_name+"():::ENTER\"] = {}")
        node.body.insert(0, plant_dict)

        #Now walk the function's subtree, for each node contianing a return we will plant exit point dictionary calls
        for n in ast.walk(node):
            if ((hasattr(n, 'body') and not isinstance(n, ast.FunctionDef)) or (isinstance(n, ast.FunctionDef) and n is node)) and isinstance(n.body[-1], ast.Return):
                plant_dict = ast.parse("if d.get(\""+self.func_name+"():::EXIT"+str(self.exit_num)+"\") is None: d[\""+self.func_name+"():::EXIT"+str(self.exit_num)+"\"] = {}")
                return_string = (ast.unparse(n.body[-1]))[7:]
                n.body.insert(-1, plant_dict)
            
                for param in self.curr_params:
                    plant_dict_exit = ast.parse("d[\""+self.func_name+"():::EXIT"+str(self.exit_num)+"\"][\""+param.arg+"\"]=type_prep("+param.arg+")")
                    n.body.insert(-1, plant_dict_exit)
                #Return exit_num
                n.body.insert(-1, ast.parse("exit_" + str(self.exit_num) + " = " + return_string))
                n.body.insert(-1, ast.parse("d[\""+self.func_name+"():::EXIT"+str(self.exit_num)+"\"][\"exit_"+str(self.exit_num)+"\"]=type_prep(exit_"+str(self.exit_num)+")"))
                n.body[-1] = ast.parse("return exit_"+str(self.exit_num))
                self.exit_num += 1


#Captures traces of execution from given driver
#Here each critical point is allowed to hold more than 1 trace
#An entry in the dictionary will instead by a given critical point that maps to all values that went through point along with their type information
class ValueInstrumenter(ast.NodeVisitor):
    
    curr_params = []
    exit_num = 0
    func_name = ""

    #Find each function node in ast
    def visit(self, node):
        #print(type(node).__name__, ast.unparse(node))
        if isinstance(node, ast.FunctionDef):
            self.return_hunting(node)     
        ast.NodeVisitor.generic_visit(self, node)

    #For given function node, hunt for returns in its subtree
    def return_hunting(self, node):
        #same variables as before ***
        self.curr_params = []
        self.exit_num = 0
        self.func_name = node.name
        #collect function's parameters, place dictionary key initializers
        for param in node.args.args:
            self.curr_params.append("\""+param.arg+"\":val_prep("+param.arg+")")

        parameter_string = ",".join(self.curr_params)

        plant_dict = ast.parse("if v.get(\""+self.func_name+"()\") is None: v[\""+self.func_name+"()\"] = []")
        node.body.insert(0, plant_dict)

        assignment_string = "curr_entry = {"+parameter_string+"}"
        entry_node = ast.parse(assignment_string)
        node.body.insert(0, entry_node)


        for n in ast.walk(node):
            if ((hasattr(n, 'body') and not isinstance(n, ast.FunctionDef)) or (isinstance(n, ast.FunctionDef) and n is node)) and isinstance(n.body[-1], ast.Return):
                return_string = (ast.unparse(n.body[-1]))[7:]
                return_placeholdr = "exit_" + str(self.exit_num)
                n.body.insert(-1, ast.parse(return_placeholdr + " = " + return_string))
                curr_exit_string = ""
                if (len(parameter_string) > 0):
                    curr_exit_string = "curr_exit = [{"+parameter_string+",\""+return_placeholdr+"\":val_prep("+return_placeholdr+")},{\"EXIT\":"+str(self.exit_num)+"}]"
                else:
                    curr_exit_string = "curr_exit = [{\""+return_placeholdr+"\":val_prep("+return_placeholdr+")}, {\"EXIT\":"+str(self.exit_num)+"}]"

                n.body.insert(-1, ast.parse(curr_exit_string))

                plant_append = ast.parse("v[\""+self.func_name+"()\"].append([curr_entry, curr_exit])")

                n.body.insert(-1, ast.parse(plant_append))

                n.body[-1] = ast.parse("return exit_"+str(self.exit_num))
                self.exit_num += 1


# THE FIRST RUN
# OBJECTIVE: instrument code and execute it to gather type information needed to satisfy Daikon requirements
# INPUTS: target_file : source code that you want to instrument
#
# PROCESS: 
#       1. Open target_file and convert code as Abstract Syntax Tree
#       2. Use UntypedTraverser to traverse tree and capture all critical entry and exit points
#                   - at each point, create database entry
#                   - dictionary assignments will be added as new AST nodes, thus modifying the original AST
#                   - for entry points, include any parameter's types into database entry.
#                   - for exit points, include all parameter types AND return type
#       3. Unparse modified AST
#       4. Execute the instrumented code
#       5. This execution will build our database of types belonging to variables of interest
#  
# OUTPUTS:  pickle_types - the pickle file that consolidates the database and will be unloaded on second run
#           type_instr.py - the resulting instrumentation after completing step 2
def first_run(target_file):
    print("First Run!")
    instrumented_untyped_filename = "instrumented/type_instr.py"
    #Open and store target python file's contents
    code = ""
    with open(target_file) as source:
         code = source.read()

    #Converts target's source code into a Abstract Syntax Tree
    tree = ast.parse(code)

    #ast walk traverse the ENTIRE parsed tree (solves inner classes and defs issue)
    c = TypeInstrumenter()
    c.generic_visit(tree)

    #Leaving it as a list if we needed to add anything else
    import_list = ["import pickle"]
    #adds dictionary initializaiton line to front of ast.Module's body

    prepper_functions = ""
    with open("front_end_helpers/prepper.py") as source:
        prepper_functions = source.read()

    tree.body.insert(0, ast.parse(prepper_functions))

    tree.body.insert(0, ast.parse("d = {}"))

    #adds any lambda and import statements to front of ast.Module's body
    for i in import_list:
        tree.body.insert(0, ast.parse(i))
           
    #Here needs to be case for using either standalone or test suite
    #If there is an if __name___ main driver, node should be last in Module's body
    executable = ""
    if isinstance(tree.body[-1], ast.If):
        print("Driver Located")
        executable = instrumented_untyped_filename
        #if __name__ should be at the end of standalone script
        tree.body[-1].body.append(ast.parse("pickle_types = open(\"pickled_files/pickled_types\", \"wb\")"))
        tree.body[-1].body.append(ast.parse("pickle.dump(d, pickle_types)"))
        tree.body[-1].body.append(ast.parse("pickle_types.close()"))
    else:
        print("Invalid: double check if your program needs a test suite")

    #modified ast morphs into instrumented source code
    result = ast.unparse(tree)
    with open(instrumented_untyped_filename, "w") as output:
        output.writelines(result)

    #Run instrumented code!
    os.system("python " + executable)

# THE SECOND RUN
# OBJECTIVE: re-instrument code and execute it to collect values and types from test driver
# INPUTS: target_file : source code that you want to instrument
#       pickled_types : the pickled database of type information from first run
#
# PROCESS: 
#       1. Unload the pickled_types ===> unlocks the dictionary (variable is type_data)
#       2. Using type_data, construct the .decls file
#                   - while looking, need to encode lists as arrays
#       3. Using TypedTraverser, instrument code that will capture ALL runtime traces from driver
#       4. Construct .dtrace file
#  
# OUTPUTS:  .decls and .dtrace files that Daikon will consume and generate invariants off of
def second_run(target_file):
    print("Second Run!")

    typed_instrumented_file = "instrumented/value_instr.py"

    type_data = load_my_dictionary("pickled_files/pickled_types")
    type_data = collections.OrderedDict(sorted(type_data.items()))

    #Generate .decls file
    print("Generating declarations file....")
    decls = open(target_file + ".decls", "w")
    curr_method = ""
    for tuple in type_data.items():

        #Check if new programming point set
        new_method = tuple[0].split(":")[0]
        if (curr_method == ""):
            curr_method = new_method
        elif (curr_method != new_method):
            decls.write("\n\n")
            curr_method = new_method
        else:
            decls.write("\n")

        decls.write("DECLARE\n")
        decls.write("a."+tuple[0] + "\n")
        for item in tuple[1]:
            if ((type_data[tuple[0]][item])[-2:] == "[]"):
                decls.write(""+item+"[]\n")
                decls.write(type_data[tuple[0]][item] + "\n")
                decls.write(type_data[tuple[0]][item] + "\n")
                decls.write("1[1]\n")
            else:
                decls.write(""+item+"\n")
                decls.write(type_data[tuple[0]][item] + "\n")
                decls.write(type_data[tuple[0]][item] + "\n")
                decls.write("1\n")
    decls.write("\n")
    decls.close()

    #Open and store target python file's contents
    code = ""
    with open(target_file) as source:
         code = source.read()

    #Converts target's source code into a Abstract Syntax Tree
    tree = ast.parse(code)
    #traverse code, construct trace entries
    c = ValueInstrumenter()
    c.visit(tree)

    prepper_functions = ""
    with open("front_end_helpers/prepper.py") as source:
        prepper_functions = source.read()
    tree.body.insert(0, ast.parse(prepper_functions))

    tree.body.insert(0, ast.parse("v = {}"))
    tree.body.insert(0, ast.parse("import pickle"))


    executable = ""
    if isinstance(tree.body[-1], ast.If):
        executable = typed_instrumented_file
        #if __name__ should be at the end of standalone script
        tree.body[-1].body.append(ast.parse("pickle_values = open(\"pickled_files/pickled_values\", \"wb\")"))
        tree.body[-1].body.append(ast.parse("pickle.dump(v, pickle_values)"))
        tree.body[-1].body.append(ast.parse("pickle_values.close()"))
    else:
        print("Invalid: double check if your program needs a test suite")

    #modified ast morphs into instrumented source code
    result = ast.unparse(tree)
    with open(typed_instrumented_file, "w") as output:
        output.writelines(result)

    #Run instrumented code!
    os.system("python " + executable)

    #Locate pickle_values
    print("Generating data traces from test driver")
    val_db = load_my_dictionary("pickled_files/pickled_values")
    dtrace = open(target_file + ".dtrace", "w")
    for point in val_db:
        for value_dict in val_db[point]:
            dtrace.write("a."+point+":::ENTER\n")
            for value_key in value_dict[0]:
                if ((type_data[point+":::ENTER"][value_key])[-2:] == "[]"):
                    dtrace.write(""+value_key+"[]\n")
                    dtrace.write(str(value_dict[0][value_key]) + "\n")
                    dtrace.write("1\n")
                else:                 
                    dtrace.write(""+value_key+"\n")
                    dtrace.write(str(value_dict[0][value_key]) + "\n")
                    dtrace.write("1\n")
            dtrace.write("\n")
            dtrace.write("a."+point+":::EXIT"+str(value_dict[1][1].get("EXIT"))+"\n")
            id = value_dict[1][1].get("EXIT")
            for value_key in value_dict[1][0]:
                if ((type_data[point+":::EXIT"+str(id)][value_key])[-2:] == "[]"):
                    dtrace.write(""+value_key+"[]\n")
                    dtrace.write(str(value_dict[1][0][value_key]) + "\n")
                    dtrace.write("1\n")
                else:                 
                    dtrace.write(""+value_key+"\n")
                    dtrace.write(str(value_dict[1][0][value_key]) + "\n")
                    dtrace.write("1\n")
            dtrace.write("\n")
    dtrace.write("\n")
    dtrace.close()
    
#Used in second run, unpacks pickle file and returns type database for use in re-instrumentation
def load_my_dictionary(pickled_file:str):
    dbfile = open(pickled_file, 'rb')
    db = pickle.load(dbfile)
    dbfile.close()
    return db

#Driver Code
if __name__ == "__main__":
    print(sys.argv)
    #First Run - Instrument for Types, then run instrumented code
    if (len(sys.argv) == 2):
        os.makedirs("pickled_files", exist_ok=True)
        os.makedirs("instrumented", exist_ok=True)
        first_run(sys.argv[1])
    #Second Run - Re-instrument for Values, run re-instrumented code, generate .dtrace and .decls
    elif (len(sys.argv) == 3 and sys.argv[1] == "--T"):
        if os.path.isfile("./pickled_files/pickled_types") and os.path.isfile("./instrumented/type_instr.py"):
            second_run(sys.argv[2])
        else:
            print("Missing either type data or instrumented code; or you didn't run first step")
    else:
        print("INVALID")