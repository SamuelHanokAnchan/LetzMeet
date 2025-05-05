# app.py
from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from datetime import datetime, date, timedelta
import json
import calendar

app = Flask(__name__)
app.secret_key = os.urandom(24)  # For flash messages and session

# Database (simple JSON file for storage)
DATA_FILE = 'availability_data.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            data = json.load(f)
            
            # Migration: Update old data format to new format
            if 'users' in data:
                for user in data['users']:
                    # Check for old format users (without 'days' field)
                    if 'days' not in user and 'day' in user:
                        # Convert old format to new format
                        user['days'] = [{
                            'day': user['day'],
                            'start_time': user.get('start_time', '00:00'),
                            'end_time': user.get('end_time', '23:59'),
                            'full_day': user.get('full_day', False)
                        }]
                        
                        # Set default week if missing
                        if 'week' not in user:
                            user['week'] = 'current'
                        
                        # Remove old fields
                        if 'day' in user:
                            del user['day']
                        if 'start_time' in user:
                            del user['start_time']
                        if 'end_time' in user:
                            del user['end_time']
                        if 'full_day' in user and 'days' in user:
                            del user['full_day']
            
            return data
    else:
        return {'users': []}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

def time_to_minutes(time_str):
    """Convert time string (HH:MM) to minutes since midnight"""
    time_obj = datetime.strptime(time_str, '%H:%M')
    return time_obj.hour * 60 + time_obj.minute

def minutes_to_time(minutes):
    """Convert minutes since midnight to time string (HH:MM)"""
    hours = minutes // 60
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"

def get_date_for_day(day, week):
    """Calculate the date for a given day and week"""
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    today = date.today()
    
    # Find the date of the specified day in the current week
    today_weekday = today.weekday()  # Monday is 0
    day_index = days.index(day)
    
    days_diff = day_index - today_weekday
    if days_diff < 0:  # If the day is earlier in the week than today
        days_diff += 7
    
    target_date = today + timedelta(days=days_diff)
    
    # Adjust for selected week
    if week == "next":
        target_date += timedelta(days=7)
    elif week == "after_next":
        target_date += timedelta(days=14)
    
    return target_date

def calculate_overlaps():
    data = load_data()
    users = data['users']
    
    if not users:
        return {}, None
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weeks = ["current", "next", "after_next"]
    
    # Create a structure to hold all possible day-week combinations
    overlaps = {}
    for week in weeks:
        overlaps[week] = {day: [] for day in days}
    
    # Get unique names for checking if everyone is available at the same time
    all_user_names = set(user['name'] for user in users)
    meetup_slot = None
    
    # Process each user's availability
    for week in weeks:
        for day in days:
            # Find all availabilities for this specific day and week
            day_availabilities = []
            for user in users:
                # Make sure user has days field
                if 'days' not in user:
                    continue
                    
                for day_info in user['days']:
                    if day_info['day'] == day and user['week'] == week:
                        day_availabilities.append({
                            'name': user['name'],
                            'start_time': day_info['start_time'],
                            'end_time': day_info['end_time']
                        })
            
            if len(day_availabilities) < 2:
                continue  # Need at least 2 users to have an overlap
            
            # Find the latest start time and earliest end time
            start_times = [time_to_minutes(avail['start_time']) for avail in day_availabilities]
            end_times = [time_to_minutes(avail['end_time']) for avail in day_availabilities]
            
            latest_start = max(start_times)
            earliest_end = min(end_times)
            
            if latest_start < earliest_end:
                names_present = set(avail['name'] for avail in day_availabilities)
                
                overlap_slot = {
                    'start': minutes_to_time(latest_start),
                    'end': minutes_to_time(earliest_end),
                    'users': [avail['name'] for avail in day_availabilities]
                }
                
                overlaps[week][day].append(overlap_slot)
                
                # Check if all users are available (for the meetup date feature)
                if names_present == all_user_names and len(names_present) >= 2 and not meetup_slot:
                    target_date = get_date_for_day(day, week)
                    
                    meetup_slot = {
                        'day': day,
                        'week': week,
                        'week_name': "Current Week" if week == "current" else "Next Week" if week == "next" else "Week After Next",
                        'date': target_date.strftime('%Y-%m-%d'),
                        'date_formatted': target_date.strftime('%B %d, %Y'),
                        'start': minutes_to_time(latest_start),
                        'end': minutes_to_time(earliest_end)
                    }
    
    return overlaps, meetup_slot

@app.route('/')
def index():
    data = load_data()
    overlaps, meetup_slot = calculate_overlaps()
    return render_template('index.html', 
                          users=data['users'], 
                          overlaps=overlaps, 
                          meetup_slot=meetup_slot,
                          time_to_minutes=time_to_minutes)  # Pass function to template

@app.route('/add', methods=['POST'])
def add_availability():
    name = request.form.get('name')
    week = request.form.get('week')
    days = request.form.getlist('days')  # Get multiple days
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    full_day = request.form.get('full_day') == 'on'
    
    # Basic validation
    if not name or not week or not days:
        flash('Name, week, and at least one day are required!', 'error')
        return redirect(url_for('index'))
    
    # If full day is checked, set times to full day
    if full_day:
        start_time = '00:00'
        end_time = '23:59'
    elif not start_time or not end_time:
        flash('Please provide both start and end times or check "Full Day" option!', 'error')
        return redirect(url_for('index'))
    # Check if start time is before end time when not full day
    elif time_to_minutes(start_time) >= time_to_minutes(end_time):
        flash('Start time must be before end time!', 'error')
        return redirect(url_for('index'))
    
    # Add user availability
    data = load_data()
    
    # Check if user already exists
    user_exists = False
    for user in data['users']:
        if user['name'] == name and user['week'] == week:
            # Make sure user has days field
            if 'days' not in user:
                user['days'] = []
                
            # Add days to existing user
            for day in days:
                # Check if day already exists
                day_exists = False
                for day_info in user['days']:
                    if day_info['day'] == day:
                        day_exists = True
                        flash(f'You already added {day} for {name} in {week}!', 'error')
                        break
                
                if not day_exists:
                    user['days'].append({
                        'day': day,
                        'start_time': start_time,
                        'end_time': end_time,
                        'full_day': full_day
                    })
            
            user_exists = True
            break
    
    if not user_exists:
        # Create new user entry
        days_info = []
        for day in days:
            days_info.append({
                'day': day,
                'start_time': start_time,
                'end_time': end_time,
                'full_day': full_day
            })
        
        data['users'].append({
            'name': name,
            'week': week,
            'days': days_info
        })
    
    save_data(data)
    
    flash('Availability added successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/remove/<int:user_index>', methods=['POST'])
def remove_entry(user_index):
    data = load_data()
    
    # Check if the index is valid
    if 0 <= user_index < len(data['users']):
        removed_user = data['users'][user_index]['name']
        data['users'].pop(user_index)
        save_data(data)
        flash(f'Entry for {removed_user} removed successfully!', 'success')
    else:
        flash('Invalid entry!', 'error')
    
    return redirect(url_for('index'))

@app.route('/clear', methods=['POST'])
def clear_data():
    save_data({'users': []})
    flash('All data cleared!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)