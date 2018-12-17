""" The service for a Folf application."""

import calendar
import time
from .firebaseConfig import config
from pyrebase import pyrebase
from datetime import datetime


class Firebase:
    """ The Application Programming Interface for the Firebase database
    back-end services. The class expands pyrebase library for Firebase."""

    def __init__(self):
        """ The class constructor."""
        self.firebase = pyrebase.initialize_app(config)
        self.db = self.firebase.database()
        self.auth = self.firebase.auth()
        self.store = self.firebase.storage()

    def __get_all_users__(self):
        """ Returns a list of all users in the database."""
        values = self.db.child('Users').get()
        return dict(values.val())

    def __get_top_players_at_course__(self, location, course, many):
        """ Returns a list of top ten players and there score in desc order."""
        topPlayers = []
        # retList = []
        # names = set()
        try:
            # Get all games in the database.
            values = dict((self.db.child('Games').get()).val())
        except:
            # If exception occurse when trying to fetch data then return an
            # empty list.
            return topPlayers
        else:
            # For all played games.
            for v in values:
                try:
                    # If the game location and course match requried course.
                    if values[v][location][course]:
                        times = values[v][location][course]
                        # For all date times played.
                        for tme in times:
                            players = times[tme]
                            # For all the players that played that round.
                            for player in players:
                                colors = players[player]
                                # For all the course level that player played
                                # that round.
                                for color in colors:
                                    # Sum that round up to get the total
                                    # throws.
                                    game = sum(
                                        [x for x in colors[
                                            color] if x is not None])
                                    # Append the user and his total throws
                                    # to an list as a tuple.
                                    topPlayers.append((player, game))
                except KeyError:
                    # If location or course cant be found then throw KeyError.
                    return topPlayers
            # Sort the list with all played games at given course by it's
            # total throws and reverse the list. So all the most throws are in
            # the start.

            # Next change the list to dictionary.
            # That way we get only the lowest throws from each user
            # played once.
            topPlayers = dict(sorted(topPlayers, reverse=True,
                                     key=lambda x: x[1])).items()
            # Change the dictionary back to list and sort by it's lowest
            # throws first. and take n many players.
            return sorted(topPlayers, key=lambda x: x[1])[:many]

    def get_top_players_at_course(self, location, course, many):
        """ Returns a list of top ten players and there score in desc order."""
        return {
            "Location": location,
            "Course": course,
            "Players": self.__get_top_players_at_course__(
                location, course, many)
        }

    def add_user(self, userModel):
        """ Add user to the system."""
        try:
            # Add user to the authentication service.
            user = self.auth.create_user_with_email_and_password(
                userModel['email'], userModel['password'])
        except:
            return False
        else:
            # Add user email and name to the database.
            self.db.child('Users/' + user['localId']).set({
                "Name": userModel['name'],
                "Email": userModel['email'],
            })
            return user

    def sign_in_user(self, email, password):
        """ Sign in user to the system."""
        try:
            user = self.auth.sign_in_with_email_and_password(email, password)
            return user
        except:
            return False

    def verify_mail(self, email):
        """ Sends verifycation email."""
        try:
            return self.auth.send_email_verification(email)
        except:
            return False

    def reset_password(self, email):
        """ Sends email to user to reset his password."""
        try:
            self.auth.send_password_reset_email(email)
            return True
        except:
            return False

    def get_rules(self):
        """ Return rules in a text."""
        return (self.db.child('Rules').get()).val()

    def get_all_locations_and_courses(self):
        """ Return all course locations."""
        return dict((self.db.child('Locations').get()).val())

    def get_course_info(self, location, course):
        """ Returns a course at given location and place.."""
        values = (self.db.child('Locations/' +
                                location + '/' + course).get()).val()
        basketColors = list(values['Baskets'].keys())
        courseInfo = dict()
        courseInfo['Location'] = location
        courseInfo['Course'] = course
        courseInfo['BasketColors'] = basketColors
        courseInfo['Info'] = values['Info']
        courseInfo['Map'] = values['Map']
        return courseInfo

    def get_course_details(self, location, course, color):
        """ Return detailed course."""
        values = (self.db.child('Locations/' +
                                location + '/' + course).get()).val()
        baskets = [c for c in list(values['Baskets'].values())[
            0] if c is not None]
        couresInfo = dict()
        couresInfo['Location'] = location
        couresInfo['Course'] = course
        couresInfo['BasketColor'] = color
        couresInfo['Baskets'] = baskets
        couresInfo['Info'] = values['Info']
        couresInfo['Map'] = values['Map']
        return couresInfo

    def add_game_to_user(self, game):
        """ Add game to players record."""
        # Get list of course pars for played game.
        coursePar = [x['Par'] for x in (self.get_course_details(game[
            'location'], game['course'], game['color']))['Baskets']]
        # If the played didnt play that lane. That is submited 0 throws.
        # Then replace  0 with double par at that lane.
        for i in range(1, len(game['game'])):
            if game['game'][i] == 0:
                game['game'][i] = (coursePar[i - 1] * 2)
        date = str(calendar.timegm(time.gmtime()))
        #  make a dict of lane number and the user throws.
        game_score = dict(list(zip(range(len(game['game'])), game['game']))[
                          1:len(game['game'])])
        # Add the score to the database.
        try:
            self.db.child('Games/' + game['uId'] + '/' + game[
                'location'] + '/' + game['course'] + '/' + date + '/' + game[
                    'game'][0]).set({game['color']: game_score})
            return True
        except:
            return False

    def get_all_games_by_uId(self, uId):
        """ Return dict of all games by given user."""
        # Get all the games given user have played.
        values = (self.db.child('Games/' + str(uId)).get()).val()
        coursesList = []
        # If the user has never played a game then return empty list.
        if values is None:
            return coursesList
        # For all the locations.
        for l in values:
            location = values[l]
            # For all the courses.
            for c in location:
                course = location[c]
                for date in course:
                    # For all the dates.
                    players = course[date]
                    # For all the players that played that day with the user.
                    for player in players:
                        games = players[player]
                        coursesList.append({
                            "Location": l,
                            "Course": c,
                            "Player": player,
                            "Date": str(datetime.fromtimestamp(
                                int(date)).isoformat()).replace('T', ' '),
                            "Games": games,
                            # Sum upp the total throws.
                            "Total": sum([x for x in list(games.values())[
                                0] if x is not None])
                        })
        return coursesList

    def get_user_by_uId(self, uId):
        if uId is None:
            return None
        return (self.db.child('Users/' + uId).get()).val()
