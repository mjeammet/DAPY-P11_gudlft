import datetime
import json
from typing_extensions import Required
from flask import Flask, render_template, request, redirect, flash, url_for

MAX_PER_CLUB = 12
POINTS_PER_ENTRY = 3


def loadClubs(clubs_json):
    with open(clubs_json) as c:
        listOfClubs = json.load(c)['clubs']
        for club in listOfClubs:
            club['points'] = int(club['points'])
        return listOfClubs


def loadCompetitions(competitions_json):
    with open(competitions_json) as comps:
        listOfCompetitions = json.load(comps)['competitions']
        date_format = "%Y-%m-%d %H:%M:%S"
        for competition in listOfCompetitions:
            competition['date'] = datetime.datetime.strptime(competition["date"], date_format)
            if competition['date'] < datetime.datetime.now():
                competition['is_past'] = True
            else:
                competition['is_past'] = False
        return listOfCompetitions


def create_app(config={}):
    app = Flask(__name__)
    app.config.update(config)
    app.secret_key = 'something_special'

    competitions_json = 'competitions.json'
    clubs_json = 'clubs.json'
    if app.config["TESTING"] == True:
        competitions_json = 'tests/test_dataset.json'
        clubs_json = 'tests/test_dataset.json'

    competitions = loadCompetitions(competitions_json)
    clubs = loadClubs(clubs_json)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/showSummary',methods=['POST'])
    def showSummary():
        email = request.form['email']
        try:
            club = [club for club in clubs if club['email'] == email][0]
        except IndexError:
            flash('Sorry, that email wasn\'t found.')
            return redirect(url_for('index'))
        return render_template('welcome.html', club=club, competitions=competitions)

    @app.route('/book/<competition>/<club>')
    def book(competition,club):
        foundClub = [c for c in clubs if c['name'] == club][0]
        if foundClub["points"] < POINTS_PER_ENTRY:
            flash("You don't have enough points to make any reservation.")
            return render_template('welcome.html', club=foundClub, competitions=competitions)
        foundCompetition = [c for c in competitions if c['name'] == competition][0]
        if foundCompetition['is_past'] == True:
            flash('Cannot book past competitions.')
            return bad_request()
        if foundClub and foundCompetition:
            return render_template('booking.html', club=foundClub, competition=foundCompetition, points_per_entry=POINTS_PER_ENTRY)
        else:
            flash("Something went wrong-please try again")
            return render_template('welcome.html', club=club, competitions=competitions)

    @app.route('/purchasePlaces',methods=['POST'])
    def purchasePlaces():
        competition = [c for c in competitions if c['name'] == request.form['competition']][0]
        club = [c for c in clubs if c['name'] == request.form['club']][0]
        if competition['is_past'] == True:
            flash('Cannot book past competitions.')
            return bad_request()
        placesRequired = int(request.form['places'])
        placesRemaining = int(competition['numberOfPlaces'])
        if placesRequired > club['points']/POINTS_PER_ENTRY:
            flash(f"Cannot book - trying to book more than what you have.")
            return render_template('booking.html',club=club, competition=competition, points_per_entry=POINTS_PER_ENTRY)
        elif placesRequired > placesRemaining:
            flash(f"Cannot book - trying to book more than what remains.")
            return render_template('booking.html', club=club, competition=competition, points_per_entry=POINTS_PER_ENTRY)
        elif placesRequired > MAX_PER_CLUB:
            flash(f'Cannot book - Trying to book more than maximum allowed ({MAX_PER_CLUB})')
            return render_template('booking.html', club=club, competition=competition, points_per_entry=POINTS_PER_ENTRY)
        else:
            flash(f'Great, succesfully booked {placesRequired} place(s)!')
            club['points'] = club['points'] - placesRequired*POINTS_PER_ENTRY
            competition['numberOfPlaces'] = int(competition['numberOfPlaces']) - placesRequired
            return render_template('welcome.html', club=club, competitions=competitions)

    @app.route('/pointsBoard', methods=['GET'])
    def pointsBoard():
        return render_template('points_board.html', clubs=clubs)

    @app.route('/logout')
    def logout():
        return redirect(url_for('index'))

    @app.errorhandler(400)
    def bad_request():
        return render_template("exception.html"), 400

    return app