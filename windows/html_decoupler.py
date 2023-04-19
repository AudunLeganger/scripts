from sys import argv

def main():
    html_file_path = argv[1]

    try:
        html_read_file = open(html_file_path, "r")
       
    except IOError:
        print("Error: Source HTML does not exist.")
        exit(1)
    
    html_lines = html_read_file.readlines()
    html_read_file.close()

    ordered_file_data = identify_file_types(argv)
    style_data = ordered_file_data[0]
    js_data = ordered_file_data[1]

    if style_data[0] == False and js_data[0] == False:
        exit(0)
    
    if style_data[0] == True:
        css_file_path  = argv[style_data[1]]
        style_indexes, style_lines = find_style_lines(html_lines)
        relative_css_path = "./" + css_file_path.split("/")[-1]
        start_index = style_indexes[0]
        end_index = style_indexes[1]
        if write_to_css(css_file_path, style_lines):
            html_lines = remove_style_from_html(html_file_path, html_lines, relative_css_path, start_index, end_index)

    if js_data[0] == True:
        js_file_path = argv[js_data[1]]
        script_indexes, script_lines = find_script_lines(html_lines)
        relative_js_path = "./" + js_file_path.split("/")[-1]
        start_index = script_indexes[0]
        end_index = script_indexes[1]
        if write_to_js(js_file_path, script_lines):
            html_lines = remove_script_from_html(html_file_path, html_lines, relative_js_path, start_index, end_index)
    
    

'''
Identifies which runtime arguments are provided, and their corresponding index:

returns: [whether or not css is contained (true/false), css file index], [whether or not javascript is contained (true/false), javascript file index]
'''
def identify_file_types(argv):
    css_index = None
    has_css = False
    js_index = None
    has_js = False
    for index, file_name in enumerate(argv):
        if file_name.split(".")[-1] == "css":
            has_css = True
            css_index = index
        if file_name.split(".")[-1] == "js":
            has_js = True
            js_index = index
    return [has_css, css_index], [has_js, js_index]

'''
Identifies the lines in the html that contain style data. Returns a list for indexes [start_index, end_index], as well as a list containing the lines
'''
def find_style_lines(html_lines):
    start_index = None
    end_index = None
    for line_num, line in enumerate(html_lines):
        if "<style>" in line:
            start_index = line_num
        elif "</style>" in line and start_index:
            end_index = line_num
            return [start_index, end_index], html_lines[(start_index+1):end_index]
    return [None, None], None

'''
Identifies the lines in the html that contain script data. Returns a list for indexes [start_index, end_index], as well as a list containing the lines
'''
def find_script_lines(html_lines):
    start_index = None
    end_index = None
    for line_num, line in enumerate(html_lines):
        if "<script>" in line:
            start_index = line_num
        elif "</script>" in line and start_index:
            end_index = line_num
            return [start_index, end_index], html_lines[(start_index+1):end_index]
    return [None, None], None

'''
Tries to write to the .css file. Returns True if operation is successfull, False in the event of TypeError
'''
def write_to_css(css_file_path, style_lines):
    try:
        with open(css_file_path, "w") as css_file:
            css_file.writelines(style_lines)
            return True
    except TypeError:
        return False

'''
Tries to write to the .js file. Returns True if operation is successfull, False in the event of TypeError
'''
def write_to_js(js_file_path, script_lines):
    try:
        with open(js_file_path, "w") as js_file:
            js_file.writelines(script_lines)
            return True
    except TypeError:
        return False

'''
Removes styling lines from the html. Returns list containing file lines without styling lines
'''
def remove_style_from_html(html_file_path, html_lines, relative_css_path, start_index, end_index):
    html_write_file = open(html_file_path, "w")
    try:
        html_start_lines = html_lines[0:start_index]
        html_end_lines = html_lines[end_index+1:]
        replaced_html_lines = html_start_lines + html_end_lines
        end_of_head_line_index = get_end_of_head_line(replaced_html_lines)
        replaced_html_lines.insert(end_of_head_line_index, '    <link rel="stylesheet" href="{css_path}" />\n'.format(css_path = relative_css_path))
        html_write_file.writelines(replaced_html_lines)
    finally:
        html_write_file.close()
    return replaced_html_lines
    

'''
Removes script lines from the html. Returns list containing file lines without styling lines
'''
def remove_script_from_html(html_file_path, html_lines, relative_js_path, start_index, end_index):
    html_write_file = open(html_file_path, "w")
    try:
        html_start_lines = html_lines[0:start_index]
        html_end_lines = html_lines[end_index+1:]
        replaced_html_lines = html_start_lines + html_end_lines
        end_of_head_line_index = get_end_of_head_line(replaced_html_lines)
        replaced_html_lines.insert(end_of_head_line_index, '    <script src="{js_path}" defer></script>\n'.format(js_path = relative_js_path))
        html_write_file.writelines(replaced_html_lines)
    finally:
        html_write_file.close()
    return replaced_html_lines

'''
Identifies the line index of the </head> element, so that elements can be placed just before it
'''
def get_end_of_head_line(html_lines):
    for index, line in enumerate(html_lines):
        if "</head>" in line:
            return index
    raise IndexError

if __name__ == "__main__":
    main()