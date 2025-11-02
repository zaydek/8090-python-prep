import colorful as cf

# Basic colors
print("=== Basic Colors ===")
print(cf.red("This is red"))
print(cf.green("This is green"))
print(cf.blue("This is blue"))
print(cf.yellow("This is yellow"))

# Text styles
print("\n=== Text Styles ===")
print(cf.bold("This is bold"))
print(cf.italic("This is italic"))
print(cf.underline("This is underlined"))

# Combining styles (using & operator)
print("\n=== Combined Styles ===")
print(cf.bold & cf.red("Bold and red!"))
print(cf.italic & cf.green("Italic and green!"))
print(cf.bold & cf.blue("Bold and blue!"))

# Grayscale colors
print("\n=== Grayscale ===")
print(cf.gray("This is gray"))
print(cf.black("This is black"))
print(cf.white("This is white"))

# Dimmed (faint) text
print("\n=== Dimmed Text ===")
print(cf.dimmed("This is dimmed"))
print(cf.dimmed & cf.red("Dimmed red"))

# Using variables to store styles
print("\n=== Style Variables ===")
error = cf.bold & cf.red
success = cf.bold & cf.green
warning = cf.bold & cf.yellow

print(error("Error: Something went wrong!"))
print(success("Success: Everything is working!"))
print(warning("Warning: Be careful!"))

# Mixing with regular text
print("\n=== Mixing Colors ===")
print(f"Regular text {cf.red('red text')} more regular text")
print(f"{cf.bold('Bold')} and {cf.italic('italic')} in the same line")
