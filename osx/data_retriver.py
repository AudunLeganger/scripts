from sys import argv
import requests

def main():
    f_name = argv[1]
    url = argv[2]
    response = requests.get(url)
    response.close()
    response_text = response.text
    nonempty = len(response_text) > 0

    has_styling, has_scripting = check_style_script(response_text)
    function_string = make_function_string(f_name, has_styling, has_scripting)
    write_to_file(f"{f_name}.html", response_text)
    print(function_string, end="")


def check_style_script(response_text):
    has_styling = False
    has_scripting = False
    if "<style>" in response_text and "</style>" in response_text:
        has_styling = True
    if "<script>" in response_text and "</script>" in response_text:
        has_scripting = True
    return has_styling, has_scripting


def write_to_file(f_name, response_text):
    with open(f_name, "w") as f:
        f.write(response_text)


def make_function_string(f_name, has_styling, has_scripting):
    output_string = f_name
    if has_styling: 
        output_string += " css"
    if has_scripting: 
        output_string += " js"
    return output_string

if __name__ == "__main__":
    main()