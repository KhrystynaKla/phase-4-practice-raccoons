#!/usr/bin/env python3

from app import app
from models import db, Raccoon, Trashcan, Visit
from faker import Faker
import random

faker = Faker()

if __name__ == '__main__':
    with app.app_context():
        print("Seeding database...")

        print("Removing old data...")

        Visit.query.delete()
        Raccoon.query.delete()
        Trashcan.query.delete()

        print("Creating raccoons...")

        raccoons_list = []

        for _ in range(10):
            r = Raccoon( name=faker.name(), age=random.randint(1,20) )
            raccoons_list.append(r)

        db.session.add_all(raccoons_list)
        db.session.commit()

        print("Creating trashcans...")

        trashcans_list = []

        for _ in range(10):
            tc = Trashcan( address=faker.address() )
            trashcans_list.append(tc)

        db.session.add_all(trashcans_list)
        db.session.commit()

        print("Creating visits...")

        visits_list = []

        for _ in range(20):
            v = Visit( 
                raccoon=random.choice(raccoons_list),
                trashcan=random.choice(trashcans_list),
                date=str(faker.date_between(start_date='-10y', end_date='today'))
            )
            visits_list.append(v)

        db.session.add_all(visits_list)
        db.session.commit()

        print("Seeding complete!")