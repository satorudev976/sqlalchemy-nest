from test.models import Branch, Leaf, Node, Root
    

def test_declarative_nested_model_constructor_by_dict(session):
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
        assert new_root.branches[0].name =='branch'
        assert len(new_root.branches[0].nodes) == 1
        assert new_root.branches[0].nodes[0].name == 'node'
        assert len(new_root.branches[0].nodes[0].leaves) == 2
        assert new_root.branches[0].nodes[0].leaves[0].name == 'leaf_1'
        assert new_root.branches[0].nodes[0].leaves[1].name == 'leaf_2'
        
        
        
def test_declarative_nested_model_constructor_by_model(session):
    root = Root(id=2, name='root', branches=[
        Branch(id=2, name='branch', nodes=[
            Node(id=2, name='node', leaves=[
                Leaf(id=3, name='leaf_1'),
                Leaf(id=4, name='leaf_2'),
            ])
        ])
    ])
    with session() as session:
        session.add(root)
        session.commit()
        new_root: Root = session.query(Root).filter(Root.id == 2).first()
        
        assert new_root.id == 2
        assert new_root.name == 'root'
        assert len(new_root.branches) == 1
        assert new_root.branches[0].name =='branch'
        assert len(new_root.branches[0].nodes) == 1
        assert new_root.branches[0].nodes[0].name == 'node'
        assert len(new_root.branches[0].nodes[0].leaves) == 2
        assert new_root.branches[0].nodes[0].leaves[0].name == 'leaf_1'
        assert new_root.branches[0].nodes[0].leaves[1].name == 'leaf_2'
        