from flask_restx import Namespace

doctors_namespace = Namespace("doctors", description="Quản lý bác sĩ")
public_namespace = Namespace("public", description="Dữ liệu công khai")
