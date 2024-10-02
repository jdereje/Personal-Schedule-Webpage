from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import unquote_plus
import os
import stat
from urllib.parse import urlparse, parse_qs
import datetime
import glob

MimeType = str
Response = bytes

mime_types = {
    "html": "text/html",
    "css": "text/css",
    "js": "application/javascript",
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "mp3": "audio/mpeg",
    "txt": "text/plain",
    "": "application/octet-stream" 
}

content_types = {
    "html": "html",
    "css": "css",
    "js": "js",
    "png": "img",
    "jpg": "img",
    "jpeg": "img",
    "mp3": "audio",
    "txt": "text"
}

#attempt for bonus points
def file_explorer():
    file_list = []
    html_gen = ""
    for file_f in glob.glob("./files/*"):
        file_extension = file_f.split(".")[-1]
        file_name = file_f.split("/")[-1]
        if file_extension in mime_types:
            file_list.append(file_f)
            html_gen = html_gen + '<tr><td><a href="' + file_f + '">' + file_name + '</a></td></tr>'

    try:
        with open("./static/html/explorer.html", "r") as file:
            file_explorer = file.read()
    except FileNotFoundError:
        return open("static/html/404.html").read(), "text/html"

    file_explorer = file_explorer.replace("<file_list_placeholder>", html_gen)
    return file_explorer, "text/html"

#403 Permissions checker
def check_perms(resource):
    stmode = os.stat(resource).st_mode
    return (getattr(stat, 'S_IROTH') & stmode) > 0

#Log response creator and writer
def log_response(response_code, headers, request_path):
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    log_entry = f"{current_time}, {response_code}, {headers}, {request_path}\n"
    with open("response.log", "a") as log_file:
        log_file.write(log_entry)
        

def get_file_mime_types(file_extension):
    if file_extension not in mime_types:
        return "text/plain"
    return mime_types[file_extension]



submissions = []

def get_body_params(body):
    if not body:
        return {}
    parameters = body.split("&")

    # split each parameter into a (key, value) pair, and escape both
    def split_parameter(parameter):
        k, v = parameter.split("=", 1)
        k_escaped = unquote_plus(k)
        v_escaped = unquote_plus(v)
        return k_escaped, v_escaped

    body_dict = dict(map(split_parameter, parameters))
    print(f"Parsed parameters as: {body_dict}")
    # return a dictionary of the parameters
    return body_dict

def submission_to_table(items):
    """Takes a dictionary of form parameters and returns an HTML table row."""

    table_row = f"""
        <tr>
            <td>{items['eventName']}</td>
            <td>{items['dayOfWeek']}</td>
            <td>{items['startTime']}</td>
            <td>{items['stopTime']}</td>
            <td>{items['phoneNumber']}</td>
            <td>{items['location']}</td>
            <td>{items['extraInfo']}</td>
            <td>{items['url']}</td>
        </tr>
    """

    return table_row


def handle_req(url, body=None):
    
    if url == "/FileExplorer.html":
        return file_explorer()
    
    
    #calculator 
    if url.startswith("/calculator"):
        query_string = urlparse(url).query
        parameters = parse_qs(query_string)
        
        num1 = float(parameters.get("num1", [0])[0])
        num2 = float(parameters.get("num2", [0])[0])
        operator = parameters.get("operator", ["+"])[0]
        result = 0
        if operator == "+":
            result = num1 + num2
        elif operator == "-":
            result = num1 - num2
        elif operator == "*":
            result = num1 * num2
        elif operator == "/":
            if num2 != 0:
                result = num1 / num2
            else:
                return "Error: Division by zero", "text/plain"
        return str(result), "text/plain"
    
    #redirect to both youtube and google
    elif url.startswith("/redirect"):
        query_string = urlparse(url).query
        parameters = parse_qs(query_string)
        
        query = parameters.get("query", [""])[0]
        site = parameters.get("site", ["youtube"])[0]
        if site == "youtube":
            location = f"https://www.youtube.com/results?search_query={query}"
        else:
            location = f"https://www.google.com/search?q={query}"
        return "", 307, {"Location": location}



    url_parts = url.split("/")
    relative_path = "/".join(url_parts[1:])
    file_path = os.path.join(os.path.dirname(__file__), relative_path)

    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension[1:].lower()

    if file_extension in mime_types:
        print(f"Trying to access file: {file_path}")

        content_type = mime_types[file_extension]

        try:
            if content_type in ["image/png", "image/jpg", "image/jpeg"]:
                with open(file_path, "rb") as file:
                    file_content = file.read()
            else:
                with open(file_path, "r", encoding="utf-8") as file:
                    file_content = file.read()
                    
                    
        #Handling 404 (FileNotFound Error)            
        except FileNotFoundError:
            print(f"File not found: {file_path}")
            return open(os.path.join(os.path.dirname(__file__), "static", "html", "404.html")).read(), "text/html"
        
        #Handling 403 (Permission Error)
        except PermissionError:
            print(f"Permission denied for: {file_path}")
            return open(os.path.join(os.path.dirname(__file__), "static", "html", "403.html")).read(), "text/html"

        return file_content, content_type


    
    
    if url == "/EventLog.html":
        # Event log handling
        table_rows = ""
        for parameters in submissions:
            table_rows += submission_to_table(parameters)
        return (
            """
            <!DOCTYPE html>
            <html lang="en">
                <head>
                    <title> Event Submission </title>
                </head>
                <body>
                    <header>
                        <nav>
                            <a href="/MySchedule.html">My Schedule</a>
                            <a href="/MyForm.html">Form Input</a>
                            <a href="/AboutMe.html">About Me</a>
                        </nav>
                    </header>
                    <h1> My New Events </h1>
                    <div>
                        <table>
                            <thead>
                                <tr>
                                    <th>Event</th>
                                    <th>Day</th>
                                    <th>Start</th>
                                    <th>End</th>
                                    <th>Phone</th>
                                    <th>Location</th>
                                    <th>Extra Info</th>
                                    <th>URL</th>
                                </tr>
                            </thead>
                            <tbody>
                            """
            + submission_to_table(parameters)
            + """
                            </tbody>
                        </table>
                    </div>
                </body>
            </html>""",
            "text/html; charset=utf-8",
        )

    return open(os.path.join(os.path.dirname(__file__), "static", "html", "404.html")).read(), "text/html; charset=utf-8"




# You shouldn't change content below this. It would be best if you just left it alone.

class RequestHandler(BaseHTTPRequestHandler):
    def __c_send_response(self, message, response_code, headers):

        if type(message) == str:
            message = bytes(message, "utf8")

        self.protocol_version = "HTTP/1.1"
        self.send_response(response_code)


        for key, value in headers.items():
            self.send_header(key, value)
        self.send_header("Content-Length", len(message))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()

        self.wfile.write(message)

        log_response(response_code, headers, self.path)

    def do_GET(self):
        if self.path.startswith("/calculator"):
 
            response = handle_req(self.path)
        elif self.path.startswith("/redirect"):
            response = handle_req(self.path)
        else:
            if self.path == "/EventLog.html":
                response = handle_req(self.path)
            else:
                file_path = os.path.join(os.path.dirname(__file__), self.path[1:])
                if os.path.exists(file_path):
                    if check_perms(file_path):
                        response = handle_req(self.path)
                    else:
                        response = open(os.path.join(os.path.dirname(__file__), "static", "html", "403.html")).read(), "text/html; charset=utf-8"
                else:
                    response = open(os.path.join(os.path.dirname(__file__), "static", "html", "404.html")).read(), "text/html; charset=utf-8"


        if isinstance(response, tuple) and len(response) == 3:
            message, response_code, headers = response
            self.__c_send_response(message, response_code, headers)
        elif isinstance(response, tuple) and len(response) == 2:
            message, content_type = response
            self.__c_send_response(
                message,
                200,
                {
                    "Content-Type": content_type,
                    "Content-Length": len(message),
                    "X-Content-Type-Options": "nosniff",
                },
            )
        else:
            print("Invalid response from handle_req")



    def do_POST(self):
        body = self.__c_read_body()
        response = handle_req(self.path, body)

 
        if isinstance(response, tuple) and len(response) == 3:
            message, response_code, headers = response
            self.__c_send_response(message, response_code, headers)
        elif isinstance(response, tuple) and len(response) == 2:
            message, content_type = response
            self.__c_send_response(
                message,
                200,
                {
                    "Content-Type": content_type,
                    "Content-Length": len(message),
                    "X-Content-Type-Options": "nosniff",
                },
            )
        else:
            print("Invalid response from handle_req")

def run():
    PORT = 8026
    print(f"Starting server http://localhost:{PORT}/")
    server = ("", PORT)
    httpd = HTTPServer(server, RequestHandler)
    httpd.serve_forever()

run()