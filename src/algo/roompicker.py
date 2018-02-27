import random
import pandas as pd

class RoomPicker(object):

    def __init__(self, roommates, total_rent):
        self.roommates = roommates
        random.shuffle(self.roommates)
        self.total_rent = total_rent
        indiv_rent = total_rent / len(self.roommates)
        rooms_list = [[room_num + 1, roommate, indiv_rent] for room_num, roommate in enumerate(self.roommates)]
        self.rooms_df = pd.DataFrame(rooms_list, columns=["room_number", "roommate", "rent"]).set_index("room_number")
        self.turn = 0
        self.pass_count = 0

    def get_room_number(self, roommate):
        return self.rooms_df[self.rooms_df["roommate"] == roommate].index.values[0]

    def get_roommate(self, room_number):
        return self.rooms_df.loc[room_number, "roommate"]

    def get_rent_from_roommate(self, roommate):
        return self.rooms_df[self.rooms_df["roommate"] == roommate].iloc[0, 1]

    def get_rent_from_room_number(self, room_number):
        return self.rooms_df.loc[room_number, "rent"]

    def set_roommate_and_rent(self, room_number, roommate, rent):
        self.rooms_df.loc[room_number] = [roommate, rent]

    def pass_dude(self):
        self.pass_count += 1
        self.turn += 1

    def run_algo(self, in_room_number, in_bid):
        roommate = self.roommates[self.turn]
        old_room_number = self.get_room_number(roommate)
        if old_room_number == in_room_number:
            raise ValueError("Cannot choose room you already have! Try again.")
        elif in_room_number not in self.rooms_df.index.values:
            raise ValueError("Invalid room number! Try again.")
        else:
            current_rent = self.get_rent_from_room_number(in_room_number)
            if in_bid > current_rent:
                current_roommate = self.get_roommate(in_room_number)
                old_rent = self.get_rent_from_roommate(roommate)
                self.set_roommate_and_rent(old_room_number, current_roommate, old_rent)
                remaining_rent = self.total_rent - in_bid
                rent_multiplier = remaining_rent / (self.total_rent - current_rent)
                self.rooms_df["rent"] *= rent_multiplier
                self.set_roommate_and_rent(in_room_number, roommate, in_bid)
                self.rooms_df["rent"] = self.rooms_df["rent"].round()
                if self.turn == len(self.roommates) - 1:
                    self.turn = 0
                else:
                    self.turn += 1
            else:
                raise ValueError("Bid must be higher than existing rent price! Try again.")
