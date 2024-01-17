from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher

from .schema import AssignmentSchema, AssignmentGradeSchema, TeacherSchema
principal_assignment_resources = Blueprint('principal_assignment_resources', __name__)

# get the list of all submitted and graded assignments
@principal_assignment_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    principal_assignments = Assignment.get_assignments_by_principal(p.principal_id)
    principal_assignments_dump = AssignmentSchema().dump(principal_assignments, many=True)
    return APIResponse.respond(data=principal_assignments_dump)

# get the list of all teachers
@principal_assignment_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    principal_teacher = Teacher.get_teachers_by_principal(p.principal_id)
    principal_teacher_dump = TeacherSchema().dump(principal_teacher, many=True)
    return APIResponse.respond(data=principal_teacher_dump)

# Update the grade given by teacher
@principal_assignment_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def update_grade_assignment(p, incoming_payload):
    update_grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

    update_grade_assignment = Assignment.update_grade(
        _id = update_grade_assignment_payload.id,
        grade=update_grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    update_grade_assignment_dump = AssignmentSchema().dump(update_grade_assignment)
    return APIResponse.respond(data=update_grade_assignment_dump)