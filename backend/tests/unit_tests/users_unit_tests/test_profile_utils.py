from types import SimpleNamespace
from unittest.mock import patch

from src.utils.users.profile_utils import add_profile_updates, update_extended_profile


def test_add_profile_updates():
    obj = SimpleNamespace(a=1, b=2)
    mapping = {'x': 'a', 'y': 'b'}
    data = {'x': 10}
    add_profile_updates(obj, data, mapping)
    assert obj.a == 10


def test_update_extended_profile_medical_history():
    profile = SimpleNamespace(profile_type='patient', medical_history=None, avatar=None, gender=None)
    update_extended_profile(profile, {'medicalHistory': 'mh'} )
    assert profile.medical_history == 'mh'


def test_update_extended_profile_avatar_and_gender():
    profile = SimpleNamespace(profile_type='patient', medical_history=None, avatar=None, gender=None)
    with patch('src.utils.users.profile_utils.cloudinary_upload_process', return_value='http://img'):
        update_extended_profile(profile, {'avatar': 'file', 'gender': 'male'})
    assert profile.avatar == 'http://img'
    assert profile.gender is not None
