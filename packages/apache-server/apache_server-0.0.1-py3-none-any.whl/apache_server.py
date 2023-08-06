import time
import subprocess
from turtle import Turtle

def help():
    print("ICCS moving text = apache_server.iccs_movingtext_ass1()")
    print("Ordered List Unordered List = apache_server.ulol()")
    print("Country Population Table = apache_server.country_population_table()")
    print("Number Roll no Etc = apache_server.namerolletc()")
    print("Family names in css = apache_server.familynames_intcss()")
    print("Css cricket = apache_server.css_cricket()")
    print("Placements Details Css = apache_server.placement_details_css()")
    print("CSS college = apache_server.css_college_html()")
    print("Form with css = apache_server.css_form()")
    print("Operating system form css = apache_server.os_form")
    print("Sort numbers using js = apache_server.js_sort()")
    print("Day and time = apache_server.js_dayandtime()")
    print("Factorial = apache_server.js_factorial()")
    print("Reverse = apache_server.js_reverse()")
    print("Vowels = apache_server.js_vowels")
    print("Volume of sphere = apache_server.js_volumesphere()")
    print("Calculator = apache_server.js_calculator()")

def iccs_movingtext_ass1():
    code = """
    <!Doctype html>
    <html>
    <head>
    <title> ICCS </title>
    </head>
    <body style="background-image: url();">
    <header>
    <center>
    <h1> <u> <i> INDIRA COLLEGE OF COMMERCE AND SCIENCE </u> </i> </h1>
    <img src="">
    </center>
    <marquee> <h2> <i> Welcome to Indira College of Commerce and Science (ICCS) Pune.... </h2> </i> </marquee>
    <h2 align="center"> Pimpri Chincwad Maharastra Pune...</h2>
    </header>
    <h3> <u> Courses : </u> </h3>
    <font size="4" color="red"
    <b> BSC Cyber Security </b>
    <br>
    </font>
    <font size="3" color="blue"
    <b> BCS </b>
    <br>
    </font>
    <font size="3" color="brown"
    <b> BSc (Comp.Sci) </b>
    <br>
    </font>
    <font size="3" color="orange"
    <b> BCA </b>
    <br>
    </font>
    <font size="3" color="pink"
    <b> B-Pharmacy </b>
    <br>
    </font>
    <font size="3" color="black"
    <b> D-Pharmacy </b>
    <br>
    </font>
    <footer>
    <p> <b> Author: ICCS </b> </p>
    <p> <a href="http://www.iccs.ac.in/"> Click here </a></p>
    </body>
    </html>
    """
    f = open("iccs.html", "a")
    f.write(code)
    f.close()
    print("[+] Starting apache2 service")
    print("[+] apache2 service started")
    subprocess.call("rm start_server.py", shell=True)
    

def ulol():
    code = """
    <html>
    <title> Lists
    </title>
    <body>
    <b>   <ul type=square>
                    <li>Coffee
                    <li>Tea
        <ul type=disc>
                    <li> Black tea 
                    <li> Green tea
        <ul type=circle>
                    <li> Africa   
                    <Li> China
                            </ul>
                        </ul>
                    </ul>
        <ul type=square>
                    <li> Milk
                            </ul>
    </b>
    </body>
    
    </html>
    """
    f = open("lists.html", "a")
    f.write(code)
    f.close()
    print("[+] Starting apache2 service")
    print("[+] apache2 service started")
    subprocess.call("rm start_server.py", shell=True)

def country_population_table():
    code = """
    <HTML>
    <HAED>
    <title> Question  </title>
    </HAED>
    <table border="2" align="center">
    <tr>
    <th> Country </th>
    <th colspan="2">Population (In Crores)</th>
    <tr>
    <td rowspan="3" aling="center"> India </td>
    <td> 1998 </td>
    <td> 85 </td>
    </tr>
    <td> 1999 </td>
    <td> 90 </td>
    <tr>
    <td> 2000 </td>
    <td> 100 </td>
    </tr>
    <tr>
    <td rowspan="3" aling="center"> USA </td>
    <td> 1998 </td>
    <td> 30 </td>
    </tr>
    <tr>
    <td> 1999 </td>
    <td> 35 </td>
    </tr>
    <tr>
    <td> 2000 </td>
    <td> 40 </td>
    </tr>
    <tr>
    <td rowspan="3" aling="center"> UK </td>
    <td> 1998 </td>
    <td> 25 </td>
    </tr>
    <tr>
    <td> 1999 </td>
    <td> 30 </td>
    </tr>
    <tr>
    <td> 2000 </td>
    <td> 35 </td>
    </tr>
    </html>
    """
    f = open("countrypopulation.html", "a")
    f.write(code)
    f.close()
    print("[+] Starting apache2 service")
    print("[+] apache2 service started")
    subprocess.call("rm start_server.py", shell=True)

def namerolletc():
    code = """
    <html>
    <head>
    <title>Form</title>
    </head>

    <body style="background-image: url(/home/jagtap/Downloads/nature.jpg);">
    <h1 align="center"> Name = abc </h1>
    <br>
    <h1 align="center"> Roll Number = Aaaa</h1>
    <br>
    <h1 align="center"> Course name = BSC(Specilization in Cyber Security) </h1>
    <br>
    <h1 align="center"> Birth date= 18/04/2003 </h1>
    <br> 
    </body>
    </html>
    """
    f = open("namerollno.html", "a")
    f.write(code)
    f.close()
    print("[+] Starting apache2 service")
    print("[+] apache2 service started")
    subprocess.call("rm start_server.py", shell=True)

def familynames_intcss():
    code = """
    <!DOCTYPE html>
    <HTML>
    <BODY>
    <style>
    body{
    background-color:red;
    }
    h1{
    color:black;
    text-align:center;
    }
    h2{
    color:black;
    text-align:center;
    }
    h3{
    color:black;
    text-align:center;
    }
    h4{
    color:black;
    text-align:center;
    }
    </style>
    <h1> eere </h2>
    <h2> Merte </h2>
    <h3> err </h3>
    <h4> rttr </h3>
    </BODY>
    </HTML>
    """
    f = open("familynameintcss.html", "a")
    f.write(code)
    f.close()
    print("[+] Starting apache2 service")
    print("[+] apache2 service started")
    subprocess.call("rm start_server.py", shell=True)

def css_cricket():
    code = """
    <!Doctype hrml>
    <html>
    <head>
    <title></title>
    </head>
    <body>
    <style>
    body{
    background-color:yellow;
    }
    </style>
    <center>
    <b> MAHENDRA SINGH DHONI <b>
    <br>
    <I> VIRAT KOHLI <I>
    <BR>
    <I> KL RAHUL <U>
    <BR>
    <B> <I> <U> MAHENDRA SINGH DHONI <B> <I> <U>
    <BR>
    <B> <I> <U> VIRAT KOHLI <B> <I> <U>
    <BR>
    <B> <I> <U> KL RAHUL <B> <I> <U>
    <BR>
    </center>
    </BODY>
    </HTML>
    """
    f = open("csscricket.html", "a")
    f.write(code)
    f.close()
    print("[+] Starting apache2 service")
    print("[+] apache2 service started")
    subprocess.call("rm start_server.py", shell=True)

def placement_details_css():
    code = """
    <!Doctype html>
    <html>
    <head>
    <title></title>
    </head>
    <style type="text/css">
    body{
    color:red;
    }
    table{
    border:1px solid black;
    }
    h2{
    color:black;
    }
    </style>
    <body>
    <center>
    <h2> Yearly placement details </h2>
    <table>
    <tr>
    <th> </th>
    <th colspan="3"> Years </th>
    </tr>
    <tr>
    <td> </td>
    <td> 2010 </td>
    <td> 2011 </td>
    <td> 2012 </td>
    </tr>
    <tr>
    <td> No.of students appeared </td>
    <td> 400 </td>
    <td> 550 </td>
    <td> 700 </td>
    </tr>
    <tr>
    <td> Distinction </td>
    <td> 150 </td>
    <td> 175 </td>
    <td> 250 </td>
    </tr>
    <tr>
    <td> I Class </td>
    <td> 125 </td>
    <td> 200 </td>
    <td> 225 </td>
    </tr>
    <tr>
    <td> II class </td>
    <td> 120 </td>
    <td> 125 </td>
    <td> 100 </td>
    </tr>
    </center>
    """
    f = open("placementcss.html", "a")
    f.write(code)
    f.close()
    print("[+] Starting apache2 service")
    print("[+] apache2 service started")
    subprocess.call("rm start_server.py", shell=True)

def css_college_html():
    code_html = """
    <!doctype html>
    <html>
    <head>
    <link rel="stylesheet"href="mystyle.css">
    </head>
    <title>ICCS</TITLE>
    <body>
    <h1>INDIRA COLLEGE OF COMMERCE AND SCIENCE</h1>
    <marquee> <h3><i> WELCOME TO INDIRA COLLEGE OF COMMERCE AND SCIENCE(ICCS) PUNE......</H3> </I> </MARQUEE>
    <h4 align="center"> Pimpri Chinchwad maharashtra pune.....</h4>
    <bIG>COURSES</bIG>
    <h5>BSC</H5>
    <u>BCS</u>
    <br>
    <b>BCA</b>
    <br>
    <SMALL>BCOM</SMALL>
    <br>
    </DIV>
    <footer>
    <IMG SRC="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR3Sq2AschMkl6k4inWwNkvpz-Q6IKJa8aHgQ&usqp=CAU.png" WIDTH=300 HEIGHT=300>
    </footer>
    </body>
    </html>
    """

    code_css = """
    body{
    background-repeat:no-repeat;
    background-image:url("https://www.howtogeek.com/wp-content/uploads/2009/08/image27.png?width=1198&trim=1,1&bg-color=000&pad=1,1.PNG");
    background-size:1580Px 800px;
    }

    h1{
    color:LIGHTblue;
    text-align:center;
    }
    h2{
    color:red;
    }
    H3{
    COLOR:yellow;
    }
    u{
    color:blue;
    }
    big{
    color:lightblue;
    }
    H4{
    FONT-SIZE:30PX
    }
    """

    f = open("css_college.html", "a")
    f.write(code_html)
    f.close()

    f1 = open("mystyle.css", "a")
    f.write(code_css)
    f.close()

    print("[+] Starting apache2 service")
    print("[+] apache2 service started")
    subprocess.call("rm start_server.py", shell=True)

def css_form():
    code = """
    <html>
	<head><title>Form demo</title></head>
	<body bgcolor= #fcf3cf>
		<form>
			<p style=font-color:red;font-size:20pt;>
			CREATE NEW ACCOUNT</p><BR><BR>
			First Name: <input type=text><br><br>
			Last Name: <input type=text><br><br>
			Gender: <input type=radio> Male<input type=radio>
			Female<br><br>
			Age: <input type=text><br><br>
			Birth Date: <input type=text><br><br>
			Time: <input type=text><br><br>
			Country: <select>
				<option>India</option>
				<option>USA</option>
				<option>UK</option>
				<option>Germany</option>
				<option>France</option>
			</select>
			<br><br>
			Fav. Games:<input type=checkbox>chess<input type=checkbox>Pokers<br><br>
			Fav. colors:<input type=checkbox>Black<input type=checkbox>Orange<br><br>
			Telephone no.:<textarea ></textarea><br><br>
			<input type=submit value-"Sign Up">
		</form></body></html>
    """

    f = open("css_form.html", "a")
    f.write(code)
    f.close()
    print("[+] Starting apache2 service")
    print("[+] apache2 service started")
    subprocess.call("rm start_server.py", shell=True)

def os_form():
    code = """
    <!Doctype html>
    <html>
    <head>
    <title> Question 5 </title>
    </head>
    <form>
    <body>
    Enter your name<input type="text" name="t1">
    <br><br>
    password<input type="password" name="t2">
    <br><br>
    Country <select name="cont" id="cont">
    <option value="in"> India </option>
    <option value="np"> Nepal </option>
    </select>
    Details:
    <textarea id="textdetails" name="txtdetails" rows="4" cols="50"> </textarea><br>
    Which of the following Operating systems have you used <br><br>
    <input type=radio name=r1>Linux
    <input type=radio name=r1> Windows 10
    <input type=radio name=r1> Macintosh 8.0
    <br><br>
    Which of the operating system do you like the best? <br><br>
    <input type=checkbox name=c1> Linux
    <input type=checkbox name=c2> Windows 10
    <input type=checkbox name=c3> Macintosh 8.0
    <br>
    <br>
    You have Completed the Form
    <input type=submit value="Sign Up"></h4>
    </form>
    </body>
    </html>
    """
    f = open("os_form.html", "a")
    f.write(code)
    f.close()
    print("[+] Starting apache2 service")
    print("[+] apache2 service started")
    subprocess.call("rm start_server.py", shell=True)


###############JS

def js_sort():
    code = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sorting</title>
        <script>
        const num1 = parseInt(prompt("Enter the num1 :"));
        const num2 = parseInt(prompt("Enter the num1 :"));
        const num3 = parseInt(prompt("Enter the num1 :"));
        if (num1 > num2 && num1 > num3 && num2 > num3) {
            alert(num1 + " " + num2 + " " + num3);
        } else if (num2 > num1 && num2 > num3 && num1 > num3) {
            alert(num2 + " " + num1 + " " + num3);
        } else if (num3 > num1 && num3 > num2 && num1 > num2) {
            alert(num3 + " " + num1 + " " + num2);
        } else if (num1 > num2 && num1 > num3 && num2 < num3) {
            alert(num1 + " " + num3 + " " + num2);
        } else if (num2 > num1 && num2 > num3 && num1 < num3) {
            alert(num2 + " " + num3 + " " + num1);
        } else if (num3 > num1 && num3 > num2 && num1 < num2) {
            alert(num3 + " " + num2 + " " + num1);
        }
        </script>
    </head>
    </html>
    """
    f = open("js_sort.html", "a")
    f.write(code)
    f.close()
    print("[+] Starting apache2 service")
    print("[+] apache2 service started")
    subprocess.call("rm start_server.py", shell=True)

def js_dayandtime():
    code = """
    <!doctype html>
    <html>
    <body>
    Time: <p id="d1"></p>
    Day: <p id= "d2"></p>
    <script>
    const t1 = new Date() ;
    const time = t1.toLocaleTimeString("en-US");
    document.getElementById("d1").innerHTML = time;
    const days=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"];
    const d1 = new Date();
    let day = days[d1.getDay()];
    document.getElementById("d2").innerHTML = day;
    </script>
    </body>
    </html>
    """
    f = open("js_daytime.html", "a")
    f.write(code)
    f.close()
    print("[+] Starting apache2 service")
    print("[+] apache2 service started")
    subprocess.call("rm start_server.py", shell=True)

def js_factorial():
    code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Document</title>
    </head>
    <body>
        Factorial:
        <input type="number" id="factNum" />
        <p id="fact"></p>
    </body>
    <script>
        function factor(n) {
        fact = 1;
        for (var i = 1; i <= n; i++) {
            fact = fact * i;
        }
        return fact;
        }
        var x = document.getElementById("factNum").value;
        document.getElementById("fact").innerHTML = factor(x);
    </script>
    </html>
    """
    f = open("js_factorial.html", "a")
    f.write(code)
    f.close()
    print("[+] Starting apache2 service")
    print("[+] apache2 service started")
    subprocess.call("rm start_server.py", shell=True)

def js_reverse():
    code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Document</title>
    </head>
    <body>
        Num
        <input type="number" id="Num" />
        <p id="revNum"></p>
    </body>
    <script>
        function revNum(n) {
        let a = n.toString().split("").reverse().join("");
        return a;
        }
        var x = document.getElementById("Num").value;
        document.getElementById("revNum").innerHTML = revNum(x);
    </script>
    </html>
    """
    f = open("js_reverse.html", "a")
    f.write(code)
    f.close()
    print("[+] Starting apache2 service")
    print("[+] apache2 service started")
    subprocess.call("rm start_server.py", shell=True)

def js_vowels():
    code = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Document</title>
    </head>
    <body>
        String
        <input type="text" id="str" />
        <p id="vow"></p>
    </body>
    <script>
        function CountVow(str1) {
        const cnt = str1.match(/[aeiou]/gi).length;
        return cnt;
        }

        let c = document.getElementById("str").value;
        document.getElementById("vow").innerHTML = CountVow(c);
    </script>
    </html>
    """
    f = open("js_vowels.html", "a")
    f.write(code)
    f.close()
    print("[+] Starting apache2 service")
    print("[+] apache2 service started")
    subprocess.call("rm start_server.py", shell=True)

def js_volumesphere():
    code = """
    <!doctype html>
    <html>
    <body>
    <p> Volume of Sphere </p>
    Volume:<div id="demo"></div>
    <script>
    function MyResult(r)
    {
    return 4/3 * pi * r * r * r;
    }
    const pi=3.142;
    var r = prompt("please enter the radius ","Enter radius");
    document.getElementById("demo").innerHTML=MyResult(r);
    </script>
    </body>
    </html>
    """
    f = open("js_volume_sphere.html", "a")
    f.write(code)
    f.close()
    print("[+] Starting apache2 service")
    print("[+] apache2 service started")
    subprocess.call("rm start_server.py", shell=True)

def js_calculator():
    code = """
    <!DOCTYPE html>
    <html>
    <body>
        <p>
        This example calls a function which performs a calculation, and returns
        the result:
        </p>
        Multiplication:
        <div id="d1"></div>
        Addition:
        <div id="d2"></div>
        Substraction:
        <div id="d3"></div>
        Division:
        <div id="d4"></div>
        <script>
        function myfunction(a, b) {
            return a * b;
        }
        function myadd(a, b) {
            return a + b;
        }
        function mysub(a, b) {
            return a - b;
        }
        function mydiv(a, b) {
            return a / b;
        }
        var n1 = prompt("Please enter number n1", "Enter number");
        var n2 = prompt("Please enter number n2", "Enter number");
        document.getElementById("d1").innerHTML = myfunction(n1, n2);
        document.getElementById("d2").innerHTML = myadd(n1, n2);
        document.getElementById("d3").innerHTML = mysub(n1, n2);
        document.getElementById("d4").innerHTML = mydiv(n1, n2);
        </script>
    </body>
    </html>
    """
    f = open("js_calc.html", "a")
    f.write(code)
    f.close()
    print("[+] Starting apache2 service")
    print("[+] apache2 service started")
    subprocess.call("rm start_server.py", shell=True)


js_calculator()