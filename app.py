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
            return json.load(f)
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

def calculate_overlaps():
    data = load_data()
    users = data['users']
    
    if not users:
        return {}, None
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    overlaps = {day: [] for day in days}
    
    # Get unique names for checking if everyone is available at the same time
    all_user_names = set(user['name'] for user in users)
    meetup_slot = None
    
    for day in days:
        users_on_day = [user for user in users if user['day'] == day]
        
        if len(users_on_day) < 2:
            continue  # Need at least 2 users to have an overlap
        
        # Find the latest start time and earliest end time among all users for this day
        start_times = [time_to_minutes(user['start_time']) for user in users_on_day]
        end_times = [time_to_minutes(user['end_time']) for user in users_on_day]
        
        latest_start = max(start_times)
        earliest_end = min(end_times)
        
        if latest_start < earliest_end:
            names_present = set(user['name'] for user in users_on_day)
            
            overlap_slot = {
                'start': minutes_to_time(latest_start),
                'end': minutes_to_time(earliest_end),
                'users': [user['name'] for user in users_on_day]
            }
            
            overlaps[day].append(overlap_slot)
            
            # Check if all users are available (for the meetup date feature)
            if names_present == all_user_names and len(names_present) >= 2 and not meetup_slot:
                # Get the current date and find next occurrence of this day
                today = date.today()
                today_day = today.weekday()  # Monday is 0
                day_index = days.index(day)
                
                days_until = (day_index - today_day) % 7
                # Create the next occurrence date correctly
                next_occurrence = today + timedelta(days=days_until)
                
                meetup_slot = {
                    'day': day,
                    'date': next_occurrence.strftime('%Y-%m-%d'),
                    'date_formatted': next_occurrence.strftime('%B %d, %Y'),
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
    day = request.form.get('day')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    full_day = request.form.get('full_day') == 'on'
    
    # Basic validation
    if not name or not day:
        flash('Name and day are required!', 'error')
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
    data['users'].append({
        'name': name,
        'day': day,
        'start_time': start_time,
        'end_time': end_time,
        'full_day': full_day
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