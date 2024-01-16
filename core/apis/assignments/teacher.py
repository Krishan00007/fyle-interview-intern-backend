from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)

# get a list of assignments submitted to a teacher
@teacher_assignments_resources.route('/teacher/assignments', methods=['GET'], strict_slashes=False)
@decorators.auth_principal
def list_assignments(p):
    assignment_submitted = Assignment.get_assignments_submitted_to_teacher(p.teacher_id)
    assignment_submitted_dump = AssignmentSchema().dump(assignment_submitted, many=True)
    return APIResponse.respond(data=assignment_submitted_dump)

# Grade a assignment submitted by student
@teacher_assignments_resources.route('/teacher/assignments/grade', method=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.auth_principal
def grade_assignment(p, incoming_payload):
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)