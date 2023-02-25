from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required

from . import app, db
from .models import Employee, Position, User
from .forms import PositionForm, EmployeeForm, UserForm
from sqlalchemy.exc import IntegrityError


def index():
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)


def position_create():
    title = 'Position'
    form = PositionForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            position = Position()
            form.populate_obj(position)
            db.session.add(position)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            print(form.errors)
    return render_template('standard_form.html', form=form, title=title)


@login_required
def employee_create():
    title = 'Employ'
    form = EmployeeForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            employee = Employee()
            form.populate_obj(employee)
            db.session.add(employee)
            try:
                db.session.commit()
            except IntegrityError:
                flash('Такой сотрудник уже существует', 'danger')
            else:
                flash('Вы успешно зарены', 'success')
                return redirect(url_for('index'))
        else:
            print(form.errors)
    return render_template('standard_form.html', form=form, title=title)


@login_required
def employee_update(employee_id):
    employee = Employee.query.get(employee_id)
    form = EmployeeForm(obj=employee)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(employee)
            db.session.add(employee)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            print(form.errors)
    return render_template('standard_form.html', form=form)


@login_required
def employee_delete(employee_id):
    employee = Employee.query.get(employee_id)
    if request.method == "POST":
        db.session.delete(employee)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('confirm_delete.html', employee=employee)


def register():
    title = 'Регистрация'
    form = UserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User()
            form.populate_obj(user)
            db.session.add(user)
            try:
                db.session.commit()
            except IntegrityError:
                flash('Такой пользователь уже существует', 'danger')
            else:
                flash('Вы успешно зарены', 'success')
                return redirect(url_for('login'))
        else:
            print(form.errors)
    return render_template('user_form.html', form=form, title=title)


def login():
    title = 'Login'
    form = UserForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('index'))
            else:
                print('Errors data')
        else:
            print(form.errors)
    return render_template('user_form.html', form=form, title=title)


def logout():
    logout_user()
    return redirect(url_for('login'))
