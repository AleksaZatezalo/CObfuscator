import re
import random
import string

class CObfuscator:
    def __init__(self):
        self.variable_map = {}
        self.function_map = {}
        self.macros = []
        
    def generate_random_name(self, length=8):
        """Generate confusing variable names that look similar."""
        chars = 'OoIlL1' + string.ascii_letters
        return '_' + ''.join(random.choice(chars) for _ in range(length))
    
    def obfuscate_variables(self, code):
        """Find and replace all variable declarations with obfuscated names."""
        pattern = r'\b(?:int|char|float|double|long)\s+([a-zA-Z_][a-zA-Z0-9_]*)'
        declarations = re.finditer(pattern, code)
        
        for match in declarations:
            var_name = match.group(1)
            if var_name != 'main' and var_name not in self.variable_map:
                self.variable_map[var_name] = self.generate_random_name()
                
        for original, obfuscated in self.variable_map.items():
            code = re.sub(r'\b' + original + r'\b', obfuscated, code)
            
        return code
    
    def obfuscate_functions(self, code):
        """Find and replace all function declarations with obfuscated names."""
        pattern = r'\b(?:void|int|char|float|double|long)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\('
        functions = re.finditer(pattern, code)
        
        for match in functions:
            func_name = match.group(1)
            if func_name != 'main' and func_name not in self.function_map:
                self.function_map[func_name] = self.generate_random_name()
                
        for original, obfuscated in self.function_map.items():
            code = re.sub(r'\b' + original + r'\b', obfuscated, code)
            
        return code
    
    def add_junk_macros(self, code):
        """Add confusing macros at the top of the code."""
        junk_macros = [
            '#define ' + self.generate_random_name() + '(x) ((x))',
            '#define ' + self.generate_random_name() + ' 1',
            '#define ' + self.generate_random_name() + '(x,y) ((x)+(y))'
        ]
        return '\n'.join(junk_macros) + '\n\n' + code
    
    def add_junk_functions(self, code):
        """Add meaningless function declarations and calls to obscure the code."""
        # Generate some random junk functions
        junk_functions = []
        
        # Simple void functions with basic operations
        basic_operations = [
            "int {var1} = 0; {var1} += 1;",
            "{var1} = {var1} & 0xFF;",
            "int {var1} = 1; {var1} = {var1} << 2;",
            "int {var1} = 100; {var1} = {var1} >> 1;",
            "int {var1} = 1; {var1} = ~{var1};",
            "int {var1} = 42; {var1} = {var1} | 0x0F;",
        ]
        
        # Generate 3-5 random functions
        num_functions = random.randint(3, 5)
        for _ in range(num_functions):
            # Generate random variable names
            var1 = self.generate_random_name()
            var2 = self.generate_random_name()
            
            # Pick a random operation
            operation = random.choice(basic_operations).format(var1=var1, var2=var2)
            
            # Create function with random name
            func_name = self.generate_random_name()
            junk_function = f"""
    void {func_name}() {{
        if(1) {{
            {operation}
        }}
    }}
    """
            junk_functions.append(junk_function)

        # Add all junk functions at the beginning of the code
        return '\n'.join(junk_functions) + '\n' + code


    def split_lines(self, code):
        """Randomly split lines to make code harder to read."""
        lines = code.split('\n')
        result = []
        for line in lines:
            if len(line.strip()) > 0 and ';' in line:
                parts = line.split(';')
                for part in parts[:-1]:
                    if part.strip():
                        result.append(part.strip() + ';')
            else:
                result.append(line)
        return '\n'.join(result)
    
    def obfuscate(self, code):
        """Apply all obfuscation techniques to the input code."""
        result = code
        result = self.obfuscate_variables(result)
        result = self.obfuscate_functions(result)
        result = self.add_junk_macros(result)
        result = self.add_junk_functions(result)
        result = self.split_lines(result)
        result = self.format_c_code(result)
        return result
        
    def format_c_code(self, code):
        """Format C code with proper indentation and spacing."""
        lines = code.split('\n')
        includes = []
        macros = []
        code_lines = []

        for line in lines:
            parts = line.strip().split(' #')
            for part in parts:
                if part:
                    if part.startswith('include'):
                        # Remove spaces between <>, remove leading spaces, and add carriage return after >
                        fixed_include = re.sub(r'\s*#?\s*include\s*<\s*([a-zA-Z0-9.]+)\s*>', r'#include<\1>\n', part)
                        includes.append(fixed_include.strip())
                    elif part.startswith('define'):
                        macros.append(f'#{part.strip()}')
                    else:
                        code_lines.append(part)

        indent_level = 0
        formatted_code = []

        for line in code_lines:
            stripped = line.strip()
            if not stripped:
                continue

            if stripped.startswith('}'):
                indent_level = max(0, indent_level - 1)

            formatted_code.append('    ' * indent_level + stripped)

            if stripped.endswith('{'):
                indent_level += 1

            if stripped.endswith('}') and not stripped.startswith('}'):
                indent_level = max(0, indent_level - 1)

        result = []

        if includes:
            result.extend(includes)

        if macros:
            result.extend(macros)
            result.append('')  # Empty line after macros

        result.extend(formatted_code)
        final_code = '\n'.join(result)
        final_code = re.sub(r',(?=\S)', ', ', final_code)
        final_code = re.sub(r'\s*([=+\-*/<>])\s*', r' \1 ', final_code)
        final_code = re.sub(r'#include\s*<\s*([^>\s]+)\s*>', r'#include<\1>\n', final_code)
        final_code = re.sub(r'^\s*(#)', r'\1', final_code, flags=re.MULTILINE)

        return final_code



        
    def obfuscate(self, code):
        """Apply all obfuscation techniques to the input code."""
        result = code
        result = self.obfuscate_variables(result)
        result = self.obfuscate_functions(result)
        result = self.add_junk_macros(result)
        result = self.split_lines(result)
        # Format the final code
        result = self.format_c_code(result)
        return result