from __future__ import print_function
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for
from src.algo import roompicker
from wtforms import Form
from wtforms import StringField, IntegerField

app = Flask(__name__)

# start off with no exceptions
app.config['ROOMPICKER_EXCEPTION'] = ""

class RoommatesForm(Form):
    roommates = StringField('Roommates')
    total_rent = IntegerField('Total Rent')

# create the form for entering bids
class BidForm(Form):
    # should verify that this is a y or an n TODO
    bid_bool = StringField('bool_choose')
    room_choice = IntegerField('room num')
    rent_choice = IntegerField('rent')

rp = roompicker.RoomPicker()

@app.route('/', methods=['GET', 'POST'])
def start():
    roommates_form = RoommatesForm(request.form)

    if request.method == 'POST':
        roommates = str(roommates_form.roommates.data).split(",")
        total_rent = int(roommates_form.total_rent.data)
        rp.init(roommates, total_rent)
        return redirect(url_for('pick_rooms'))

    return render_template('start.html', form=roommates_form)

@app.route('/roompicker', methods=['GET', 'POST'])
def pick_rooms():
    # get the BidForm defined above
    bidform = BidForm(request.form)
    # if you hit go
    if request.method == 'POST':
        # and you chose "y" as bid_bool
        if bidform.bid_bool.data == 'y':
            # try to run the algo and reset the exception
            try:
                rp.run_algo(in_room_number=bidform.room_choice.data, in_bid=bidform.rent_choice.data)
                app.config['ROOMPICKER_EXCEPTION'] = ""
            # if it errors, set the exception so it can be printed to the page
            except Exception as e:
                app.config['ROOMPICKER_EXCEPTION'] = e
        # if you chose not to bid, pass that on to the algo
        else:
            # increment counter
            rp.pass_dude()
    # render the page
    return render_template('roompicker.html', form=bidform,
                           html_data=rp.rooms_df.to_html(),
                           whos_up=rp.roommates[rp.turn],
                           myexcept = app.config['ROOMPICKER_EXCEPTION'])
