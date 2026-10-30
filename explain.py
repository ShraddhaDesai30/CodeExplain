import ast, re

def explain_code(code):
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return {"summary":"Python syntax error: " + e.msg, "details":[f"Check line {e.lineno}."],
                "functions":[],"classes":[],"imports":[],"complexity":None}
    imports, functions, classes, details = [], [], [], []
    for n in ast.walk(tree):
        if isinstance(n, ast.Import):
            imports += [a.name for a in n.names]
        elif isinstance(n, ast.ImportFrom):
            imports.append(n.module or "")
        elif isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions.append({"name":n.name,"args":[a.arg for a in n.args.args],
                              "line":n.lineno,"docstring":ast.get_docstring(n) or "No docstring provided."})
        elif isinstance(n, ast.ClassDef):
            classes.append({"name":n.name,"line":n.lineno,
                "methods":[x.name for x in n.body if isinstance(x,(ast.FunctionDef,ast.AsyncFunctionDef))]})
    for i, line in enumerate(code.splitlines(), 1):
        s=line.strip()
        if not s or s.startswith("#"): continue
        if re.match(r"(async )?def ",s):
            details.append(f"Line {i}: defines a function named '{s.split('def ',1)[1].split('(',1)[0]}'.")
        elif s.startswith("class "):
            details.append(f"Line {i}: defines a class named '{s.split('class ',1)[1].split(':',1)[0].split('(',1)[0]}'.")
        elif s.startswith(("if ","elif ")):
            details.append(f"Line {i}: checks a condition and selects a branch.")
        elif s.startswith(("for ","while ")):
            details.append(f"Line {i}: repeats instructions using a loop.")
        elif s.startswith("return"):
            details.append(f"Line {i}: returns a value from the current function.")
        elif re.match(r"^[\w.]+\s*=(?!=)",s):
            details.append(f"Line {i}: assigns a value to '{s.split('=',1)[0].strip()}'.")
    decisions=sum(isinstance(n,(ast.If,ast.For,ast.While,ast.IfExp,ast.Try)) for n in ast.walk(tree))
    parts=[]
    if classes: parts.append(f"{len(classes)} class(es)")
    if functions: parts.append(f"{len(functions)} function(s)")
    if imports: parts.append(f"{len(set(imports))} imported module(s)")
    summary="This Python program contains "+(", ".join(parts) if parts else "executable statements")+"."
    if decisions: summary+=f" It contains approximately {decisions} decision/loop construct(s)."
    return {"summary":summary,"details":details,"functions":functions,"classes":classes,
            "imports":sorted(set(x for x in imports if x)),"complexity":1+decisions}
