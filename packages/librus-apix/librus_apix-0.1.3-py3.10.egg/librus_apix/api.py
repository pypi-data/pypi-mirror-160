from flask import Flask, request, jsonify, make_response, request
from flask_restx import Api, Resource, fields, reqparse
from get_token import get_token, Token, AuthenticationError
from messages import get_recieved, message_content
from grades import get_grades
from attendance import get_attendance, get_detail
from schedule import get_schedule, schedule_detail
from timetable import get_timetable
from datetime import datetime
from announcements import get_announcements
from homework import get_homework, homework_detail

app = Flask(__name__)
api = Api(app)

model = api.model('Login', {
    'username': fields.String,
    'password': fields.String
})

#def header_to_token(auth_header: str):
#    token = Token(request.headers.get(auth_header))

@api.route('/login')
class Login(Resource):
    @api.doc(body=model)
    def post(self):
        try:
            token = get_token(api.payload['username'], api.payload['password'])
            return {"X-API-Key": token.API_Key}, 200
        except KeyError:
            return {"error": "Provide a proper Authorization header"}, 401
        except AuthenticationError as AuthError:
            return {"error": str(AuthError)}, 401
        
@api.route('/messages/<int:page>')
class Message(Resource):
    @api.header("X-API-Key", type=[str])
    def get(self, page):
        token = Token(request.headers.get("X-API-Key"))
        msgs = get_recieved(token, page)
        return msgs
@api.route('/messages/content/<string:content_url>')
class MessageContent(Resource):
    def get(self, content_url: str):
        token = Token(request.headers.get("X-API-Key"))
        content = message_content(token, content_url)
        return content
@api.route('/grades/<int:semester>')
class Grades(Resource):
    def get(self, semester: int):
        def to_dict(obj):
            initial = obj.__dict__
            initial.update({"value": obj.value})
            return initial
        token = Token(request.headers.get("X-API-KEY"))
        g, code = get_grades(token)
        if code != 200:
            return g, code
        grades = {}
        for subject in g[semester]:
            grades[subject] = list(map(to_dict, g[semester][subject]))
        return grades, code
@api.route('/attendance')
class Attendance(Resource):
    def get(self):
        token = Token(request.headers.get("X-API-KEY"))
        attendance = get_attendance(token)
        return attendance
@api.route('/attendance/details/<string:detail_url>')
class AttendanceDetail(Resource):
    def get(self, detail_url: str):
        token = Token(request.headers.get("X-API-KEY"))
        detail = get_detail(token, detail_url)
        return detail
@api.route('/schedule/<string:year>/<string:month>')
class Schedule(Resource):
    def get(self, year: str, month: str):
        token = Token(request.headers.get("X-API-KEY"))
        schedule = get_schedule(token, month, year)
        return schedule
@api.route('/schedule/details/<string:detail_prefix>/<string:detail_url>')
class ScheduleDetail(Resource):
    def get(self, detail_prefix: str, detail_url: str):
        token = Token(request.headers.get("X-API-KEY"))
        details = schedule_detail(token, detail_prefix, detail_url)
        return details
@api.route('/timetable/<string:monday_date>')
class Timetable(Resource):
    def get(self, monday_date: str):
        token = Token(request.headers.get("X-API-KEY"))
        timetable = get_timetable(token, datetime.strptime(monday_date, '%Y-%m-%d'))
        return timetable
@api.route('/announcements')
class Announcements(Resource):
    def get(self):
        token = Token(request.headers.get("X-API-KEY"))
        announcements = get_announcements(token)
        return announcements
@api.route('/homework/details/<string:detail_url>')
class HomeworkDetails(Resource):
    def get(self, detail_url: str):
        token = Token(request.headers.get("X-API-KEY"))
        details = homework_detail(token, detail_url)
        return details
@api.route('/homework/<string:date_from>/<string:date_to>')
class Homework(Resource):
    def get(self, date_from: str, date_to: str):
        token = Token(request.headers.get("X-API-KEY"))
        homework = get_homework(token, date_from, date_to)
        return homework

if __name__ == '__main__':
    app.run(debug=True)