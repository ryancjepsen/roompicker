from __future__ import print_function
import pandas as pd
from flask import Flask, render_template, request
from src.algo import roompicker
from wtforms import Form
from wtforms import StringField, IntegerField

app = Flask(__name__)

# start off with no exceptions
app.config['ROOMPICKER_EXCEPTION'] = ""

# create the form for entering bids
class BidForm(Form):
    # should verify that this is a y or an n TODO
    bid_bool = StringField('bool_choose')
    room_choice = IntegerField('room num')
    rent_choice = IntegerField('rent')

# this needs to be filled in by a form TODO
rp = roompicker.RoomPicker(roommates=['drew', 'casey', 'jepsen', 'joe', 'chris'], total_rent=4500)

@app.route('/', methods=['GET', 'POST'])
def hello_world():
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
    return render_template('index.html', form=bidform,
                           html_data=rp.rooms_df.to_html(),
                           whos_up=rp.roommates[rp.turn],
                           myexcept = app.config['ROOMPICKER_EXCEPTION'])
