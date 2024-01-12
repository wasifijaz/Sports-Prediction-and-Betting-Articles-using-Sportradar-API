from flask import Flask, send_file

app = Flask(__name__)

@app.route('/nba-zip/')
def return_files_nba():
    try:
        return send_file('/home/ubuntu/article-automation/NBA.zip')
    except Exception as e:
        return str(e)
    
@app.route('/nhl-zip/')
def return_files_nhl():
    try:
        return send_file('/home/ubuntu/article-automation/NHL.zip')
    except Exception as e:
        return str(e)

@app.route('/nfl-zip/')
def return_files_nfl():
    try:
        return send_file('/home/ubuntu/article-automation/NFL.zip')
    except Exception as e:
        return str(e)


@app.route('/mlb-zip/')
def return_files_mlb():
    try:
        return send_file('/home/ubuntu/article-automation/MLB.zip')
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(debug=True, port=5002)