import pytest
from datetime import date
from test.models import Base, Branch, DateRange, Leaf, Node, RegistrationCard, Reservation, Root
    

class TestOneToMany:
    @pytest.fixture(autouse=True, scope="function")
    def setup(self, session):
        yield
        
        # remove test data
        with session() as session:
            root: Root = session.query(Root).filter(Root.id == 1).first()
            session.delete(root)
            session.commit()
        
    
    def test_one_to_many_by_dict(self, session):
        root = {
            'name': 'root',
            'branches': [
                {
                    'name': 'branch',
                    'nodes': [
                        {
                            'name': 'node',
                            'leaves': [
                                {
                                    'name': 'leaf_1'
                                },
                                {
                                    'name': 'leaf_2'
                                },
                            ]
                        }
                    ]
                },
            ] 
        }
        
        with session() as session:
            session.add(Root(**root))
            session.commit()
            new_root: Root = session.query(Root).filter(Root.id == 1).first()
            
            assert new_root.id == 1
            assert new_root.name == 'root'
            assert len(new_root.branches) == 1
            assert new_root.branches[0].id == 1
            assert new_root.branches[0].name =='branch'
            assert new_root.branches[0].root_id == new_root.id
            assert len(new_root.branches[0].nodes) == 1
            assert new_root.branches[0].nodes[0].name == 'node'
            assert len(new_root.branches[0].nodes[0].leaves) == 2
            assert new_root.branches[0].nodes[0].leaves[0].name == 'leaf_1'
            assert new_root.branches[0].nodes[0].leaves[1].name == 'leaf_2'
        
                
    def test_one_to_many_by_model(self, session):
        root = Root(name='root', branches=[
            Branch(name='branch', nodes=[
                Node(name='node', leaves=[
                    Leaf(name='leaf_1'),
                    Leaf(name='leaf_2'),
                ])
            ])
        ])
        with session() as session:
            session.add(root)
            session.commit()
            new_root: Root = session.query(Root).filter(Root.id == 1).first()
            
            assert new_root.id == 1
            assert new_root.name == 'root'
            assert len(new_root.branches) == 1
            assert new_root.branches[0].id == 1
            assert new_root.branches[0].name =='branch'
            assert new_root.branches[0].root_id == new_root.id
            assert len(new_root.branches[0].nodes) == 1
            assert new_root.branches[0].nodes[0].name == 'node'
            assert len(new_root.branches[0].nodes[0].leaves) == 2
            assert new_root.branches[0].nodes[0].leaves[0].name == 'leaf_1'
            assert new_root.branches[0].nodes[0].leaves[1].name == 'leaf_2'

class TestOneToOne:
    
    @pytest.fixture(autouse=True, scope="function")
    def setup(self, session):
        yield
        
        #remove test data
        with session() as session:
            reservation: Reservation = session.query(Reservation).filter(Reservation.id == 1).first()
            session.delete(reservation)
            session.commit()
        
    def test_one_to_one_by_model(self, session):
        reservation = {
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 1, 2),
            'registration_card': {
                'guest_name': 'Jon'
            }
        }
        
        with session() as session:
            session.add(Reservation(**reservation))
            session.commit()
            new_reservation: Reservation = session.query(Reservation).filter(Reservation.id == 1).first()
            
            assert new_reservation.id == 1
            assert new_reservation.start_date == date(2024, 1, 1)
            assert new_reservation.end_date == date(2024, 1, 2)
            assert new_reservation.registration_card.id == 1
            assert new_reservation.registration_card.reservation_id == new_reservation.id
            assert new_reservation.registration_card.guest_name == 'Jon'

    def test_one_to_one_by_model(self, session):
        reservation = Reservation(
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 2),
            registration_card=RegistrationCard(
                guest_name='Jon'
            )
        )
        
        with session() as session:
            session.add(reservation)
            session.commit()
            new_reservation: Reservation = session.query(Reservation).filter(Reservation.id == 1).first()
            
            assert new_reservation.id == 1
            assert new_reservation.start_date == date(2024, 1, 1)
            assert new_reservation.end_date == date(2024, 1, 2)
            assert new_reservation.registration_card.id == 1
            assert new_reservation.registration_card.reservation_id == new_reservation.id
            assert new_reservation.registration_card.guest_name == 'Jon'

class TestCompositeType:
    
    @pytest.fixture(autouse=True, scope="function")
    def setup(self, session):
        yield
        
        #remove test data
        with session() as session:
            reservation: Reservation = session.query(Reservation).filter(Reservation.id == 1).first()
            session.delete(reservation)
            session.commit()
    
    def test_composite_by_dict(self, session):
        reservation = {
            'date_range': {
                'start': date(2024, 1, 1),
                'end': date(2024, 1, 2),
            },
            'registration_card': {
                'guest_name': 'Jon'
            }
        }
        
        with session() as session:
            session.add(Reservation(**reservation))
            session.commit()
            new_reservation: Reservation = session.query(Reservation).filter(Reservation.id == 1).first()
            
            assert new_reservation.id == 1
            assert new_reservation.start_date == date(2024, 1, 1)
            assert new_reservation.end_date == date(2024, 1, 2)
            assert new_reservation.date_range == DateRange(start=date(2024, 1, 1), end=date(2024, 1, 2))
            assert new_reservation.registration_card.id == 1
            assert new_reservation.registration_card.reservation_id == new_reservation.id
            assert new_reservation.registration_card.guest_name == 'Jon'

    def test_composite_by_model(self, session):
        reservation = Reservation(
            date_range=DateRange(start=date(2024, 1, 1), end=date(2024, 1, 2)),
            registration_card=RegistrationCard(
                guest_name='Jon'
            )
        )
        
        with session() as session:
            session.add(reservation)
            session.commit()
            new_reservation: Reservation = session.query(Reservation).filter(Reservation.id == 1).first()
            
            assert new_reservation.id == 1
            assert new_reservation.start_date == date(2024, 1, 1)
            assert new_reservation.end_date == date(2024, 1, 2)
            assert new_reservation.date_range == DateRange(start=date(2024, 1, 1), end=date(2024, 1, 2))
            assert new_reservation.registration_card.id == 1
            assert new_reservation.registration_card.reservation_id == new_reservation.id
            assert new_reservation.registration_card.guest_name == 'Jon'

class TestNotHasAttr:
    
    @pytest.fixture(autouse=True, scope="function")
    def setup(self, session):
        yield
        
        #remove test data
        with session() as session:
            reservation: Reservation = session.query(Reservation).filter(Reservation.id == 1).first()
            session.delete(reservation)
            session.commit()
            
    def test_not_hasattr_by_dict(self, session):
        reservation = {
            'is_vip': True,
            'start_date': date(2024, 1, 1),
            'end_date': date(2024, 1, 2),
            'registration_card': {
                'guest_name': 'Jon'
            }
        }
        
        with session() as session:
            session.add(Reservation(**reservation))
            session.commit()
            new_reservation: Reservation = session.query(Reservation).filter(Reservation.id == 1).first()
            
            assert new_reservation.id == 1
            assert new_reservation.start_date == date(2024, 1, 1)
            assert new_reservation.end_date == date(2024, 1, 2)
            assert new_reservation.registration_card.id == 1
            assert new_reservation.registration_card.reservation_id == new_reservation.id
            assert new_reservation.registration_card.guest_name == 'Jon'
