from flask import Flask, render_template, request, make_response
from wtforms import SelectField, SubmitField, StringField
from flask.views import MethodView
from flask_wtf import FlaskForm
from calc import Calculator

app = Flask(__name__)
app.config['SECRET_KEY'] = '98765'


class HomePage(MethodView):

    def get(self):
        return render_template('index.html')


class CalculatePage(MethodView):

    def get(self):
        calc_form = CalcForm()
        return render_template('calculate.html',
                               calcform=calc_form)

    def post(self):
        calc_form = CalcForm(request.form)

        first_num = calc_form.first_num.data.replace(',', '.')
        second_num = calc_form.second_num.data.replace(',', '.')
        operation = calc_form.opts.data

        try:
            if operation == 'add':
                equation = f'{first_num} + {second_num}'
                result = Calculator(float(first_num), float(second_num)).add()
            elif operation == 'subtract':
                equation = f'{first_num} - {second_num}'
                result = Calculator(float(first_num), float(second_num)).subtract()
            elif operation == 'multiply':
                equation = f'{first_num} * {second_num}'
                result = Calculator(float(first_num), float(second_num)).multiply()
            else:
                equation = f'{first_num} / {second_num}'
                result = Calculator(float(first_num), float(second_num)).divide()
        except (TypeError, ValueError):
            result = 'Type only numbers!'
            equation = None

        if type(result) == float or result == 'Can not divide by zero!':
            resp = make_response(render_template('calculate.html',
                                                 calcform=calc_form,
                                                 result=result))
            resp.set_cookie(equation, str(result))
            return resp
        return render_template('calculate.html',
                               calcform=calc_form,
                               result=result)


class HistoryPage(MethodView):

    def get(self):
        calculations = dict(request.cookies)
        calculations.pop('session')
        return render_template('history.html',
                               calcs=calculations)


class CalcForm(FlaskForm):

    first_num = StringField()
    second_num = StringField()
    opts = SelectField('Operation',
                       choices=[('add', 'Add'),
                                ('subtract', 'Subtract'),
                                ('multiply', 'Multiply'),
                                ('divide', 'Divide')])
    button = SubmitField('Calculate')


app.add_url_rule('/', view_func=HomePage.as_view('home_page'))
app.add_url_rule('/calculate', view_func=CalculatePage.as_view('calculate_page'))
app.add_url_rule('/history', view_func=HistoryPage.as_view('history_page'))

app.run(debug=True)
