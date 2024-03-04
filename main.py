import sqlite3

from flask import Flask, request, g, render_template, send_file

DATABASE ='/tmp/chatbot.db'
app = Flask(__name__)
app.config.from_object(__name__)

def connect_to_database():
    return sqlite3.connect(app.config['DATABASE'])

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = g.db = connect_to_database()
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def execute_query(query, args=()):
    cur = get_db().execute(query, args)
    rows = cur.fetchall()
    cur.close()
    return rows

def commit():
    get_db().commit()

@app.route("/")
def hello():
    execute_query("DROP TABLE IF EXISTS userstable")
    execute_query("CREATE TABLE userstable (firstname text,lastname text,email text)")
    return render_template('index.html')

@app.route('/startenquiry', methods =['POST', 'GET'])
def startinquiry():
    message = ''
    if request.method == 'POST' and str(request.form['ufname']) !="" and str(request.form['ulname']) != "" and str(request.form['mail']) != "":
        firstname = str(request.form['ufname'])
        lastname = str(request.form['ulname'])
        email = str(request.form['mail'])
        result = execute_query("""INSERT INTO userstable (firstname, lastname, email) values (?, ?, ?)""",(firstname, lastname, email))
        commit()
    elif request.method == 'POST':
        message = 'OOPS! Some required fields are missing. Please fill in all the fields.'
    return render_template('Chat.html', message = message)

ChatWindowHTMLFirst = """
    <!DOCTYPE html>
    <html>
      <title>University of Cincinnati Inquiry Chatbot </title>
      <body>
      <div style="width:500px;margin: auto;border: 1px solid black;padding:10px">
        <form {{url_for('chatbotsystem')}} method="POST">
          <h1>University of Cincinnati Inquiry Chatbot</h1>
          <div class="icon">
    	 <i class="fas fa-user-circle"></i>
          </div>
          <div class="formcontainer">
          <div class="container">
           <label for="ufname"><strong>Hello! University of Cincinnati Inquiry Chatbot</strong></label></br></br>
    	  <label for="ufname"><strong>Choose your questions from the list below:</strong></label></br>
    	  <label for="ufname"><strong> Does the college have a football team?</strong></label></br>
    	  <label for="ufname"><strong> How can I apply for need based scholarships as an international student?</strong></label></br>       
    	  <label for="ufname"><strong> Does it have Computer Science Major?</strong></label></br>
    	  <label for="ufname"><strong> What is the in-state tuition?</strong></label></br>
          <label for="ufname"><strong> How many co-ops do Engineering majors need to do?</strong></label></br>
    	  <label for="ufname"><strong> Does it have on campus housing?</strong></label></br>
    """

ChatWindowHTMLLast = """
    </br>
    </div>
    	<div class="text-box">
            <input type="text" style="width:300pt;height:50px" name="question" id="message" autocomplete="off" placeholder="Type your QUESTIONS here">
    	  <input class="send-button" style="width:50pt;height:50px" type="submit" value=">">
          </div></br>
           <a href='/endchat' align='center'">End Chat?</a>
    	</div>
        </form>
        </div>
      </body>
    </html>
    """


@app.route('/chatbotsystem', methods =['GET', 'POST'])
def chatbotsystem():
    global ChatWindowHTMLFirst
    ChatWindowHTMLMiddle = ''
    if request.method == 'POST' and str(request.form['question']) !="":
        questionasked = str(request.form['question'])
        if(questionasked in "Does the college have a football team?"):
            ChatWindowHTMLMiddle="""
            </br><label for="ufname" style="color:blue;"><strong>"""+questionasked+"""</strong></label></br>
            <label for ="ufname"><strong>Yes, The football team of the university is known as the Cincinnati Bearcats.</strong></label></br>
            """
        elif(questionasked in "How can I apply for need based scholarships as an international student?"):
            ChatWindowHTMLMiddle = """
            </br><label for="ufname" style="color:blue;"><strong>""" + questionasked + """</strong></label></br>
            <label for ="ufname"><strong>International Students are eligible for merit-based scholarships only.</strong></label></br>
            """
        elif(questionasked in "Does it have Computer Science Major?"):
            ChatWindowHTMLMiddle = """
            </br><label for="ufname" style="color:blue;"><strong>""" + questionasked + """</strong></label></br>
            <label for ="ufname"><strong>Yes, Computer Science Major is one of the poplular majors in the College of Engineering and Applied Sciences at UC.</strong></label></br>
            """
        elif (questionasked in "What is the in-state tuition?"):
            ChatWindowHTMLMiddle = """
            </br><label for="ufname" style="color:blue;"><strong>""" + questionasked + """</strong></label></br>
            <label for ="ufname"><strong>At the University of Cincinnati, the in-state tuition UC is around $28,150.</strong></label></br>
            """
        elif (questionasked in "Does it have on campus housing?"):
            ChatWindowHTMLMiddle = """
            </br><label for="ufname" style="color:blue;"><strong>""" + questionasked + """</strong></label></br>
            <label for ="ufname"><strong>Yes, The university does have on campus housing options available for all the students. For Freshmen class it's mandatory to live on campus, while for other's it is optional</strong></label></br>
            """
        elif (questionasked in "How many co-ops do Engineering majors need to do?"):
            ChatWindowHTMLMiddle = """
            </br><label for="ufname" style="color:blue;"><strong>""" + questionasked + """</strong></label></br>
            <label for ="ufname"><strong>As an engineering major you need to do 5 co-ops as part of your curriculum.</strong></label></br>
            """
        else:
            ChatWindowHTMLMiddle = """
            </br><label for="ufname" style="color:blue;"><strong>""" + questionasked + """</strong></label></br>
            <label for ="ufname"><strong>Sorry, the answer to your question doesn't exist. Please choose from the questions provided above.</strong></label></br>
            """
    ChatWindowHTMLFirst=ChatWindowHTMLFirst + ChatWindowHTMLMiddle
    return ChatWindowHTMLFirst+ChatWindowHTMLLast

EndChatHTMLFirst="""
<!DOCTYPE html>
<html>
  <title> University of Cincinnati Inquiry Chatbot - Session Closed</title>
  <body>
  <div style="width:500px;margin: auto;border: 1px solid black;padding:10px">
    <form>
      <h1>Chat Session is currently closed</h1>
      <div class="icon">
	 <img src="https://static.thenounproject.com/png/878515-200.png" width="200" height="200"></img>
      </div>
      <div class="formcontainer">
      <div class="container">
        <label for="ufname"><strong>Thank you for your interest, Hope all of your questions are answered!</strong></label></br></br>
"""

EndChatHTMLLast="""
 </div>
	</div>
    </form>
    </div>
  </body>
</html>
"""
@app.route("/endchat")
def endchat():
    global ChatWindowHTMLFirst
    ChatWindowHTMLFirst = """
        <!DOCTYPE html>
        <html>
          <title>University of Cincinnati Inquiry Chatbot</title>
          <body>
          <div style="width:500px;margin: auto;border: 1px solid black;padding:10px">
            <form {{url_for('chatbotsystem')}} method="POST">
              <h1>University of Cincinnati Inquiry Chatbot</h1>
              <div class="formcontainer">
              <div class="container">
           <label for="ufname"><strong>Hello! University of Cincinnati Inquiry Chatbot</strong></label></br></br>
    	  <label for="ufname"><strong>Choose your questions from the list below:</strong></label></br>
    	  <label for="ufname"><strong> Does the college have a football team?</strong></label></br>
    	  <label for="ufname"><strong> How can I apply for need based scholarships as an international student?</strong></label></br>       
    	  <label for="ufname"><strong> Does it have Computer Science Major?</strong></label></br>
    	  <label for="ufname"><strong> What is the in-state tuition?</strong></label></br>
          <label for="ufname"><strong> How many co-ops do Engineering majors need to do?</strong></label></br>
    	  <label for="ufname"><strong> Does it have on campus housing?</strong></label></br>
        """
    result = execute_query("""SELECT firstname, lastname, email  FROM userstable""")
    if result:
        for row in result:
            Userdetails=row[0]+" "+row[1]+", "+row[2]
    EndChatHTMLMiddle="""
    User Information: <br>
    <label for="ufname"><strong>"""+Userdetails+"""</strong></label></br></br>
    Developer Information: <br>
    <label for="ufname"><strong>Haneesha Dushara, dusharha@mail.uc.edu</strong></label></br></br>
    """
    return EndChatHTMLFirst+EndChatHTMLMiddle+EndChatHTMLLast

if __name__ == '__main__':
  app.run()