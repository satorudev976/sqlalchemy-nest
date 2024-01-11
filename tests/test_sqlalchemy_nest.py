import pytest
from datetime import date
from tests.models import Branch, DateRange, Leaf, Node, RegistrationCard, Reservation, Root
    

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
    
    expect_reservation = Reservation(
        id=1,
        start_date=date(2024, 1, 1),
        end_date=date(2024, 1, 2),
        registration_card=RegistrationCard(
            id=1,
            guest_name='Jon',
            reservation_id=1
            )
        )
    
    @pytest.fixture(autouse=True, scope="function")
    def setup(self, session):
        yield
        
        #remove test data
        with session() as session:
            reservation: Reservation = session.query(Reservation).filter(Reservation.id == 1).first()
            session.delete(reservation)
            session.commit()

    @pytest.mark.parametrize(
        "reservation",
        [
            pytest.param({
                'start_date': date(2024, 1, 1),
                'end_date': date(2024, 1, 2),
                'registration_card': {
                    'guest_name': 'Jon'
                }
            }),
            # not hasattr (is_vip)
            pytest.param({
                'is_vip': True,
                'start_date': date(2024, 1, 1),
                'end_date': date(2024, 1, 2),
                'registration_card': {
                    'guest_name': 'Jon'
                }
            }),
            # composit (date_range)
            pytest.param({
                'date_range': {
                    'start': date(2024, 1, 1),
                    'end': date(2024, 1, 2),
                },
                'registration_card': {
                    'guest_name': 'Jon'
                }
            })
        ],
    )
    def test_one_to_one_by_dict(self, reservation, session):
        with session() as session:
            session.add(Reservation(**reservation))
            session.commit()
            new_reservation: Reservation = session.query(Reservation).filter(Reservation.id == 1).first()
                    
            assert new_reservation == TestOneToOne.expect_reservation
    
    
    @pytest.mark.parametrize(
        "reservation",
        [
            pytest.param(Reservation(
                start_date=date(2024, 1, 1),
                end_date=date(2024, 1, 2),
                registration_card=RegistrationCard(
                    guest_name='Jon'
                )
            )),
            # composit (date_range)
            pytest.param(Reservation(
                date_range=DateRange(
                    start=date(2024, 1, 1), 
                    end=date(2024, 1, 2)
                ),
                registration_card=RegistrationCard(
                    guest_name='Jon'
                )
            ))
            
        ]
    )
    def test_one_to_one_by_model(self, reservation, session): 
        with session() as session:
            session.add(reservation)
            session.commit()
            new_reservation: Reservation = session.query(Reservation).filter(Reservation.id == 1).first()
            
            assert new_reservation == TestOneToOne.expect_reservation
