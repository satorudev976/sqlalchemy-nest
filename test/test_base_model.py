import pytest
from datetime import date

from test.models import Reservation, Root


class TestUpdateColumns:
    
    @pytest.fixture(autouse=True, scope="function")
    def setup(self, session):
        self.db_session = session
        with self.db_session() as session:
            reservation = {
                'start_date': date(2024, 1, 1),
                'end_date': date(2024, 1, 2),
            }
            session.add(Reservation(**reservation))
            session.commit()
        
        yield
        
        #remove test data
        with self.db_session() as session:
            reservation: Reservation = session.query(Reservation).filter(Reservation.id == 1).first()
            session.delete(reservation)
            session.commit()
    
    def test_update_columns(self, session):
        update_reservation = {
            'id': 1,
            'start_date': date(2024, 2, 1),
            'end_date': date(2024, 2, 2),
        }
        with session() as session:
            reservation: Reservation = session.query(Reservation).filter(Reservation.id == 1).first()
            reservation.merge(**update_reservation)
            session.commit()
            updated_reservation: Reservation = session.query(Reservation).filter(Reservation.id == 1).first()
            
            assert updated_reservation.id == 1
            assert updated_reservation.start_date == date(2024, 2, 1)
            assert updated_reservation.end_date == date(2024, 2, 2)
    
    def test_update_by_composit(self, session):
        update_reservation = {
            'id': 1,
            'date_range': {
                'start': date(2024, 2, 1),
                'end': date(2024, 2, 2),
            },
        }
        with session() as session:
            reservation: Reservation = session.query(Reservation).filter(Reservation.id == 1).first()
            reservation.merge(**update_reservation)
            session.commit()
            updated_reservation: Reservation = session.query(Reservation).filter(Reservation.id == 1).first()
            
            assert updated_reservation.id == 1
            assert updated_reservation.start_date == date(2024, 2, 1)
            assert updated_reservation.end_date == date(2024, 2, 2)
    
    def test_remove_columns(self, session):
        update_reservation = {
            'id': 1,
            'start_date': date(2024, 2, 1),
        }
        with session() as session:
            reservation: Reservation = session.query(Reservation).filter(Reservation.id == 1).first()
            reservation.merge(**update_reservation)
            session.commit()
            updated_reservation: Reservation = session.query(Reservation).filter(Reservation.id == 1).first()
            
            assert updated_reservation.id == 1
            assert updated_reservation.start_date == date(2024, 2, 1)
            assert updated_reservation.end_date == None
    
    def test_not_hasattr(self, session):
        update_reservation = {
            'id': 1,
            'is_vip': True,
            'start_date': date(2024, 2, 1),
            'end_date': date(2024, 2, 2),
        }
        
        with session() as session:
            reservation: Reservation = session.query(Reservation).filter(Reservation.id == 1).first()
            reservation.merge(**update_reservation)
            session.commit()
            updated_reservation: Reservation = session.query(Reservation).filter(Reservation.id == 1).first()
            
            assert updated_reservation.id == 1
            assert updated_reservation.start_date == date(2024, 2, 1)
            assert updated_reservation.end_date == date(2024, 2, 2)
    
    def test_add_one_to_one(self, session):
        update_reservation = {
            'id': 1,
            'start_date': date(2024, 2, 1),
            'end_date': date(2024, 2, 2),
            'registration_card': {
                'guest_name': 'Jon'
            }
        }
        with session() as session:
            reservation: Reservation = session.query(Reservation).filter(Reservation.id == 1).first()
            reservation.merge(**update_reservation)
            session.commit()
            updated_reservation: Reservation = session.query(Reservation).filter(Reservation.id == 1).first()
            
            assert updated_reservation.id == 1
            assert updated_reservation.start_date == date(2024, 2, 1)
            assert updated_reservation.end_date == date(2024, 2, 2)
            assert updated_reservation.registration_card.id == 1
            assert updated_reservation.registration_card.guest_name == 'Jon'

class TestOneToOne:

    @pytest.fixture(autouse=True, scope="function")
    def setup(self, session):
        self.db_session = session
        with self.db_session() as session:
            reservation = {
                'start_date': date(2024, 1, 1),
                'end_date': date(2024, 1, 2),
                'registration_card': {
                    'guest_name': 'Jon'
                }
            }
            session.add(Reservation(**reservation))
            session.commit()
        
        yield
        
        #remove test data
        with self.db_session() as session:
            reservation: Reservation = session.query(Reservation).filter(Reservation.id == 1).first()
            session.delete(reservation)
            session.commit()
    

    def test_update_one_to_one(self, session):
        update_reservation = {
            'id': 1,
            'start_date': date(2024, 2, 1),
            'end_date': date(2024, 2, 2),
            'registration_card': {
                'guest_name': 'Jon Smith',
            }
        }
        with session() as session:
            reservation: Reservation = session.query(Reservation).filter(Reservation.id == 1).first()
            reservation.merge(**update_reservation)
            session.commit()
            updated_reservation: Reservation = session.query(Reservation).filter(Reservation.id == 1).first()
            
            assert updated_reservation.id == 1
            assert updated_reservation.start_date == date(2024, 2, 1)
            assert updated_reservation.end_date == date(2024, 2, 2)
            assert updated_reservation.registration_card.guest_name == 'Jon Smith'
    
    def test_remove_one_to_one(self, session):
        update_reservation = {
            'id': 1,
            'start_date': date(2024, 2, 1),
            'end_date': date(2024, 2, 2),
        }
        with session() as session:
            reservation: Reservation = session.query(Reservation).filter(Reservation.id == 1).first()
            reservation.merge(**update_reservation)
            session.commit()
            updated_reservation: Reservation = session.query(Reservation).filter(Reservation.id == 1).first()
            
            assert updated_reservation.id == 1
            assert updated_reservation.start_date == date(2024, 2, 1)
            assert updated_reservation.end_date == date(2024, 2, 2)
            assert updated_reservation.registration_card == None

    def test_remove_by_composite(self, session):
        update_reservation = {
            'id': 1,
            'date_range': None
        }
        with session() as session:
            reservation: Reservation = session.query(Reservation).filter(Reservation.id == 1).first()
            reservation.merge(**update_reservation)
            session.commit()
            updated_reservation: Reservation = session.query(Reservation).filter(Reservation.id == 1).first()
            
            assert updated_reservation.id == 1
            assert updated_reservation.start_date == None
            assert updated_reservation.end_date == None
            assert updated_reservation.registration_card == None

class TestOneToMany:

    @pytest.fixture(autouse=True, scope="function")
    def setup(self, session):
        self.db_session = session
        with self.db_session() as session:
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
            
            session.add(Root(**root))
            session.commit()
        
        yield
        
        #remove test data
        with self.db_session() as session:
            root: Root = session.query(Root).filter(Root.id == 1).first()
            session.delete(root)
            session.commit()
    
    def test_update_one_to_many(self, session):
        updat_root = {
            'id': 1,
            'name': 'updated_root',
            'branches': [
                {
                    'id': 1,
                    'name': 'updated_branch',
                    'nodes': [
                        {
                            'id': 1,
                            'name': 'updated_node',
                            'leaves': [
                                {
                                    'id': 1,
                                    'name': 'updated_leaf_1'
                                },
                                {
                                    'id': 2,
                                    'name': 'updated_leaf_2'
                                },
                            ]
                        }
                    ]
                },
            ] 
        }
        
        with session() as session:
            root: Root = session.query(Root).filter(Root.id == 1).first()
            root.merge(**updat_root)
            session.commit()
            updated_root: Root = session.query(Root).filter(Root.id == 1).first()
            
            
            assert updated_root.id == 1
            assert updated_root.name == 'updated_root'
            assert len(updated_root.branches) == 1
            assert updated_root.branches[0].id == 1
            assert updated_root.branches[0].name =='updated_branch'
            assert updated_root.branches[0].root_id == updated_root.id
            assert len(updated_root.branches[0].nodes) == 1
            assert updated_root.branches[0].nodes[0].name == 'updated_node'
            assert len(updated_root.branches[0].nodes[0].leaves) == 2
            assert updated_root.branches[0].nodes[0].leaves[0].name == 'updated_leaf_1'
            assert updated_root.branches[0].nodes[0].leaves[1].name == 'updated_leaf_2'

    def test_add_only_children(self, session):
        updat_root = {
            'id': 1,
            'name': 'root',
            'branches': [
                {
                    'id': 1,
                    'name': 'branch',
                    'nodes': [
                        {
                            'id': 1,
                            'name': 'node',
                            'leaves': [
                                {
                                    'id': 1,
                                    'name': 'leaf_1'
                                },
                                {
                                    'id': 2,
                                    'name': 'leaf_2'
                                },
                                {
                                    'name': 'leaf_3'
                                }
                            ]
                        }
                    ]
                },
            ] 
        }
        
        with session() as session:
            root: Root = session.query(Root).filter(Root.id == 1).first()
            root.merge(**updat_root)
            session.commit()
            updated_root: Root = session.query(Root).filter(Root.id == 1).first()
            
            
            assert updated_root.id == 1
            assert updated_root.name == 'root'
            assert len(updated_root.branches) == 1
            assert updated_root.branches[0].id == 1
            assert updated_root.branches[0].name =='branch'
            assert updated_root.branches[0].root_id == updated_root.id
            assert len(updated_root.branches[0].nodes) == 1
            assert updated_root.branches[0].nodes[0].name == 'node'
            assert len(updated_root.branches[0].nodes[0].leaves) == 3
            assert updated_root.branches[0].nodes[0].leaves[0].name == 'leaf_1'
            assert updated_root.branches[0].nodes[0].leaves[1].name == 'leaf_2'
            assert updated_root.branches[0].nodes[0].leaves[2].name == 'leaf_3'

    def test_add_parent_and_child(self, session):
        updat_root = {
            'id': 1,
            'name': 'root',
            'branches': [
                {
                    'id': 1,
                    'name': 'branch',
                    'nodes': [
                        {
                            'id': 1,
                            'name': 'node',
                            'leaves': [
                                {
                                    'id': 1,
                                    'name': 'leaf_1'
                                },
                                {
                                    'id': 2,
                                    'name': 'leaf_2'
                                },
                            ]
                        }
                    ]
                },
                {
                    'name': 'added_branch',
                    'nodes': [
                        {
                            'name': 'added_node',
                            'leaves': [
                                {
                                    'name': 'added_leaf_1'
                                },
                            ]
                        }
                    ]
                },
            ] 
        }
        
        with session() as session:
            root: Root = session.query(Root).filter(Root.id == 1).first()
            root.merge(**updat_root)
            session.commit()
            updated_root: Root = session.query(Root).filter(Root.id == 1).first()
            
            
            assert updated_root.id == 1
            assert updated_root.name == 'root'
            assert len(updated_root.branches) == 2
            assert updated_root.branches[0].id == 1
            assert updated_root.branches[0].name =='branch'
            assert updated_root.branches[0].root_id == updated_root.id
            assert len(updated_root.branches[0].nodes) == 1
            assert len(updated_root.branches[1].nodes) == 1
            assert updated_root.branches[0].nodes[0].name == 'node'
            assert len(updated_root.branches[0].nodes[0].leaves) == 2
            assert len(updated_root.branches[1].nodes[0].leaves) == 1
            assert updated_root.branches[0].nodes[0].leaves[0].name == 'leaf_1'
            assert updated_root.branches[0].nodes[0].leaves[1].name == 'leaf_2'
            assert updated_root.branches[1].nodes[0].leaves[0].name == 'added_leaf_1'

    def test_remove_only_children(self, session):
        updat_root = {
            'id': 1,
            'name': 'root',
            'branches': [
                {
                    'id': 1,
                    'name': 'branch',
                    'nodes': [
                        {
                            'id': 1,
                            'name': 'node',
                            'leaves': [
                                {
                                    'id': 1,
                                    'name': 'leaf_1'
                                },
                            ]
                        }
                    ]
                },
            ] 
        }
        
        with session() as session:
            root: Root = session.query(Root).filter(Root.id == 1).first()
            root.merge(**updat_root)
            session.commit()
            updated_root: Root = session.query(Root).filter(Root.id == 1).first()
            
            
            assert updated_root.id == 1
            assert updated_root.name == 'root'
            assert len(updated_root.branches) == 1
            assert updated_root.branches[0].id == 1
            assert updated_root.branches[0].name =='branch'
            assert updated_root.branches[0].root_id == updated_root.id
            assert len(updated_root.branches[0].nodes) == 1
            assert updated_root.branches[0].nodes[0].name == 'node'
            assert len(updated_root.branches[0].nodes[0].leaves) == 1
            assert updated_root.branches[0].nodes[0].leaves[0].name == 'leaf_1'

    def test_remove_parent_and_children(self, session):
        updat_root = {
            'id': 1,
            'name': 'root',
            'branches': [
                {
                    'id': 1,
                    'name': 'branch',
                },
            ] 
        }
        
        with session() as session:
            root: Root = session.query(Root).filter(Root.id == 1).first()
            root.merge(**updat_root)
            session.commit()
            updated_root: Root = session.query(Root).filter(Root.id == 1).first()
            
            
            assert updated_root.id == 1
            assert updated_root.name == 'root'
            assert len(updated_root.branches) == 1
            assert updated_root.branches[0].id == 1
            assert updated_root.branches[0].name =='branch'
            assert updated_root.branches[0].root_id == updated_root.id
            assert len(updated_root.branches[0].nodes) == 0
            assert updated_root.branches[0].nodes == []

class TestCreateOneToMany:

    @pytest.fixture(autouse=True, scope="function")
    def setup(self, session):
        self.db_session = session
        with self.db_session() as session:
            root = {
                'name': 'root',
            }
            
            session.add(Root(**root))
            session.commit()
        
        yield
        
        #remove test data
        with self.db_session() as session:
            root: Root = session.query(Root).filter(Root.id == 1).first()
            session.delete(root)
            session.commit()


    def test_create_one_to_many(self, session):
        updat_root = {
            'id': 1,
            'name': 'root',
            'branches': [
                {
                    'name': 'created_branch',
                    'nodes': [
                        {
                            'name': 'created_node',
                            'leaves': [
                                {
                                    'name': 'created_leaf_1'
                                },
                                {
                                    'name': 'created_leaf_2'
                                },
                            ]
                        }
                    ]
                },
            ] 
        }
        
        with session() as session:
            root: Root = session.query(Root).filter(Root.id == 1).first()
            root.merge(**updat_root)
            session.commit()
            updated_root: Root = session.query(Root).filter(Root.id == 1).first()
            
            
            assert updated_root.id == 1
            assert updated_root.name == 'root'
            assert len(updated_root.branches) == 1
            assert updated_root.branches[0].id == 1
            assert updated_root.branches[0].name =='created_branch'
            assert updated_root.branches[0].root_id == updated_root.id
            assert len(updated_root.branches[0].nodes) == 1
            assert updated_root.branches[0].nodes[0].name == 'created_node'
            assert len(updated_root.branches[0].nodes[0].leaves) == 2
            assert updated_root.branches[0].nodes[0].leaves[0].name == 'created_leaf_1'
            assert updated_root.branches[0].nodes[0].leaves[1].name == 'created_leaf_2'