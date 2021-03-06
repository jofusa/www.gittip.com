from faker import Factory
from gittip import orm
from gittip.models.tip import Tip
from gittip.models.participant import Participant
from gittip.models.elsewhere import Elsewhere
from gittip import AMOUNTS
import string
import random

faker = Factory.create()

platforms = ['github', 'twitter']


def fake_text_id(size=6, chars=string.ascii_lowercase + string.digits):
    """
    Create a random text id
    """
    return ''.join(random.choice(chars) for x in range(size))


def fake_balance(max_amount=100):
    """
    Return a random amount between 0 and max_amount
    """
    return random.random() * max_amount

def fake_int_id(nmax=2 ** 31 -1):
    """
    Create a random int id
    """
    return random.randint(0, nmax)


def fake_participant(is_admin=False, anonymous=False):
    """
    Create a fake User
    """
    return Participant(
        id=faker.firstName() + fake_text_id(3),
        statement=faker.sentence(),
        ctime=faker.dateTimeThisYear(),
        is_admin=is_admin,
        balance=fake_balance(),
        anonymous=anonymous,
        goal=fake_balance(),
        balanced_account_uri=faker.uri(),
        last_ach_result='',
        is_suspicious=False,
        last_bill_result='',  # Needed to not be suspicious
        claimed_time=faker.dateTimeThisYear()
    )


def fake_tip(tipper, tippee):
    """
    Create a fake tip
    """
    return Tip(
        id=fake_int_id(),
        ctime=faker.dateTimeThisYear(),
        mtime=faker.dateTimeThisMonth(),
        tipper=tipper.id,
        tippee=tippee.id,
        amount=random.choice(AMOUNTS)
    )


def fake_elsewhere(participant, platform=None):
    """
    Create a fake elsewhere
    """
    if platform is None:
        platform = random.choice(platforms)

    return Elsewhere(
        id=fake_int_id(),
        platform=platform,
        user_id=fake_text_id(),
        is_locked=False,
        participant_id=participant.id,
        user_info=''
    )


def populate_db(session, num_participants=100, num_tips=50):
    """
    Populate DB with fake data
    """
    #Make the participants
    participants = []
    for i in xrange(num_participants):
        p = fake_participant()
        session.add(p)
        participants.append(p)

    #Make the "Elsewhere's"
    for p in participants:
        #All participants get 1 or 2 elsewheres
        num_elsewheres = random.randint(1, 2)
        for platform_name in platforms[:num_elsewheres]:
            e = fake_elsewhere(p, platform_name)
            session.add(e)

    #Make the tips
    tips = []
    for i in xrange(num_tips):
        tipper, tippee = random.sample(participants, 2)
        t = fake_tip(tipper, tippee)
        tips.append(t)
        session.add(t)
    session.commit()


def main():
    db = orm.db
    dbsession = db.session
    populate_db(dbsession)

if __name__ == '__main__':
    main()
