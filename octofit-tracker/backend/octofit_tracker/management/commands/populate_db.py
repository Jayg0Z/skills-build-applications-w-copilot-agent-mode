import json
import os
from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout

class Command(BaseCommand):
    help = 'Populate the database with test data'

    def handle(self, *args, **kwargs):
        # Correct the file path
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        test_data_path = os.path.join(base_dir, 'test_data.json')
        self.stdout.write(f"Resolved file path: {test_data_path}")

        with open(test_data_path, 'r') as file:
            data = json.load(file)

        # Populate users
        users = {}
        for user_data in data['users']:
            user = User.objects.create(**user_data)
            users[user_data['email']] = user

        # Populate teams
        for team_data in data['teams']:
            members = [users[email] for email in team_data.pop('members')]
            team = Team.objects.create(**team_data)
            team.members.set(members)

        # Populate activities
        for activity_data in data['activities']:
            activity_data['user'] = users[activity_data['user']]
            Activity.objects.create(**activity_data)

        # Populate leaderboard
        for leaderboard_data in data['leaderboard']:
            leaderboard_data['team'] = Team.objects.get(name=leaderboard_data['team'])
            Leaderboard.objects.create(**leaderboard_data)

        # Populate workouts
        for workout_data in data['workouts']:
            Workout.objects.create(**workout_data)

        self.stdout.write(self.style.SUCCESS('Database populated with test data.'))
