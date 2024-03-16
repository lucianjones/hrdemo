from rest_framework import permissions


class ApplicantPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        match request.method:
            case "GET":
                return request.user.has_perm("api.view_applicant")
            case "POST":
                return request.user.has_perm("api.create_applicant")
            case "PUT":
                return request.user.has_perm("api.update_applicant")
            case "DELETE":
                return request.user.has_perm("api.delete_applicant")
            case _:
                return False


class NotePermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        match request.method:
            case "GET":
                return request.user.has_perm("api.view_note")
            case "POST":
                return request.user.has_perm("api.create_note")
            case _:
                return False
