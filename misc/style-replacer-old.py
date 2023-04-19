from sys import argv

def main():
    html_file_path = argv[1]
    css_file_path = argv[2]
    js_file_path = argv[3]

    try:
        html_file = open(html_file_path, "r")
       
    except IOError:
        print("Error: Source HTML does not exist.")
        exit(1)
    
    html_lines = html_file.readlines()
    html_file.close()

    style_indexes, style_lines = find_style_lines(html_lines)
    if not style_indexes[0]:
        quit(0)
    
    start_index = style_indexes[0]
    end_index = style_indexes[1]
    relative_css_path = "./" + css_file_path.split("/")[-1]
    write_to_css(css_file_path, style_lines)
    update_html(html_file_path, relative_css_path, html_lines, start_index, end_index)

def identify_file_types(argv):
    css_index = None
    has_css = False
    js_index = None
    has_js = False
    for index, file_name in enumerate(argv):
        if file_name.split()[-1] == "css":
            has_css = True
            css_index = index
        if file_name.split()[-1] == "js":
            has_js = True
            js_index = index
    
    return [has_css, css_index], [has_js, js_index]

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

def write_to_css(css_file_path, style_lines):
    with open(css_file_path, "w") as css_file:
        css_file.writelines(style_lines)

def write_to_js(js_file_path, script_lines):
    with open(js_file_path, "w") as js_file:
        js_file.writelines(script_lines)

def update_html(html_file_path, relative_css_path, html_lines, start_index, end_index):
    html_head = html_lines[0:start_index]
    html_tail = html_lines[end_index+1:]
    with open(html_file_path, "w") as html_file:
        html_file.writelines(html_head)
        html_file.write('<link rel="stylesheet" href="' + relative_css_path + '" />\n')
        html_file.writelines(html_tail)
    if len(argv == 3):
        html_file.w
    

if __name__ == "__main__":
    main()