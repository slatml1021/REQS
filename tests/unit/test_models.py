from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database import Base
from app.models import PriorityMethod, PriorityScore, RelationType, Requirement, RequirementRelation


def test_requirement_relations_and_priority_scores_are_persisted():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        login = Requirement(key="REQ-001", title="Kullanıcı girişi")
        report = Requirement(key="REQ-002", title="Rapor oluşturma")
        session.add_all([login, report])
        session.flush()
        session.add(RequirementRelation(source=report, target=login, relation_type=RelationType.DEPENDS_ON))
        session.add(PriorityScore(requirement=login, method=PriorityMethod.WIEGERS, raw_score=23.5, normalized_score=82.0, inputs={"benefit": 9}))
        session.commit()

        assert report.outgoing_relations[0].target.key == "REQ-001"
        assert login.priority_scores[0].method is PriorityMethod.WIEGERS


def test_self_relation_is_rejected():
    engine = create_engine("sqlite://")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        requirement = Requirement(key="REQ-001", title="Kullanıcı girişi")
        session.add(requirement)
        session.flush()
        session.add(RequirementRelation(source=requirement, target=requirement, relation_type=RelationType.RELATED_TO))
        try:
            session.commit()
        except IntegrityError:
            session.rollback()
        else:
            raise AssertionError("Self-relations must violate the database constraint")
